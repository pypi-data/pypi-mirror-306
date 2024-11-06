from typing import Any

from datatree import DataTree

from sentineltoolbox.readers.open_datatree import open_datatree


def convert_safe_to_datatree(
    url: Any,
    *,
    product_type: str,
    attrs: dict[str, Any],
    name: str | None = None,
    **kwargs: Any,
) -> DataTree[Any]:
    kwargs["attrs"] = attrs
    kwargs["use_eopf_for_metadata"] = kwargs.get("use_eopf_for_metadata", False)
    kwargs["output_product_type"] = product_type

    xdt = open_datatree(url, **kwargs)
    if name is not None:
        xdt.name = name
    return xdt
