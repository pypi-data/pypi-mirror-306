# Given Any OpenAPI Spec convert it to a list of tools
# This will help write tools in a declarative way

import os
from .openapi_tool.convert_openai_spec_to_tool import openapi_spec_to_openai_fn
from .openapi_tool.openapi_tool import OpenAPISpec

# Parse the OpenAPI spec and convert it to a list of tools
# OpenAI tools input Tools will be in openapi_GLOBAL_ASSISTANT_TOOLS
# Callable functions will be in openapi_callable_functions. This is invoked with assistant tool callback API
OPENAPI_GLOBAL_ASSISTANT_TOOLS = []
OPENAPI_CALLABALE_FUNCTIONS = {}
OPENAPI_TOOL_CONFIGURATIONS = {}


def convert_spec_to_tools(file_path: str):
    # Open the file and load spec from there
    with open(file_path, 'r') as file:
        openapi_spec = file.read()
    spec = OpenAPISpec.from_text(openapi_spec)
    openai_fns, call_api_fn = openapi_spec_to_openai_fn(spec)
    return openai_fns, call_api_fn

# Parse and save the OpenAI Tools parsed and the corresponding callable functions


def add_openapi_spec_to_tools_list(file_path: str):
    openai_fns, call_api_fn = convert_spec_to_tools(file_path)
    if (len(openai_fns) > 0):
        OPENAPI_GLOBAL_ASSISTANT_TOOLS.extend(openai_fns)
        for fn in openai_fns:
            name = fn["function"]["name"]
            if name:
                OPENAPI_CALLABALE_FUNCTIONS[name] = call_api_fn
    return OPENAPI_GLOBAL_ASSISTANT_TOOLS
