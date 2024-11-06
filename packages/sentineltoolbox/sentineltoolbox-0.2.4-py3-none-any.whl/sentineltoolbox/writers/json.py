import logging
from typing import Any

from zarr import MemoryStore
from zarr.attrs import Attributes

logger = logging.getLogger("sentineltoolbox")


def serialize_to_zarr_json(log_data: Any, **kwargs: Any) -> bool:
    store = MemoryStore()
    attrs = Attributes(store)
    errors = kwargs.get("errors", "strict")
    try:
        attrs[""] = log_data
    except TypeError:
        if errors == "replace":
            # eschalk: call your code "to_json_best_effort" here
            # and recall serialize_to_zarr(jsonified, errors="strict") to be sure jsonified code
            # can be serialized with zarr
            logger.warning(f"{errors=!r} not implemented yet, equivalent to 'strict'")
            logger.warning(f"Cannot log data of type {type(log_data)!r}. zarr cannot serialize it.")
        elif errors == "ignore":
            pass
        else:
            logger.warning(f"Cannot log data of type {type(log_data)!r}. zarr cannot serialize it.")
        return False
    else:
        return log_data
