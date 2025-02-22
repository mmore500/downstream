from copy import deepcopy
import types
import typing

_DSurfDataItem = typing.TypeVar("_DSurfDataItem")


class Surface(typing.Generic[_DSurfDataItem]):
    "Container orchestrating downstream curation over a fixed-size buffer."

    __slots__ = ("_storage", "algo", "T")

    algo: types.ModuleType
    _storage: typing.MutableSequence[typing.Optional[_DSurfDataItem]]  # storage sites
    T: int  # current logical time

    def __init__(
        self: "Surface",
        algo: types.ModuleType,
        storage: typing.Union[
            typing.MutableSequence[typing.Optional[_DSurfDataItem]], int
        ],
    ) -> None:
        """Initialize a downstream Surface object, which stores hereditary
        stratigraphic annotations using a provided algorithm.

        Parameters
        ----------
        algo: module
            The algorithm used by the surface to determine the placements
            of data items. Should be one of the modules in `downstream.dstream`.
        storage: int or MutableSequence
            The object used to hold any ingested data. If an integer is
            passed in, a list of length `storage` is used. Otherwise, the
            `storage` is used directly. Random access and `__len__` must be
            supported. For example, for efficient storage, a user may pass
            in a NumPy array.
        """
        self.T = 0
        if isinstance(storage, int):
            self._storage = [None] * storage
        else:
            self._storage = storage
        self.algo = algo

    def __iter__(self: "Surface") -> typing.Iterator[typing.Optional[_DSurfDataItem]]:
        return iter(self._storage)

    def __getitem__(self: "Surface", site: int) -> typing.Optional[_DSurfDataItem]:
        return self._storage[site]

    def __deepcopy__(self: "Surface", memo: dict) -> "Surface":
        """An overloaded deepcopy to prevent a pickle error with cloning modules"""
        return Surface(self.algo, deepcopy(self._storage, memo))

    @property
    def S(self: "Surface") -> int:
        return len(self._storage)

    def enumerate(
        self: "Surface",
    ) -> typing.Iterable[
        typing.Tuple[typing.Optional[int], typing.Optional[_DSurfDataItem]]
    ]:
        """
        Iterate over ingest times and values of data items in the order they 
        appear on the downstream storage, including sites not yet written to.
        """
        return zip(self.lookup(), self._storage)

    def enumerate_retained(
        self: "Surface",
    ) -> typing.Iterable[typing.Tuple[int, _DSurfDataItem]]:
        """
        Iterate over ingest times and value of data items in sites that 
        have been written to.
        """
        return (  # type: ignore
            (T, v)
            for T, v in self.enumerate()
            if T is not None
        )

    def ingest_items(
        self: "Surface",
        n_ingests: int,
        item_getter: typing.Callable[[int], _DSurfDataItem],
        use_relative_time: bool = False,
    ) -> None:
        """Ingest multiple data items.

        Optimizes for the case where large amounts of data is ready to be 
        ingested, In such a scenario, we can avoid assigning multiple objects
        to the same site, and simply iterate through sites that would be
        updated after items were ingested.

        Parameters
        ----------
        n_ingests : int
            The number of data to ingest
        item_getter : int -> object
            For a given ingest time within the n_ingests window, should
            return the associated data item.
        use_relative_time : bool, default False 
            Use the relative time (i.e. timesteps since current self.T) 
            instead of the absolute time as input to `item_getter`
        """

        assert n_ingests >= 0
        if n_ingests == 0:
            return

        assert self.algo.has_ingest_capacity(self.S, self.T + n_ingests - 1)
        for site, (T_1, T_2) in enumerate(
            zip(
                self.lookup(),
                self.algo.lookup_ingest_times(self.S, self.T + n_ingests),
            )
        ):
            if T_1 != T_2 and T_2 is not None:
                self._storage[site] = item_getter(T_2 - self.T if use_relative_time else T_2)
        self.T += n_ingests

    def ingest_item(self: "Surface", item: _DSurfDataItem) -> typing.Optional[int]:
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

    def lookup(self: "Surface") -> typing.Iterable[typing.Optional[int]]:
        """Iterate over data item ingest times, including null values for uninitialized sites."""
        assert len(self._storage) == self.S
        return self.algo.lookup_ingest_times(self.S, self.T)

    def lookup_retained(self: "Surface") -> typing.Iterable[int]:
        """Iterate over ingest times of (possibly null) data items."""
        return (T for T in self.lookup() if T is not None)
