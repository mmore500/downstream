# C++

See the [Python quickstart](quickstart.md) for outline and intuition.

## Installation

C++ downstream is packaged as a header-only library. It can be added to a system-wide include path, or incorporated as a git submodule in another project.

## API Reference

Each algorithm variant is accessible through its own namespace:
- Steady: `downstream::dstream_steady`
- Stretched: `downstream::dstream_stretched`
- Tilted: `downstream::dstream_tilted`
See [selecting a dstream algorithm](algorithm.md) for more information.

```
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
bool has_ingest_capacity(const UINT S, const UINT T);
```
Determines if there is capacity to ingest a data item at logical time T.

```
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
std::optional<UINT> assign_storage_site(const UINT S, const UINT T);
```
Site selection algorithm for steady curation. Returns selected site or nullopt if data should be discarded.

### Internal Implementation
```
template <std::unsigned_integral UINT = DOWNSTREAM_UINT>
UINT _assign_storage_site(const UINT S, const UINT T);
```