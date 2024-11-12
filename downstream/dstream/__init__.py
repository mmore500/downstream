import lazy_loader

__getattr__, __dir__, __all__ = lazy_loader.attach(
    __name__,
    [
        "steady_algo",
        "stretched_algo",
        "tilted_algo",
    ],
)
