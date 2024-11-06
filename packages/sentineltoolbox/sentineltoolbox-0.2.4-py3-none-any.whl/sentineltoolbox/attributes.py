import copy
import logging
import warnings
from pathlib import Path
from typing import Any, Generator, MutableMapping

from sentineltoolbox._utils import string_to_slice
from sentineltoolbox.attributes_hotfix import (
    attribute_short_names,
    convert_functions,
    fix_functions,
    legacy_aliases,
    valid_aliases,
)
from sentineltoolbox.readers.resources import load_resource_file
from sentineltoolbox.typedefs import (
    MetadataType_L,
    T_Attributes,
    T_ContainerWithAttributes,
    category_paths,
    is_attributes,
    is_container_with_attributes,
)
from sentineltoolbox.writers.json import serialize_to_zarr_json

logger = logging.getLogger("sentineltoolbox")

__all__ = ["AttributeHandler"]


def path_relative_to_category(path: str, category: MetadataType_L | None) -> str:
    if category in ("stac_properties", "stac_discovery", "metadata"):
        return path.replace(category_paths[category], "")
    else:
        return path


def fix_attribute_value(path: str, value: Any, category: MetadataType_L | None) -> Any:
    if category is None:
        return value
    else:
        new_value = value
        relpath = path_relative_to_category(path, category)

        conversions = fix_functions.get(category, {})
        if relpath in conversions:
            fix_function = conversions[relpath]
            new_value = fix_function(value, path=path)

        return new_value


def to_json(path: str, value: Any, category: MetadataType_L | None) -> Any:
    if category is None:
        return value
    else:
        new_value = value
        relpath = path_relative_to_category(path, category)

    conversions = convert_functions.get(category, {})
    if relpath in conversions:
        converter = conversions[relpath]
        new_value = converter.to_json(value, path=path)

    return new_value


def from_json(path: str, value: Any, category: MetadataType_L | None) -> Any:
    if category is None:
        return value
    else:
        new_value = value
        relpath = path_relative_to_category(path, category)

    conversions = convert_functions.get(category, {})
    if relpath in conversions:
        converter = conversions[relpath]
        new_value = converter.from_json(value, path=path)

    return new_value


def guess_category(path: str, **kwargs: Any) -> MetadataType_L | None:
    category = kwargs.get("category")
    if category is not None:
        return category
    if path.startswith("properties") or path.startswith("stac_discovery/properties"):
        return "stac_properties"
    elif path.startswith("stac_discovery"):
        return "stac_discovery"
    elif path.startswith("other_metadata") or path.startswith("metadata"):
        return "metadata"
    elif path in attribute_short_names:
        # search in prop lookuptable / short names
        return attribute_short_names[path][0]
    else:
        # else: no category in path, not find in lookup table => None
        return None


def get_valid_alias(path: str, **kwargs: Any) -> str:
    warn = kwargs.get("warn_deprecated", True)

    if path in valid_aliases:
        newpath = valid_aliases[path]
    else:
        newpath = path
    if path != newpath and warn:
        logger.warning(f"{path!r} is deprecated, use {newpath!r} instead")
    return newpath


def get_legacy_alias(part: str, **kwargs: Any) -> str:
    if part in legacy_aliases:
        return legacy_aliases[part]
    else:
        return part


def _get_attr_dict(data: T_ContainerWithAttributes | T_Attributes) -> T_Attributes:
    if is_container_with_attributes(data):
        return data.attrs  # type: ignore
    elif is_attributes(data):
        return data  # type: ignore
    else:
        raise ValueError(f"type {type(data)} is not supported")


def fix_attribute_path(path: str, category: MetadataType_L | None = None, **kwargs: Any) -> str:
    if category is None:
        category = guess_category(path)
    if category is None:
        return path

    recognized_properties = ["stac_discovery/properties/", "properties/"]
    recognized_stac = ["stac_discovery/"]
    recognized_metadata = ["other_metadata/", "metadata/"]
    recognized_prefixes = recognized_properties + recognized_stac + recognized_metadata

    if category == "stac_properties":
        prefix = "stac_discovery/properties/"
    elif category == "stac_discovery":
        prefix = "stac_discovery/"
    elif category == "metadata":
        prefix = "other_metadata/"
    else:
        prefix = ""

    for possible_prefix in recognized_prefixes:
        prefix_parts = possible_prefix.split("/")

        for prefix_part in prefix_parts:
            if prefix_part and path.startswith(prefix_part):
                path = path[len(prefix_part) + 1 :]  # noqa: E203

    category_fixed_path = prefix + path
    fixed_parts = []
    for part in category_fixed_path.split("/"):
        fixed_parts.append(get_valid_alias(part))
    return "/".join(fixed_parts)


