module

/-!
This file is an independent *probe*, NOT a new CFSG proof or a claim that
the 46 Monolithic Zoo animal kernels ran.

Run only after the frozen CFSG proof tree has been completely rebuilt.
Its printed output must be captured and audited independently.
-/

import Comparator.Solution
import CFSG.Milestones.CFSG_classification

public section

#check CFSGComparator.classification
#check CFSG.Certified.classification_finite_simple_groups
#check CFSG.classification_finite_simple_groups
#check CFSG.Milestones.cfsg_classification_native_and_realization

#print axioms CFSGComparator.classification
#print axioms CFSG.Milestones.cfsg_classification_native_and_realization
