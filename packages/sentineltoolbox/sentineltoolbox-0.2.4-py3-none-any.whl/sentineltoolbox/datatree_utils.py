__all__ = ["DataTreeHandler", "patch_datatree"]

import copy
from pathlib import PurePosixPath
from typing import Any

from datatree import DataTree

from sentineltoolbox._utils import patch
from sentineltoolbox.attributes import AttributeHandler
from sentineltoolbox.readers._utils import logger
from sentineltoolbox.templates import (
    create_from_template,
    fill_template_with_default_values,
    get_jinja_template,
    render_template_as_json,
)
from sentineltoolbox.typedefs import (
    EOGroup,
    EOProduct,
    T_ContainerWithAttributes,
    is_eoproduct,
)


class DataTreeHandler(AttributeHandler):

    def set_templates(self, **kwargs: Any) -> None:
        self._template_name = None
        self._template = {}

        template = kwargs.get("template")
        if template:
            if isinstance(template, str):
                if not template.endswith(".jinja"):
                    template = template + ".jinja"
                tpl_jinja = get_jinja_template(product_type=template)
                tpl_definition = render_template_as_json(tpl_jinja, context=kwargs.get("context", {}))
                self._template_name = template
                self._template = tpl_definition
            elif isinstance(template, dict):
                if "data" in template:
                    self._template_name = "dict"
                    self._template = template
                else:
                    logger.warning("input template is not valid")

    def _read_short_names(self) -> None:
        if isinstance(self._container, DataTree):
            for ds in self._container.subtree:
                for k, v in ds.variables.items():
                    path = PurePosixPath(ds.path, k)
                    short_name = v.attrs.get("eov_attrs", {}).get("short_name")
                    if short_name:
                        self.__short_names[short_name] = str(path)
        elif is_eoproduct(self._container):
            self.__short_names.update(self._container.short_names)  # type: ignore
        else:
            raise NotImplementedError(f"{type(self)} doesn't support  {type(self._container)}")

    def _create_default_container(self, **kwargs: Any) -> DataTree[Any]:
        container = kwargs.get("container")
        if container is None:
            if self._template:
                tpl_filled = fill_template_with_default_values(self._template)
                container = create_from_template(tpl_filled)
            else:
                container = DataTree()
                self._template = {}
        return container

    def __init__(self, container: DataTree[Any] | EOProduct | None = None, **kwargs: Any):

        self.__short_names: dict[str, str] = {}
        self.set_templates(**kwargs)
        self._container: T_ContainerWithAttributes = self._create_default_container(container=container)
        self._read_short_names()
        self.name = kwargs.get("name")

    @property
    def template(self) -> dict[Any, Any]:
        return self._template

    @property
    def short_names(self) -> dict[str, str]:
        """
        Get the shortnames if available for the product type else empty dict
        """
        return copy.copy(self.__short_names)

    def set_short_name(self, key: str, path: str) -> None:
        if is_eoproduct(self._container):
            self.__short_names[key] = path
            self._container.set_type(self._container.product_type, short_names=self.__short_names)  # type: ignore
        try:
            variable = self._container[path]
        except KeyError:
            self.__short_names[key] = path
        else:
            old_short_name = variable.attrs.get("eov_attrs", {}).get("short_name")
            if old_short_name and old_short_name != key:
                del self.__short_names[old_short_name]
                logger.warning(f"Rename short name {old_short_name!r} to {key!r} (target: {path!r})")
            self.__short_names[key] = path
            variable.attrs.setdefault("eov_attrs", {})["short_name"] = key

    def set_short_names(self, short_names: dict[str, str]) -> None:
        for alias, path in short_names.items():
            self.set_short_name(alias, path)

    def __getitem__(self, key: str) -> Any:
        # Support short name to path conversion
        key = self.__short_names.get(key, key)
        return self._container[key]

    def __setitem__(self, key: str, value: Any) -> None:
        # Support short name to path conversion
        path = self.__short_names.get(key, key)
        self._container[path] = value
        if key != path:
            self.set_short_name(key, path)

    def help(self, path: str, **kwargs: Any) -> dict[Any, Any]:
        return self.help_product(path, **kwargs)

    def update_from_model(
        self,
        *,
        mapping: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        schema: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        update_from_model(self._container, mapping=mapping, template=template, schema=schema, **kwargs)

    @property
    def dt(self) -> T_ContainerWithAttributes:
        return self.container()


def patch_datatree(datatree: Any, **kwargs: Any) -> None:
    patch(datatree, DataTreeHandler, **kwargs)


def convert_template_dict_to_value_dict(tpl: dict[Any, Any]) -> dict[Any, Any]:
    if isinstance(tpl, dict):
        mapping_data = {}
        for name, attr_def in tpl.items():
            if "required" in attr_def and "value" in attr_def:
                mapping_data[name] = attr_def["value"]
            else:
                mapping_data.setdefault(name, {}).update(convert_template_dict_to_value_dict(attr_def))
        return mapping_data
    else:
        return tpl


def update_from_model(
    data: T_ContainerWithAttributes,
    *,
    mapping: dict[str, Any] | None = None,
    template: dict[str, Any] | None = None,
    schema: dict[str, Any] | None = None,
    **kwargs: Any,
) -> None:
    """
    Update attributes of data (and group, variable children) with attributes defined in corresponding mapping.
    Mapping used by this function use mappings syntax or template syntax.

    For mapping syntax: "data_mapping" must be defined with block with at least "target_path" or
    "source_path" and "attributes"

    For template syntax: "data" must be defined with block containing attrs

    For example, this is a JSON **mapping** file valid for this function:

    .. code-block:: json

        {
            "data_mapping": [
                {
                    "source_path": "/group",
                    "attributes": {"documentation": "Group documentation", "complex_attr": {"attr1": 1, "attr2": 2}},
                }
            ]
        }

    For example, this is a JSON **template** file valid for this function:

    .. code-block:: json

        {
            "data": {
                "/group": {
                    "attrs": {
                        "documentation": {"required": true, "value": "Group documentation", "dtype": "str"},
                        "complex_attr": {
                            "attr1": {"required": true, "value": 1, "dtype": "int"},
                            "attr2": {"required": true, "value": 2, "dtype": "int"},
                        },
                    }
                }
            }
        }


    Parameters
    ----------

    data: product you want to update
    mapping: mapping dict
    """
    create = kwargs.get("create", False)
    mapping_data = {}
    if schema is not None:
        raise NotImplementedError("update from schema not implemented yet.")
    if mapping is None and template is None:
        logger.warning("Nothing updated, please specify either mapping or template")

    if mapping is not None:
        if "data_mapping" in mapping:
            for metadata in mapping["data_mapping"]:
                path = metadata.get("target_path", metadata.get("source_path"))
                if path and "attributes" in metadata:
                    mapping_data[path] = metadata["attributes"]
        else:
            logger.warning("Nothing updated, mapping doesn't contain data (key 'data_mapping' not found)")

    if template is not None:
        if "data" in template:
            for path, metadata in template["data"].items():
                if "attrs" in metadata:
                    mapping_data[path] = convert_template_dict_to_value_dict(metadata["attrs"])
        else:
            logger.warning("Nothing updated, template doesn't contain data (key 'data' not found)")

    for path, metadata in mapping_data.items():
        # do not use "path in data" because
        #   in eoproduct: this check only short names and so may return false negative
        #   in datatree: doesn't behave as expected
        try:
            item = data[path]
        except KeyError:
            if create:
                if isinstance(data, DataTree):
                    data[path] = DataTree()
                    item = data[path]
                    item.attrs.update(metadata)
                elif is_eoproduct(data):
                    data[path] = EOGroup()
                else:
                    raise NotImplementedError(
                        f"update_from_model(create=True) is not implemented for data of type {type(data)}",
                    )
        else:
            item.attrs.update(metadata)
