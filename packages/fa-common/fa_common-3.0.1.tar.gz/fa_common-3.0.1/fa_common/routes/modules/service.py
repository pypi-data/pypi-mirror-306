import yaml

from fa_common.exceptions import NotFoundError
from fa_common.storage import get_storage_client

from .types import ParameterSettings


def format_any_of_schema(schema):
    # Process properties
    if "properties" in schema:
        for key, value in schema["properties"].items():
            # Handle anyOf and remove null types
            if "anyOf" in value:
                # Filter out the null type and assign better titles
                new_anyOf = []
                for index, type_option in enumerate(value["anyOf"]):
                    if type_option.get("type") != "null":
                        type_name = type_option.get("type", f"Option {index + 1}")
                        type_option["title"] = f"Type: {type_name.capitalize()}"
                        new_anyOf.append(type_option)

                # Update the anyOf with cleaned up and titled options
                value["anyOf"] = new_anyOf
                if len(value["anyOf"]) == 1:
                    # If only one type remains, replace anyOf with the type directly
                    schema["properties"][key] = value["anyOf"][0]

            # Recursively process nested objects
            if value.get("type") == "object":
                format_any_of_schema(value)

    # Process definitions recursively
    if "definitions" in schema:
        for definition in schema["definitions"].values():
            format_any_of_schema(definition)

    return schema


def transform_json_to_ui_schema(json_schema):
    elements = []
    for prop_name, prop_details in json_schema.get("properties", {}).items():
        ui_element = {"type": "Control", "scope": f"#/properties/{prop_name}"}
        # Customize further based on prop_details like type or format
        if "enum" in prop_details:
            ui_element["options"] = {"format": "dropdown"}
        elements.append(ui_element)

    return {"type": "VerticalLayout", "elements": elements}


async def get_param_settings(module_name: str, version: str, module_bucket_name: str):
    """
    This method gets parameter settings from the bucket
    allocated for a module (e.g. xt-modules-repository).
    Converts the list of parameter definitions into
    a Pydantic model, where each field of the model is a parameter
    on the list and it's value type is also parsed from the parameter definition
    in the yaml file.

    :param module_name: name of the module
    :type module_name: str
    :param version: the version of the module for
    :type version: str
    :param module_bucket_name:the name of the bucket where the
    module's parameter settings file is stored.
    :type module_bucket_name: str
    :return: The function `get_param_settings` returns four values in a tuple:
    1. `params_settings`: An instance of the `ParameterSettings` class populated with data from the YAML
    file.
    2. `class_reg`: A dictionary containing registered classes for input parameter value mappings.
    3. `json_schema`: A JSON schema generated from the input parameter values schema.
    4. `ui_schema`: A UI schema transformed
    """

    storage_client = get_storage_client()

    check_paths = [
        f"{module_name}/{version}/params_settings.yaml",
        f"{module_name}/params_settings.yaml",
    ]

    for p in check_paths:
        f = await storage_client.get_file(module_bucket_name, file_path=p)
        if f:
            data = yaml.safe_load(f.read().decode("utf-8"))
            params_settings = ParameterSettings(**data)

            class_reg = params_settings.populate_input_param_vals()

            InputParameterValue = class_reg.get("InputParameterValue")

            json_schema = format_any_of_schema(InputParameterValue.schema())
            ui_schema = transform_json_to_ui_schema(json_schema)

            return params_settings, class_reg, json_schema, ui_schema

    raise NotFoundError(detail="Parameter settings not found for this module.")
