from pathlib import Path
from typing import Any, TypeVar


def find_files_on_path_with_patterns(d: str, patterns: list) -> list:
    return [str(p.resolve()) for p in Path(d).glob("**/*") if p.suffix in patterns]


T = TypeVar("T")


class NoPublicConstructor(type):
    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: T, *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore
