from typing import Any, MutableMapping

from sentineltoolbox.exceptions import LoadingDataError, MissingAdfError
from sentineltoolbox.models.filename_generator import AdfFileNameGenerator
from sentineltoolbox.readers.open_metadata import load_metadata
from sentineltoolbox.typedefs import is_eopf_adf


def extract_semantic_from_alias(alias: str) -> str | None:
    try:
        adf_fn = AdfFileNameGenerator.from_string(alias)
    except NotImplementedError:
        return None
    else:
        return adf_fn.semantic


def check_adfs(adfs: MutableMapping[str, Any], *, required: list[str] | None = None) -> None:
    if required is None:
        required = []
    input_types = {}
    for alias, adf in adfs.items():
        semantic = extract_semantic_from_alias(alias)
        if semantic is None:
            if is_eopf_adf(adf):
                try:
                    attrs = load_metadata(adf)
                except (FileNotFoundError, LoadingDataError):
                    semantic = alias
                else:
                    try:
                        semantic = attrs.get_stac_property("product:type")
                    except KeyError:
                        semantic = alias
            else:
                semantic = alias

        input_types[alias] = semantic

    for adf_name in required:
        if adf_name not in input_types.values():
            str_inputs = "\n  - ".join([f"{k!r}: {v!r}" for k, v in input_types.items()])
            raise MissingAdfError(f"ADF {adf_name!r} is required but not found in inputs: \n  - {str_inputs}")
