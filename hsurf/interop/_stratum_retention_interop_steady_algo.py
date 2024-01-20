from ..site_selection_strategy.site_selection_algorithms import (
    steady_algo as _site_selection_algo,
)
from ._make_stratum_retention_policy_from_site_selection_algo import (
    make_stratum_retention_policy_from_site_selection_algo,
)

Policy = make_stratum_retention_policy_from_site_selection_algo(
    _site_selection_algo
)
PolicySpec = Policy.policy_spec_t

# prevent name leakage
del make_stratum_retention_policy_from_site_selection_algo
