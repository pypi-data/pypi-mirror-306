import datetime
import logging
from typing import Any

from sentineltoolbox.readers.resources import load_resource_file
from sentineltoolbox.typedefs import MetadataType_L, fix_datetime

"""
Some useful links:
https://eoframework.esa.int/display/CDSE/Copernicus+Data+Space+Ecosystem+%28CDSE%29+STAC+catalogue
"""

logger = logging.getLogger("sentineltoolbox")

aliases_and_short_names: dict[str, Any] = load_resource_file("attributes_hotfix/aliases.json")
valid_aliases: dict[str, str] = aliases_and_short_names.get("aliases", {})
legacy_aliases = {v: k for k, v in valid_aliases.items()}
attribute_short_names: dict[str, tuple[MetadataType_L, str]] = {}

"""
"short_names": { "metadata": ["root_attr", "alias->relpath/to/real/attr"]},
"""
for category, short_names in aliases_and_short_names.get("short_names", {}).items():
    for short_name in short_names:
        if "->" in short_name:
            parts = short_name.split("->")
            alias, path = parts[0], parts[1]
        else:
            alias = path = short_name
        attribute_short_names[alias] = (category, path)

for legacy, valid in valid_aliases.items():
    if valid in attribute_short_names:
        attribute_short_names[legacy] = attribute_short_names[valid]


def to_lower(value: str, **kwargs: Any) -> str:
    path = kwargs.get("path", "value")
    new_value = value.lower()
    if value != new_value:
        logger.warning(f"{path}: value {value!r} has been fixed to {new_value!r}")
    return new_value


# Function used to fix definitly value
fix_functions: dict[MetadataType_L, dict[str, Any]] = {
    "stac_properties": {"platform": to_lower, "mission": to_lower},
}


class Converter:
    json_type: type
    py_type: type

    def to_json(self, value: Any, **kwargs: Any) -> Any:
        return str(value)

    def from_json(self, value: Any, **kwargs: Any) -> Any:
        return value


class ConverterDateTime(Converter):
    json_type: type = str
    py_type: type = datetime.datetime

    def to_json(self, value: Any, **kwargs: Any) -> Any:
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        else:
            return str(value)

    def from_json(self, value: Any, **kwargs: Any) -> Any:
        return fix_datetime(value)


# Function used to convert value when get or set
convert_functions: dict[MetadataType_L, dict[str, Converter]] = {
    "stac_properties": {
        "created": ConverterDateTime(),
        "end_datetime": ConverterDateTime(),
        "start_datetime": ConverterDateTime(),
    },
}
