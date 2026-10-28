#!/usr/bin/env bash
# Rebuild the entire frozen CFSG proof chain on a capable Linux host.
# This script does not modify original theorem or certificate files.
set -Eeuo pipefail

cd "$(dirname "$0")/.."
LOG_DIR=${CFSG_LOG_DIR:-audit-results/cfsg-rebuild}
JOBS=${CFSG_JOBS:-4}
BUILD_TIMEOUT=${CFSG_BUILD_TIMEOUT:-20h}
mkdir -p "$LOG_DIR"

PHASE="startup"
finish() {
  local rc=$?
  python3 - "$LOG_DIR" "$rc" "$PHASE" <<'PY'
import json, pathlib, subprocess, sys, datetime
path, rc, phase = sys.argv[1], int(sys.argv[2]), sys.argv[3]
def git(*args):
    p=subprocess.run(["git",*args], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    return p.stdout.strip() if p.returncode == 0 else None
result = {
    "schema_version": 1,
    "kind": "cfsg_full_rebuild",
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "head": git("rev-parse","HEAD"),
    "original_source_commit": "69cb972f587a3ecc035e092253167ff2e303c962",
    "phase_completed_or_failed": phase,
    "exit_code": rc,
    "status": "PASS" if rc == 0 and phase == "complete" else "UNRESOLVED_OR_FAILED",
    "evidence": ["environment.txt", "source-preflight.json", "full-lake-build.log",
                 "final-axiom-output.log", "axiom-results.json"],
    "caveat": "Only PASS with complete logs means the pinned project built and two theorem axiom outputs passed the parser; it is not external mathematical peer review."
}
pathlib.Path(path, "rebuild-summary.json").write_text(json.dumps(result,indent=2)+"\n")
PY
}
trap finish EXIT

PHASE="environment"
{
  date -u
  uname -a
  pwd
  git rev-parse HEAD
  git status --porcelain
  df -h .
  free -h 2>/dev/null || true
  command -v lake || true
  command -v lean || true
  lake --version
  lean --version
  cat lean-toolchain
  sha256sum lake-manifest.json comparator.json lean-toolchain
} > "$LOG_DIR/environment.txt" 2>&1
cat "$LOG_DIR/environment.txt"

PHASE="static-preflight"
python3 scripts/verify_cfsg_source.py --report "$LOG_DIR/source-preflight.json"

PHASE="full-lake-build"
echo "Starting full Lake build. Timeout=$BUILD_TIMEOUT, jobs=$JOBS"
# Run the actual project-wide target, not just a comparator module.
set +e
timeout --preserve-status "$BUILD_TIMEOUT" lake build -j "$JOBS" \
    > "$LOG_DIR/full-lake-build.log" 2>&1
build_rc=$?
set -e
tail -n 60 "$LOG_DIR/full-lake-build.log" || true
if [[ "$build_rc" -ne 0 ]]; then
  echo "Full lake build failed or timed out: exit $build_rc"
  exit "$build_rc"
fi

PHASE="final-axiom-probe"
set +e
timeout --preserve-status 60m lake env lean audit/CFSGChainCheck.lean \
    > "$LOG_DIR/final-axiom-output.log" 2>&1
probe_rc=$?
set -e
cat "$LOG_DIR/final-axiom-output.log"
if [[ "$probe_rc" -ne 0 ]]; then
  echo "Axiom probe did not complete successfully: exit $probe_rc"
  exit "$probe_rc"
fi

PHASE="axiom-closure-parsing"
python3 scripts/verify_cfsg_axioms.py \
    --log "$LOG_DIR/final-axiom-output.log" \
    --report "$LOG_DIR/axiom-results.json"

PHASE="complete"
echo "Full frozen CFSG project build and two final-axiom checks completed."
echo "Do not infer the 46 Zoo animal kernels have run."
