# Helper functions to call OpenAI Assistant

from datetime import datetime
import json
import asyncio
from typing import Dict, List
import logging
import os

from openai import  AsyncOpenAI
from pydantic import BaseModel
from fastapi import HTTPException
from openai import LengthFinishReasonError, OpenAI, OpenAIError
import csv


from .agent_tools import GLOBAL_DATA_MODELS, GLOBAL_TOOLS_FUNCTIONS, get_file_content_from_googledrive_by_name, write_content_to_googledrive
from .tools_json import GLOBAL_ASSISTANT_TOOLS
from .openapi_spec_to_tools import (
    OPENAPI_TOOL_CONFIGURATIONS,
    OPENAPI_GLOBAL_ASSISTANT_TOOLS,
    OPENAPI_CALLABALE_FUNCTIONS,
)
from collections.abc import Iterable


async def read_from_google_drive(path):
    return await get_file_content_from_googledrive_by_name(file_name=path)

# Function to get headers for OpenAPI tools
def get_headers(toolname):
    headers = OPENAPI_TOOL_CONFIGURATIONS.get(toolname, {}).get("headers", {})
    return headers


def get_params(toolname):
    params = OPENAPI_TOOL_CONFIGURATIONS.get(toolname, {}).get("params", {})
    return params


async def run_assistant(client, assistant, thread, prompt, response_type, allowed_tools):
    """
    Runs the assistant with the given parameters.
    """
    await send_initial_message(client, thread, prompt)
    allowed_tool_items = get_allowed_tool_items(allowed_tools)
    response_format = get_response_format(response_type)

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        response_format=response_format,
        tools=allowed_tool_items,
    )

    max_iterations = 5
    iteration_count = 0

    while run.status == 'requires_action':
        if iteration_count >= max_iterations:
            logging.info("Exceeded maximum number of iterations for requires_action.")
            # Cancel the run before returning
            await client.beta.threads.runs.cancel(run_id=run.id)
            return "Error: Exceeded maximum number of iterations for requires_action."

        tool_outputs = await handle_required_action(run)
        if tool_outputs:
            run = await submit_tool_outputs(client, thread, run, tool_outputs)

        iteration_count += 1

    return await handle_run_completion(client, thread, run)



async def send_initial_message(client, thread, prompt):
    await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )


def get_allowed_tool_items(allowed_tools):
    allowed_tool_items = [
        tool for tool in GLOBAL_ASSISTANT_TOOLS
        if tool['type'] == 'function' and tool['function']['name'] in allowed_tools
    ]
    allowed_tool_items.extend([
        tool for tool in OPENAPI_GLOBAL_ASSISTANT_TOOLS
        if tool['type'] == 'function' and tool['function']['name'] in allowed_tools
    ])
    return allowed_tool_items


def get_response_format(response_type):
    return {
        'type': 'json_schema',
        'json_schema': {
            "name": response_type.__name__,
            "schema": response_type.model_json_schema()
        }
    }


async def handle_required_action(run):
    tool_outputs = []
    current_batch_size = 0
    max_batch_size = 256 * 1024  # 256 KB
    logging.info(f"Handling required action")

    if hasattr(run, 'required_action') and hasattr(run.required_action, 'submit_tool_outputs'):
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            function, openai_function = get_function(tool.function.name)
            if function:
                output_str, output_size = await invoke_function(function, tool, openai_function)
                if current_batch_size + output_size > max_batch_size:
                    tool_outputs.append(
                        {"tool_call_id": tool.id, "output": ""})
                else:
                    tool_outputs.append(
                        {"tool_call_id": tool.id, "output": output_str})
                    current_batch_size += output_size
            else:
                logging.info(f"Function {tool.function.name} not found.")
                tool_outputs.append(
                    {"tool_call_id": tool.id, "output": "No results found"})

    return tool_outputs


def get_function(function_name):
    function = GLOBAL_TOOLS_FUNCTIONS.get(function_name)
    openai_function = False
    if not function:
        function = OPENAPI_CALLABALE_FUNCTIONS.get(function_name)
        openai_function = True
    return function, openai_function


