for now, organized as

```
*_algo
├── _select_deposit_site
├── _calc_rank_at_surface_index.py
└── _iter_resident_ranks.py
```


long term, would like to organize as

```
*_algo
├── _enact
│   └── _SelectDepositSite.py
├── _invar
│   ├── _CalcMrcaUncertaintyAbsUpperBound.py
│   ├── _CalcMrcaUncertaintyAbsUpperBoundPessimalRank.py
│   ├── _CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank.py
│   ├── _CalcMrcaUncertaintyRelUpperBound.py
│   ├── _CalcMrcaUncertaintyRelUpperBoundPessimalRank.py
│   └── _CalcMrcaUncertaintyRelUpperBoundAtPessimalRank.py
├── _scry
│   ├── _IterResidentRanks.py
│   ├── _CalcRankAtSurfaceIndex.py
│   ├── _CalcMrcaUncertaintyAbsExact.py
│   └── _CalcMrcaUncertaintyRelExact.py
├── _Policy.py
└── _PolicySpec.py
```

note: `PolicySpec` will contain `surface_size`