def find_and_fix_attribute(
    attrs: T_Attributes,
    path: str,
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> tuple[Any, str, str]:
    convert_value_type = kwargs.get("convert_value_type", True)

    if category is None and path is not None:
        category = guess_category(path)

    # Define all possible place, depending on category
    places_properties = [
        ("stac_discovery/properties/", attrs.get("stac_discovery", {}).get("properties")),
        ("properties/", attrs.get("properties")),
        # ("stac_discovery/", attrs.get("stac_discovery")),
    ]
    places_metadata = [
        ("other_metadata/", attrs.get("other_metadata")),
        ("metadata/", attrs.get("metadata")),
    ]
    places_stac = [
        ("stac_discovery/", attrs.get("stac_discovery")),
    ]
    places_root: list[tuple[str, Any]] = [("", attrs)]
    if category == "stac_properties":
        # search order: stac_discovery/properties -> properties -> root
        places = places_properties + places_root
    elif category == "metadata":
        # search order: other_metadata -> root
        places = places_metadata + places_root
    elif category == "stac_discovery":
        # search order: stac_discovery -> root
        places = places_stac + places_root
    elif category == "root":
        places = places_root
    else:
        category = None
        places = places_root + places_properties + places_stac + places_metadata

    # remove trailing space
    path = path.strip().rstrip("/")

    value = None

    real_path_parts = []
    partially_valid_path = []

    for place_path, place in places:
        if place is None:
            continue

        if place_path:
            real_path_parts = [place_path.rstrip("/")]
        else:
            real_path_parts = []

        group = place
        parts: list[str] = path.split("/")
        value_found = False
        for part in parts:

            try:
                valid_part: int | slice | str = int(part)
            except ValueError:
                try:
                    valid_part = string_to_slice(part)
                except ValueError:
                    valid_part = part

            if isinstance(valid_part, (int, slice)):
                real_path_parts.append(part)
                if isinstance(group, list):
                    group = group[valid_part]
                    value_found = True
                else:
                    raise KeyError(
                        f"Invalid path {path!r}. Part {valid_part!r} is not correct because {group} is not a list",
                    )
            else:
                valid_name = get_valid_alias(part, warn_deprecated=False)
                legacy_name = get_legacy_alias(part, **kwargs)
                if valid_name in group:
                    value_found = True
                    group = group[valid_name]
                    real_path_parts.append(valid_name)
                elif legacy_name in group:
                    value_found = True
                    group = group[legacy_name]
                    real_path_parts.append(legacy_name)
                else:
                    # key not found on this place, try another place
                    # useless to continue the end of the path => break
                    value_found = False
                    if part != parts[0]:
                        partially_valid_path = ["/".join(real_path_parts), part]
                    break

        if value_found:
            break
    if value_found:
        value = group
        real_path = "/".join(real_path_parts)
        fixed_path = fix_attribute_path(real_path, category, warn_deprecated=kwargs.get("warn_deprecated", True))
        if convert_value_type:
            value = fix_attribute_value(fixed_path, value, category=category)
        return value, fixed_path, real_path
    else:
        if "default" in kwargs or "create" in kwargs:
            default = kwargs.get("default")
            path = fix_attribute_path(path, category=category, **kwargs)
            if "create" in kwargs:
                set_attr(attrs, path, default, category=category, **kwargs)
                return default, path, path
            else:
                return default, path, ""
        else:
            if partially_valid_path:
                valid_part, incorrect_part = partially_valid_path
                msg = f"{path}. {valid_part} exists but not {incorrect_part}"
            else:
                msg = path
            raise KeyError(msg)


def recurse_json_dict(
    d: MutableMapping[Any, Any] | list[Any],
    root: str = "",
) -> Generator[tuple[str, Any], None, None]:
    if isinstance(d, dict):
        items = list(d.items())
    elif isinstance(d, list):
        items = [(str(i), v) for i, v in enumerate(d)]
    else:
        items = []

    for k, v in items:
        path = root + k + "/"
        yield path, v
        if isinstance(v, (dict, list)):
            yield from recurse_json_dict(v, path)


def search_attributes(
    attrs: T_ContainerWithAttributes | T_Attributes,
    path: str,
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> list[str]:
    kwargs["warn_deprecated"] = kwargs.get("warn_deprecated", False)
    kwargs["convert_value_type"] = kwargs.get("convert_value_type", False)
    recursive = kwargs.get("recursive", True)
    limit = kwargs.get("limit")

    dict_attrs: T_Attributes = _get_attr_dict(attrs)
    results = set()

    try:
        value, fixed, real = find_and_fix_attribute(dict_attrs, path, category=category, **kwargs)
        results.add(real)
    except KeyError:
        pass

    if recursive:
        for p, v in recurse_json_dict(dict_attrs):
            if isinstance(limit, int) and len(results) > limit:
                break
            if not isinstance(v, dict):
                continue
            current_category = guess_category(p)
            if category is not None and current_category != category:
                continue
            try:
                value, fixed, real = find_and_fix_attribute(v, path, category=category, **kwargs)
            except KeyError:
                pass
            else:
                results.add(p + real)
    return list(sorted(results))


def extract_attr(
    data: T_ContainerWithAttributes | T_Attributes,
    path: str | None = None,
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> Any:
    attrs = _get_attr_dict(data)
    if path is None:
        if category is None:
            return attrs
        else:
            category_path = category_paths[category]
            return extract_attr(attrs, category_path)
    else:
        value, fixed_path, real_path = find_and_fix_attribute(attrs, path, category=category, **kwargs)
        return from_json(fixed_path, value, category=guess_category(fixed_path, category=category))


def set_attr(
    data: T_ContainerWithAttributes | T_Attributes,
    path: str,
    value: Any,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> MutableMapping[Any, Any]:
    root_attrs = _get_attr_dict(data)
    path = fix_attribute_path(path, category=category)
    category = guess_category(path, category=category)
    attrs = root_attrs
    parts = path.split("/")
    for part in parts[:-1]:
        attrs = attrs.setdefault(part, {})
    if kwargs.get("fix", True):
        value = fix_attribute_value(path, value, category=category)
    if kwargs.get("format", True):
        value = from_json(path, value, category=category)
    attrs[parts[-1]] = to_json(path, value, category=category)
    return root_attrs


def append_log(container: T_ContainerWithAttributes, log_data: Any, **kwargs: Any) -> None:
    """
    See :obj:`AttributeHandler.append_log`

    :param container: container to update
    """
    AttributeHandler(container, **kwargs).append_log(log_data, **kwargs)


def get_logs(container: T_ContainerWithAttributes, **kwargs: Any) -> list[Any]:
    """
    See :obj:`AttributeHandler.get_logs`

    :param container: container containing log metadata
    """
    return AttributeHandler(container, **kwargs).get_logs(**kwargs)


def _extract_namespace_name(attribute_handler_name: str | None, **kwargs: Any) -> tuple[str, str]:
    namespace = kwargs.get("namespace", "processing_unit_history")
    name = kwargs.get("name", attribute_handler_name if attribute_handler_name is not None else "root")
    return namespace, name


class AttributeHandler:
    """
    TODO: if set, read stac_discovery/stac_extensions to automatically recognize stac properties.
    For examlple, if view is in stac_extension, help('view:incidence_angle') automatically understand that
    "view:incidence_angle" is equivalent to "stac_discovery/properties/view:incidence_angle"
    """

    def __init__(self, container: T_ContainerWithAttributes | T_Attributes | None = None, **kwargs: Any):
        """

        :param container:
        :param kwargs:
          - template: template name to use
          - context: template context
          - name:
        """
        if container is None:
            container = {}
        self._container = container
        self.name = kwargs.get("name")

    def to_dict(self) -> MutableMapping[Any, Any]:
        """

        :return: convert it to dict. If container is a dict, return a copy of it
        """
        return copy.copy(_get_attr_dict(self._container))

    def container(self) -> Any:
        return self._container

    def append_log(self, log_data: Any, **kwargs: Any) -> None:
        """
        :param log_data: data you want to log
        :param kwargs:
          * name: processing unit name. Default: AttributeHandler.name or `"root"` if not set
          * namespace: group containing all logs. Default: `"processing_unit_history"`
        :return:
        """
        log_data = serialize_to_zarr_json(log_data, **kwargs)
        namespace, name = _extract_namespace_name(self.name, **kwargs)
        history = self.get_metadata(namespace, create=True, default={})
        history.setdefault(name, []).append(log_data)

    def get_logs(self, **kwargs: Any) -> list[Any]:
        """
        :param kwargs:
          * name: processing unit name. Default: AttributeHandler.name or `"root"` if not set
          * namespace: group containing all logs. Default: `"processing_unit_history"`
        :return: all logs registered in products
        """
        namespace, name = _extract_namespace_name(self.name, **kwargs)
        return self.get_metadata(f"{namespace}/{name}", default=[])

    def set_property(self, path: str, value: Any, **kwargs: Any) -> None:
        warnings.warn("use set_stac_property instead", DeprecationWarning)
        self.set_stac_property(path, value, **kwargs)

    def set_stac_property(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="stac_properties", **kwargs)

    def set_metadata(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="metadata", **kwargs)

    def set_stac(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="stac_discovery", **kwargs)

    def set_root_attr(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="root", **kwargs)

    def set_attr(self, path: str, value: Any, category: MetadataType_L | None = None, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category=category, **kwargs)

    def get_attr(self, path: str | None = None, category: MetadataType_L | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category=category, **kwargs)

    def get_stac_property(self, path: str | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category="stac_properties", **kwargs)

    def get_metadata(self, path: str | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category="metadata", **kwargs)

    def get_stac(self, path: str | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category="stac_discovery", **kwargs)

    def get_root_attr(self, path: str | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category="root", **kwargs)

    def search(
        self,
        path: str,
        *,
        category: MetadataType_L | None = None,
        **kwargs: Any,
    ) -> list[str]:
        return search_attributes(self._container, path, category=category, **kwargs)

    def fix_path(self, path: str, **kwargs: Any) -> str:
        return fix_attribute_path(path, **kwargs)

    def _help(
        self,
        path: str,
        description_data: list[Any],
        documentation_data: list[Any],
        **kwargs: Any,
    ) -> dict[str, Any]:
        help_data = {}
        attrs = _get_attr_dict(self._container)
        try:
            value, fixed, real = find_and_fix_attribute(attrs, path)
        except KeyError:
            pass
        else:

            help_data["value"] = value
            path = real
        category = guess_category(path)
        path = self.fix_path(path, category=category)
        name = Path(path).name
        if category:
            help_data["category"] = category
            help_data["path"] = fix_attribute_path(path)
        if category == "stac_properties":
            from sentineltoolbox.stacutils import STAC_PROPERTIES

            try:
                data, _, _ = find_and_fix_attribute(STAC_PROPERTIES, name, category=category)
            except KeyError:
                pass
            else:
                help_data.update(copy.copy(data))
        for field, field_dbs in [
            ("description", description_data),
            ("documentation", documentation_data),
        ]:
            for db in field_dbs:
                try:
                    found, _, _ = find_and_fix_attribute(db, name)
                except KeyError:
                    pass
                else:
                    help_data[field] = found
                    break
        return help_data

    def fix(self) -> None:
        for category, attr_dict in fix_functions.items():
            for attr_relpath in attr_dict:
                try:
                    current_value = self.get_attr(attr_relpath, category=category)
                except KeyError:
                    pass
                else:
                    self.set_attr(attr_relpath, current_value, category=category)

        for category, attr_dict in convert_functions.items():
            for attr_relpath, converter in attr_dict.items():
                try:
                    current_value = self.get_attr(attr_relpath, category=category)
                except KeyError:
                    pass
                else:
                    fixed_value = converter.to_json(converter.from_json(current_value))
                    self.set_attr(attr_relpath, fixed_value, category=category)

    def help_product(self, path: str, **kwargs: Any) -> dict[Any, Any]:
        product_description = load_resource_file("metadata/product_description.json", **kwargs)
        product_documentations = load_resource_file("metadata/product_documentation.toml", **kwargs)

        description_data = [product_description]
        documentation_data = [product_documentations]

        return self._help(path, description_data, documentation_data, **kwargs)

    def help_attr(self, path: str, **kwargs: Any) -> dict[Any, Any]:
        prop_descriptions = load_resource_file("metadata/product_properties.json", target_type=dict, **kwargs)
        prop_documentation = load_resource_file("metadata/product_properties_documentation.json", **kwargs)
        term_description = load_resource_file("metadata/term_description.json", **kwargs)
        term_documentation = load_resource_file("metadata/term_documentation.json", **kwargs)

        description_data = [prop_descriptions, term_description]
        documentation_data = [prop_documentation, term_documentation]

        return self._help(path, description_data, documentation_data, **kwargs)

    def help(self, path: str, **kwargs: Any) -> dict[Any, Any]:
        return self.help_attr(path, **kwargs)