async def invoke_function(function, tool, openai_function):
    try:
        function_args = json.loads(tool.function.arguments)
        logging.info(f"Invoking function {tool.function.name} with args: {function_args}\n")
              
        if openai_function:
            output = await invoke_openapi_function(function, function_args, tool.function.name)
        else:
            if asyncio.iscoroutinefunction(function):
                output = await function(**function_args)
            else:
                output = function(**function_args)
        output_str = json.dumps(output)
        output_size = len(output_str.encode('utf-8'))
        logging.info(f"\nOutput from function {tool.function.name}: {output_str[:256]}\n")
              
        return output_str, output_size
    except Exception as e:
        logging.info(f"invoke_function Error invoking function {tool.function.name}: {e}")
        return "No results found", 0


async def invoke_openapi_function(function, function_args, function_name):

    json_body = function_args.get("json", None)
    path_params = function_args.get("path_params", None)
    fn_args = {"path_params": path_params, "data": json_body}
    headers = get_headers(function_name)

    query_params = function_args.get("params", {})
    params = get_params(function_name)
    query_params.update(params)
    status, reason, text = await function(
        name=function_name,
        fn_args=fn_args,
        headers=headers,
        params=query_params,
    )
    logging.info(f"\nOutput from function {function_name}: {status} {reason}\n")
    return {
        "status_code": status,
        "text": text,
        "reason": reason,
    }


async def submit_tool_outputs(client, thread, run, tool_outputs):
    try:
        return await client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    except Exception as e:
        logging.info("Failed to submit tool outputs:", e)
        return run


async def handle_run_completion(client, thread, run):
    if run.status == 'completed':
        messages = await client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
    else:
        logging.info("Failed to run assistant:", run.status)
        return run.status


async def extract_and_structure_data(client, assistant, thread, prompt, task_inputs, response_type, allowed_tools):
    # Replace placeholders in the prompt with task inputs
    formatted_prompt = prompt
    for key, value in task_inputs.items():
        placeholder = "{{ inputs." + key + " }}"
        formatted_prompt = formatted_prompt.replace(placeholder, str(value))
    output = await run_assistant(client, assistant, thread, formatted_prompt, response_type, allowed_tools)
    return output

class RowItem(BaseModel):
    column_value: str
    
class ResponseList(BaseModel):
    rows: List[RowItem]
    
def lookup_response_type(name: str):
    for model in GLOBAL_DATA_MODELS:
        if model.__name__ == name:
            return model
    return ResponseList  # Default response type


async def process_agent_request(row_batch: List[Dict], workflow: Dict, custom_instructions: str) -> List[Dict]:
    """
    Process agent request using the OpenAI client.
    """
    try:
        client = AsyncOpenAI()
        assistant = await client.beta.assistants.create(
            name="AI Assistant",
            instructions=f"Hi, You are an AI Assistant. Help the user with their tasks.\n\n{custom_instructions}\n\n",   
            tools=[],
            model="gpt-4o-2024-08-06"
        )
        thread = await client.beta.threads.create()
        parsed_outputs = []
        task_outputs = {}  # Dictionary to store outputs of tasks
        input_list = {}
        input_list['initial_input_list'] = {
            "data": row_batch,
            "format": "list"
            }
        task_outputs['initial_input'] = input_list
        for task in workflow['tasks']:
            # Process each task
            task_outputs = await process_task(client, assistant, thread, task, task_outputs)
        # Collect the final output
        parsed_outputs.append(task_outputs)
        return parsed_outputs
    except Exception as e:
        logging.info(f"process_agent_request process_agent_request An error occurred: {e}")
        return "Error Processing Leads"
    finally:
        try:
            await client.beta.assistants.delete(assistant.id)
        except Exception as e:
            logging.info(f"Error deleting assistant: {e}")


async def process_task(client, assistant, thread, task, task_outputs):
    """
    Process a single task in the workflow.
    """
    # Prepare inputs
    task_inputs = await prepare_task_inputs(task, task_outputs)

    # Run the operation
    output = await run_task_operation(client, assistant, thread, task, task_inputs)

    # Store outputs
    await store_task_outputs(task, output, task_outputs)

    return task_outputs

async def read_csv_rows(file_path):
    rows = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            rows.append(row)
    return rows

