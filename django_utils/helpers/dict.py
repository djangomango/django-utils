import contextlib
from typing import Any


def get_dict_item_or_default(dic: Any, idx: Any, default: Any = None) -> Any:
    """Returns the item of the given dictionary with the given index or the default value if the index does not exist."""
    try:
        return dic[idx]
    except IndexError:
        return default


def del_dict_item_if_exists(dic: dict[Any, Any], key: Any) -> None:
    """Deletes the item of the given dictionary with the given key if it exists."""
    with contextlib.suppress(KeyError):
        del dic[key]
