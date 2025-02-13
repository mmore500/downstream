import types
import typing
import opytional as opyt


class Surface:

    __slots__ = ("_storage", "algo", "T")

    algo: types.ModuleType
    _storage: typing.MutableSequence  # storage sites
    T: int  # current logical time

    def __init__(
        self: "Surface",
        algo:types.ModuleType,
        storage: typing.Union[typing.MutableSequence[object], int]
    ) -> None:
        self.T = 0
        if isinstance(storage, int):
            self._storage = [None] * storage
        else:
            self._storage = storage
        self.algo = algo

    def __iter__(self: "Surface") -> typing.Iterable[object]:
        return iter(self._storage)

    def __getitem__(self: "Surface", site: int) -> object:
        return self._storage[site]

    @property 
    def S(self):
        return len(self._storage)

    def enumerate(
        self: "Surface",
    ) -> typing.Iterable[typing.Tuple[int, object]]:
        """Iterate over ingest times and values of retained data items."""
        return zip(self.lookup(), self._storage)

    def ingest(self: "Surface", item: object) -> typing.Optional[int]:
        """Ingest data item.

        Returns the storage site of the data item, or None if the data item is
        not retained.
        """
        assert self.algo.has_ingest_capacity(self.S, self.T)

        site = self.algo.assign_storage_site(self.S, self.T)
        if site is not None:
            self._storage[site] = item
        self.T += 1
        return site

    def lookup(self: "Surface") -> typing.Iterable[int]:
        """Iterate over ingest times of retained data items."""
        assert len(self._storage) == self.S
        return self.algo.lookup_ingest_times(self.S, self.T)