async def prepare_task_inputs(task, task_outputs):
    """
    Prepare the inputs for a task based on its input specifications.
    """
    inputs = task.get('inputs', {})
    task_inputs = {}
    for input_name, input_spec in inputs.items():
        source = input_spec.get('source', {})
        source_type = source.get('type', '')
        format = input_spec.get('format', 'list')
        if source_type == 'inline':
            # Get from inline source
            input_data = source.get('data')
        elif source_type == 'task_output':
            # Get from previous task output
            task_id = source.get('task_id')
            output_key = source.get('output_key')
            previous_task_output = task_outputs.get(task_id, {})            
            if isinstance(previous_task_output, dict):
                output_item = previous_task_output.get(output_key)
                input_data = output_item['data']
            else:
                input_data = previous_task_output
        
            # Ensure input_data is a list
            if not isinstance(input_data, list):
                input_data = [input_data]
        elif source_type == 'google_drive':
            # Handle Google Drive source
            path = source.get('location')
            input_data_path = await read_from_google_drive(path)
            input_data = await read_csv_rows(input_data_path)
        elif source_type == 'local_path':
            # Handle local path source
            input_data_path = source.get('location')
            input_data = await read_csv_rows(input_data_path)
        else:
            input_data = None
        if input_data:
            task_inputs[input_name] = { 
                                        "format": format, 
                                        "data" : input_data
            }
    return task_inputs

async def run_task_operation(client, assistant, thread, task, task_inputs):
    """
    Execute the operation defined in the task.
    """
    operation = task.get('operation', {})
    operation_type = operation.get('type', '')
    allowed_tools = operation.get('allowed_tools', [])
    response_type_name = operation.get('response_type', 'ResponseList')
    response_type = lookup_response_type(response_type_name)
    outputs = []
    
    if operation_type == 'ai_assistant_call':
        prompt_template = operation.get('prompt', '')
        args = operation.get('args', [])
        # Prepare prompt by substituting inputs
        
        
        for key, value in task_inputs.items():
            format = value.get('format', 'list')
            if format == 'list':
                items = value.get('data')
                for item in items:
                    formatted_prompt = prompt_template
                    formatted_prompt = formatted_prompt.replace(
                        "{{ inputs." + key + " }}", json.dumps(item))
                    # Run assistant with prompt
                    logging.info(formatted_prompt)                    
                    output = await extract_and_structure_data(
                        client, assistant, thread, formatted_prompt, task_inputs, response_type, allowed_tools)
                    
                    if isinstance(output, str):
                        try:
                            output_json = json.loads(output)
                        except json.JSONDecodeError:
                            pass
                                                            
                    if output_json and isinstance(output_json, dict) and 'data' in output_json and isinstance(output_json['data'], list):
                        for item in output_json['data']:
                            outputs.append(json.dumps(item))
                    else:
                        outputs.append(output)
                        interim_return_val = {
                            "data": outputs,
                            "format": "list"
                        }
                        await store_task_outputs_interim_checkpoint(task, interim_return_val, task_inputs)
            else:
                pass # TODO: Handle other formats    
    elif operation_type == 'python_callable':
            function_name = operation.get('function', '')
            args = operation.get('args', [])
            function = GLOBAL_TOOLS_FUNCTIONS.get(function_name)
            if function is None:
                raise Exception(f"Function {function_name} not found.")
            # Prepare function arguments
            function_args = [task_inputs.get(arg, {}).get("data") for arg in args]            
            if asyncio.iscoroutinefunction(function):
                output = await function(*function_args)
            else:
                output = function(*function_args)
            # If output is an iterable (but not a string or bytes), extend outputs with it
            if isinstance(output, Iterable) and not isinstance(output, (str, bytes)):
                outputs.extend(output)
            else:
                outputs.append(output)
    else:
        # Handle other operation types
        output = None
    return_val = {
        "data": outputs,
        "format": "list"
    }
    return return_val

async def store_task_outputs_interim_checkpoint(task, output, task_outputs):
    """
    Store the outputs of a task for use in subsequent tasks.
    """
    outputs = task.get('outputs', {})
    if outputs:
        for output_name, output_spec in outputs.items():
            destination = output_spec.get('destination', {})
            if destination:
                dest_type = destination.get('type')
                path_template = destination.get('path_template')
                if path_template:
                    current_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    current_timestamp = '_interim'
                    path = path_template.replace('{timestamp}', current_timestamp)
                    path = path.replace('{task_id}', task['id'])
                    local_path = path

                    if dest_type == 'google_drive':
                        local_path = os.path.join('/tmp', task['id'], path)

                    if dest_type == 'google_drive' or dest_type == 'local_path':
                        directory = os.path.dirname(local_path)
                        if directory and not os.path.exists(directory):
                            os.makedirs(directory)
                        logging.info(f"Writing output to {local_path}\n")

                        if output.get("format", "") == 'list':
                            data_list = [json.loads(item) for item in output.get("data", [])]
                            # Write the full list first with a 'full_list' prefix
                            def get_prefixed_path(file_path, prefix):
                                directory, filename = os.path.split(file_path)
                                name, ext = os.path.splitext(filename)
                                prefixed_filename = f"{prefix}_{name}{ext}"
                                return os.path.join(directory, prefixed_filename)

                            full_list_local_path = get_prefixed_path(local_path, 'full_list')
                            full_list_directory = os.path.dirname(full_list_local_path)
                            if full_list_directory and not os.path.exists(full_list_directory):
                                os.makedirs(full_list_directory)
                            logging.info(f"Writing full list output to {full_list_local_path}\n")

                            with open(full_list_local_path, 'w') as full_file:
                                if data_list:
                                    headers = [key for key, value in data_list[0].items() if isinstance(value, (str, int, float, bool))]
                                    writer = csv.DictWriter(full_file, fieldnames=headers)
                                    writer.writeheader()
                                    for data in data_list:
                                        filtered_data = {key: value for key, value in data.items() if key in headers}
                                        writer.writerow(filtered_data)
                                else:
                                    writer = csv.DictWriter(full_file, fieldnames=[])
                                    writer.writeheader()
    return task_outputs

def filter_data_list(data_list, filter_by):
    """
    Filter the data_list based on conditions specified in filter_by.
    Supported operators: 'gt', 'lt', 'eq', 'gte', 'lte', 'ne'
    """
    from operator import gt, lt, eq, ge, le, ne

    operator_map = {
        'gt': gt,
        'lt': lt,
        'eq': eq,
        'gte': ge,
        'lte': le,
        'ne': ne
    }

    filtered_list = []
    for item in data_list:
        include_item = True
        for property_name, conditions in filter_by.items():
            value = item.get(property_name)
            if value is None or (isinstance(value, str) and value.strip() == ""):
                include_item = False
                break
            for op, compare_value in conditions.items():
                op_func = operator_map.get(op)
                if op_func is None:
                    continue  # Unsupported operator
                try:
                    # Convert values to float for comparison if possible
                    item_value = float(value)
                    compare_value = float(compare_value)
                except (ValueError, TypeError):
                    item_value = value
                if not op_func(item_value, compare_value):
                    include_item = False
                    break
            if not include_item:
                break
        if include_item:
            filtered_list.append(item)
    return filtered_list

def convert_value(value):
    """
    Convert the value to the appropriate type for sorting.
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return ""
    try:
        return float(value)
    except ValueError:
        pass
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        pass
    return str(value)

def filter_and_sort(data_list, output_spec):
    """
    Filter and sort the data_list based on the output_spec.
    """
    required_properties = output_spec.get('required_properties', [])
    if required_properties:
        data_list = remove_empty_property_rows(data_list, required_properties)
    
    dedup_by = output_spec.get('deduplication_properties', [])
    if dedup_by:
        data_list = deduplicate_list_by_properties(data_list, dedup_by)
    
    sort_by_asc = output_spec.get('sort_by_asc', [])
    sort_by_desc = output_spec.get('sort_by_desc', [])
    
    # Combine sort fields with their corresponding order
    sort_fields = [(key, True) for key in sort_by_asc] + [(key, False) for key in sort_by_desc]
    logging.info(f"Sorting by: {sort_fields}")
    
    # Sort from least significant to most significant key
    for key, ascending in reversed(sort_fields):
        data_list = sorted(
            data_list,
            key=lambda x: convert_value(x.get(key)),
            reverse=not ascending
        )
    
    filter_by = output_spec.get('filter_by', {})
    if filter_by:
        data_list = filter_data_list(data_list, filter_by)
    
    return data_list

# Example usage within the original function
async def store_task_outputs(task, output, task_outputs):
    """
    Store the outputs of a task for use in subsequent tasks.
    """
    outputs = task.get('outputs', {})
    if outputs:
        for output_name, output_spec in outputs.items():
            # Store output in task_outputs using task id and output_name
            if task['id'] not in task_outputs:
                task_outputs[task['id']] = {}

            destination = output_spec.get('destination', {})
            if destination:
                dest_type = destination.get('type')
                path_template = destination.get('path_template')
                if path_template:
                    current_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    path = path_template.replace('{timestamp}', current_timestamp)
                    path = path.replace('{task_id}', task['id'])
                    local_path = path

                    if dest_type == 'google_drive':
                        local_path = os.path.join('/tmp', task['id'], path)

                    if dest_type == 'google_drive' or dest_type == 'local_path':
                        directory = os.path.dirname(local_path)
                        if directory and not os.path.exists(directory):
                            os.makedirs(directory)
                        logging.info(f"Writing output to {local_path}\n")

                        if output.get("format", "") == 'list':
                            data_list = [json.loads(item) for item in output.get("data", [])]
                            logging.info(f"Total count: {len(data_list)}")

                            # Write the full list first with a 'full_list' prefix
                            def get_prefixed_path(file_path, prefix):
                                directory, filename = os.path.split(file_path)
                                name, ext = os.path.splitext(filename)
                                prefixed_filename = f"{prefix}_{name}{ext}"
                                return os.path.join(directory, prefixed_filename)

                            full_list_local_path = get_prefixed_path(local_path, 'full_list')
                            full_list_directory = os.path.dirname(full_list_local_path)
                            if full_list_directory and not os.path.exists(full_list_directory):
                                os.makedirs(full_list_directory)
                            logging.info(f"Writing full list output to {full_list_local_path}\n")

                            with open(full_list_local_path, 'w') as full_file:
                                if data_list:
                                    headers = [key for key, value in data_list[0].items() if isinstance(value, (str, int, float, bool))]
                                    writer = csv.DictWriter(full_file, fieldnames=headers)
                                    writer.writeheader()
                                    for data in data_list:
                                        filtered_data = {key: value for key, value in data.items() if key in headers}
                                        writer.writerow(filtered_data)
                                else:
                                    writer = csv.DictWriter(full_file, fieldnames=[])
                                    writer.writeheader()

                            if data_list:
                                data_list = filter_and_sort(data_list, output_spec)
                                
                                logging.info(f"Deduped and removed count: {len(data_list)}")
                                headers = [key for key, value in data_list[0].items() if isinstance(value, (str, int, float, bool))]
                                with open(local_path, 'w') as file:
                                    writer = csv.DictWriter(file, fieldnames=headers)
                                    writer.writeheader()
                                    for data in data_list:
                                        filtered_data = {key: value for key, value in data.items() if key in headers}
                                        writer.writerow(filtered_data)
                            else:
                                with open(local_path, 'w') as file:
                                    writer = csv.DictWriter(file, fieldnames=[])
                                    writer.writeheader()
                        else:
                            with open(local_path, 'w') as file:
                                file.write(str(output))
                    else:
                        pass
                if dest_type == 'google_drive':
                    await write_to_google_drive(path, local_path)

                task_outputs[task['id']][output_name] = output
    else:
        task_outputs[task['id']] = output
def remove_empty_property_rows(data_list, properties):
    """
    Remove rows with None or empty values for the specified properties.
    """
    filtered_list = []
    for item in data_list:
        empty = False
        for property_name in properties:
            value = item.get(property_name)
            if value is None or (isinstance(value, str) and value.strip() == ""):
                empty = True
                break
        if not empty:
            filtered_list.append(item)
    return filtered_list

def deduplicate_list_by_properties(data_list, properties):
    """
    Deduplicate a list of dictionaries by a list of properties in order.
    Only deduplicate if the property value is not None or empty, strip spaces, and compare in lowercase.
    """
    for property_name in properties:
        seen = set()
        deduplicated_list = []
        for item in data_list:
            value = item.get(property_name)
            value = str(value or "").strip().lower()
            if value == "":
                deduplicated_list.append(item)
            elif value not in seen:
                seen.add(value)
                deduplicated_list.append(item)
        data_list = deduplicated_list
    return data_list

async def write_to_google_drive(cloud_path, local_path):
    # Placeholder function for writing to Google Drive
    await write_content_to_googledrive(cloud_path, local_path)
    logging.info(f"Writing to Google Drive at {cloud_path} {local_path}")

async def get_structured_output(message: str, response_type):
    try:
        client = AsyncOpenAI()
        completion = await client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Extract structured content from input. Output is in JSON Format."},
                {"role": "user", "content": message},
            ],
            response_format=response_type,
        )

        response = completion.choices[0].message
        if response.parsed:
            return response.parsed, 'SUCCESS'
        elif response.refusal:
            logging.warning("ERROR: Refusal response: %s", response.refusal)
            return response.refusal, 'FAIL'
        
    except LengthFinishReasonError as e:
        logging.error(f"Too many tokens: {e}")
        raise HTTPException(status_code=502, detail="The request exceeded the maximum token limit.")
    except OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=502, detail="Error communicating with the OpenAI API.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing your request.")