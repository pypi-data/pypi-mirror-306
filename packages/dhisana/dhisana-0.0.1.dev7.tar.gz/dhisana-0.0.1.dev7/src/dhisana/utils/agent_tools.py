# Global List of tools that can be used in the assistant
# Only functions marked with @assistant_tool will be available in the allowed list
# This is in addition to the tools from OpenAPI Spec add to allowed tools

import os
import json
import uuid
import io
import base64
import csv
import logging
from typing import List, Dict, Any, Optional

import pandas as pd
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from pydantic import BaseModel
from fastapi import HTTPException
from openai import LengthFinishReasonError, OpenAI, OpenAIError, AsyncOpenAI
from typing import List, Optional
import tempfile
import pandas as pd
from typing import List, Optional
import time



from dhisana.utils.assistant_tool_tag import assistant_tool
GLOBAL_DATA_MODELS = []
GLOBAL_TOOLS_FUNCTIONS = {}

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

@assistant_tool
async def get_html_content_from_url(url):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        logging.info(f"Requesting {url}")
        try:
            await page.goto(url, timeout=10000)
            html_content = await page.content()
            return await parse_html_content(html_content)
        except Exception as e:
            logging.info(f"Failed to fetch {url}: {e}")
            return ""
        finally:
            await browser.close()


async def parse_html_content(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style']):
        element.decompose()
    return soup.get_text(separator=' ', strip=True)


def convert_base_64_json(base64_string):
    """
    Convert a base64 encoded string to a JSON string.

    Args:
        base64_string (str): The base64 encoded string.

    Returns:
        str: The decoded JSON string.
    """
    # Decode the base64 string to bytes
    decoded_bytes = base64.b64decode(base64_string)

    # Convert bytes to JSON string
    json_string = decoded_bytes.decode('utf-8')

    return json_string


@assistant_tool
async def get_file_content_from_googledrive_by_name(file_name: str = None) -> str:
    """
    Searches for a file by name in Google Drive using a service account, downloads it, 
    saves it in /tmp with a unique filename, and returns the local file path.

    :param file_name: The name of the file to search for and download from Google Drive.
    :return: Local file path of the downloaded file.
    """
    # Retrieve the service account JSON and email for automation from environment variables
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required scope for Google Drive API access
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Authenticate using the service account info and impersonate the specific email
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Build the Google Drive service object
    service = build('drive', 'v3', credentials=credentials)

    # Search for the file by name
    query = f"name = '{file_name}'"
    results = service.files().list(q=query, pageSize=1,
                                   fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        raise FileNotFoundError(f"No file found with the name: {file_name}")

    # Get the file ID of the first matching file
    file_id = items[0]['id']
    file_name = items[0]['name']

    # Create a unique filename by appending a UUID to the original file name
    unique_filename = f"{uuid.uuid4()}_{file_name}"

    # Path to save the downloaded file
    local_file_path = os.path.join('/tmp', unique_filename)

    # Request the file content from Google Drive
    request = service.files().get_media(fileId=file_id)

    # Create a file-like object in memory to hold the downloaded data
    fh = io.FileIO(local_file_path, 'wb')

    # Initialize the downloader
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        logging.info(f"{file_name} Download {int(status.progress() * 100)}%.")

    # Close the file handle
    fh.close()

    # Return the local file path
    return local_file_path


@assistant_tool
async def write_content_to_googledrive(cloud_file_path: str, local_file_path: str) -> str:
    try:
        """
        Writes content from a local file to a file in Google Drive using a service account.
        If the file does not exist in Google Drive, it creates it along with any necessary intermediate directories.
        
        :param cloud_file_path: The path of the file to create or update on Google Drive.
        :param local_file_path: The path to the local file whose content will be uploaded.
        :return: The file ID of the uploaded or updated file.
        """

        # Retrieve the service account JSON and email for automation from environment variables
        email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')
        service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
        service_account_json = convert_base_64_json(service_account_base64)

        # Parse the JSON string into a dictionary
        service_account_info = json.loads(service_account_json)

        # Define the required scope for Google Drive API access
        SCOPES = ['https://www.googleapis.com/auth/drive']

        # Authenticate using the service account info and impersonate the specific email
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
        ).with_subject(email_for_automation)

        # Build the Google Drive service object
        service = build('drive', 'v3', credentials=credentials)

        # Split the cloud file path into components
        path_components = cloud_file_path.split('/')
        parent_id = 'root'
        
        # Create intermediate directories if they don't exist
        for component in path_components[:-1]:
            query = f"'{parent_id}' in parents and name = '{component}' and mimeType = 'application/vnd.google-apps.folder'"
            results = service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
            items = results.get('files', [])
            
            if items:
                parent_id = items[0]['id']
            else:
                file_metadata = {
                    'name': component,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [parent_id]
                }
                folder = service.files().create(body=file_metadata, fields='id').execute()
                parent_id = folder.get('id')

        # Prepare the file for upload
        media_body = MediaFileUpload(local_file_path, resumable=True)
        file_name = path_components[-1]

        # Check if the file exists in the specified directory
        query = f"'{parent_id}' in parents and name = '{file_name}'"
        results = service.files().list(q=query, pageSize=1, fields="files(id, name)").execute()
        items = results.get('files', [])

        if items:
            # File exists, update its content
            file_id = items[0]['id']
            updated_file = service.files().update(
                fileId=file_id,
                media_body=media_body
            ).execute()
        else:
            # File does not exist, create a new one
            file_metadata = {
                'name': file_name,
                'parents': [parent_id]
            }
            created_file = service.files().create(
                body=file_metadata,
                media_body=media_body,
                fields='id'
            ).execute()
            file_id = created_file.get('id')
    except HttpError as error:
            raise Exception(f"list_files_in_drive_folder_by_name An error occurred: {error}")

    return file_id

@assistant_tool
async def list_files_in_drive_folder_by_name(folder_path: str = None) -> List[str]:
    """
    Lists all files in the given Google Drive folder by folder path.
    If no folder path is provided, it lists files in the root folder.

    :param folder_path: The path of the folder in Google Drive to list files from.
                        Example: '/manda_agent_metadata/openapi_tool_specs/'
    :return: A list of file names in the folder.
    :raises Exception: If any error occurs during the process.
    """
    # Retrieve the service account JSON and email for automation from environment variables
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required scope for Google Drive API access
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Authenticate using the service account info and impersonate the specific email
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Build the Google Drive service object
    service = build('drive', 'v3', credentials=credentials)

    folder_id = 'root'  # Start from root if folder_path is None

    if folder_path:
        # Split the folder path into individual folder names
        folder_names = [name for name in folder_path.strip(
            '/').split('/') if name]
        for folder_name in folder_names:
            # Search for the folder by name under the current folder_id
            query = (
                f"name = '{
                    folder_name}' and mimeType = 'application/vnd.google-apps.folder' "
                f"and '{folder_id}' in parents and trashed = false"
            )
            try:
                results = service.files().list(
                    q=query,
                    pageSize=1,
                    fields="files(id, name)"
                ).execute()
                items = results.get('files', [])
                if not items:
                    raise FileNotFoundError(
                        f"Folder '{folder_name}' not found under parent folder ID '{folder_id}'"                           
                    )
                # Update folder_id to the ID of the found folder
                folder_id = items[0]['id']
            except HttpError as error:
                raise Exception(f"list_files_in_drive_folder_by_name An error occurred: {error}")

    # Now folder_id is the ID of the desired folder
    # List all files in the specified folder
    query = f"'{folder_id}' in parents and trashed = false"
    try:
        results = service.files().list(
            q=query,
            pageSize=1000,
            fields="files(id, name)"
        ).execute()
        items = results.get('files', [])
        # Extract file names
        file_names = [item['name'] for item in items]
        return file_names
    except HttpError as error:
        raise Exception(f"list_files_in_drive_folder_by_name An error occurred while listing files: {error}")


@assistant_tool
async def send_email_using_service_account_async(
    recipient: str, subject: str, body: str
) -> str:
    """
    Asynchronously sends an email using the Gmail API with a service account.
    The service account must have domain-wide delegation to impersonate the sender.

    :param recipient: The email address of the recipient.
    :param subject: The subject of the email.
    :param body: The body text of the email.
    :return: The ID of the sent message.
    """
    # Retrieve the service account JSON and email for automation from environment variables
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')

    if not service_account_base64 or not email_for_automation:
        raise EnvironmentError("Required environment variables are not set.")

    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required scope for sending email via Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    # Authenticate using the service account info and impersonate the email for automation
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Refresh the token if necessary
    if not credentials.valid:
        request = Request()
        credentials.refresh(request)

    # Get the access token
    access_token = credentials.token

    # Define the Gmail API endpoint for sending messages
    gmail_api_url = 'https://gmail.googleapis.com/gmail/v1/users/me/messages/send'

    # Create the email message
    message = MIMEText(body)
    message['to'] = recipient
    message['from'] = email_for_automation
    message['subject'] = subject

    # Encode the message in base64url format
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Prepare the request payload
    payload = {
        'raw': raw_message
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(gmail_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        sent_message = response.json()

    # Return the message ID of the sent email
    return sent_message.get('id', 'No ID returned')


@assistant_tool
async def get_calendar_events_using_service_account_async(
    start_date: str, end_date: str
) -> List[Dict[str, Any]]:
    """
    Asynchronously retrieves a list of events from a user's Google Calendar using a service account.
    The service account must have domain-wide delegation to impersonate the user.
    Events are filtered based on the provided start and end date range.

    :param start_date: The start date (inclusive) to filter events. Format: 'YYYY-MM-DD'.
    :param end_date: The end date (exclusive) to filter events. Format: 'YYYY-MM-DD'.
    :return: A list of calendar events within the specified date range.
    """
    # Helper function to decode base64 JSON
    def convert_base_64_json(encoded_json: str) -> str:
        decoded_bytes = base64.b64decode(encoded_json)
        return decoded_bytes.decode('utf-8')

    # Retrieve the service account JSON and email for automation from environment variables
    email_for_automation = os.getenv('EMAIL_FOR_AUTOMATION')
    service_account_base64 = os.getenv('GOOGLE_SERVICE_KEY')

    if not email_for_automation or not service_account_base64:
        raise EnvironmentError("Required environment variables are not set.")

    service_account_json = convert_base_64_json(service_account_base64)

    # Parse the JSON string into a dictionary
    service_account_info = json.loads(service_account_json)

    # Define the required Google Calendar API scope
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Authenticate using the service account info and impersonate the email for automation
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    ).with_subject(email_for_automation)

    # Refresh the token if necessary
    if not credentials.valid:
        request = Request()
        credentials.refresh(request)

    # Get the access token
    access_token = credentials.token

    # Define the API endpoint
    calendar_api_url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'

    # Convert start and end dates to ISO 8601 format with time
    start_datetime = f'{start_date}T00:00:00Z'  # UTC format
    end_datetime = f'{end_date}T23:59:59Z'      # UTC format

    params = {
        'timeMin': start_datetime,
        'timeMax': end_datetime,
        'maxResults': 10,
        'singleEvents': True,
        'orderBy': 'startTime'
    }

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(calendar_api_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        events_result = response.json()

    events = events_result.get('items', [])

    if not events:
        logging.info('No upcoming events found within the specified range.')
    else:
        logging.info('Upcoming events:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            logging.info(f"{start} - {event.get('summary', 'No Title')}")

    return events

class FileItem:
    def __init__(self, file_path: str):
        self.file_path = file_path

class FileList:
    def __init__(self, files: List[FileItem]):
        self.files = files

class PandasQuery(BaseModel):
    pandas_query: str
    
    

@assistant_tool
async def query_dataframes(user_query: str, input_files: Optional[List[str]], output_file_path: Optional[str] = None) -> str:
    """
    Query multiple dataframes based on a user query and write the output dataframe to a specified output file path.

    Args:
        user_query (str): User query in natural language.
        input_files (List[str]): List of paths to CSV files to be loaded into dataframes.
        output_file_path (Optional[str]): Path to the output file where the resulting dataframe will be saved.
            If not specified, a unique file path will be generated in '/tmp/run_interim_outputs/'.

    Returns:
        str: A JSON string representing the FileList containing the path to the output file if created, otherwise an empty list.
    """
    max_retries = 3
    # Check if the list of CSV files or the user query is empty
    if not input_files or not user_query:
        # Return an empty FileList as JSON
        return json.dumps({"files": []})

    # If output_file_path is not specified, generate one
    if not output_file_path:
        output_folder = '/tmp/run_interim_outputs/'
        # Ensure output_folder exists
        os.makedirs(output_folder, exist_ok=True)
        # Generate a unique filename
        unique_number = int(time.time() * 1000)  # milliseconds since epoch
        output_file_name = f'query_dataframe_{unique_number}.csv'
        output_file_path = os.path.join(output_folder, output_file_name)
    else:
        # Ensure the directory exists
        output_folder = os.path.dirname(output_file_path)
        if output_folder:
            os.makedirs(output_folder, exist_ok=True)

    # Load CSV files into dataframes, skipping empty files
    data_frames = []
    df_names = []
    for idx, file in enumerate(input_files):
        # Check if the file is empty
        if os.path.getsize(file) == 0:
            # Skip empty files
            continue
        df = pd.read_csv(file)
        data_frames.append(df)
        df_name = f'df{idx+1}'
        df_names.append(df_name)

    # Check if any dataframes were loaded
    if not data_frames:
        # Return an empty FileList as JSON
        return json.dumps({"files": []})

    # Create a context with the dataframes and their schemas
    schema_info = ""
    for df_name, df in zip(df_names, data_frames):
        schema_info += f"DataFrame '{df_name}' columns: {', '.join(df.columns)}\n"

    # Initialize the error message as empty
    error_message = ""

    for attempt in range(max_retries):
        # Prepare the message
        message = f"""
        You are an expert data analyst. Given the following DataFrames and their schemas:

        {schema_info}

        Write a pandas query to answer the following question:

        \"\"\"{user_query}\"\"\"

        Your query should use the provided DataFrames ({', '.join(df_names)}) and produce a DataFrame named 'result_df'. Do not include any imports or explanations; only provide the pandas query code that assigns the result to 'result_df'.
        """
        if error_message:
            message += f"\nThe previous query returned the following error:\n{error_message}\nPlease fix the query."

        # Get structured output
        pandas_query_result, status = await get_structured_output(message, PandasQuery)
        if status == 'SUCCESS' and pandas_query_result and pandas_query_result.pandas_query:
            pandas_query = pandas_query_result.pandas_query
            # Execute the query safely
            local_vars = {name: df for name, df in zip(df_names, data_frames)}
            global_vars = {}
            try:
                exec(pandas_query, global_vars, local_vars)
                result_df = local_vars.get('result_df')
                if result_df is None:
                    raise ValueError("The query did not produce a DataFrame named 'result_df'.")
                # If execution is successful, break out of the loop
                break
            except Exception as e:
                # Capture the error message
                error_message = str(e)
                # If this was the last attempt, raise the error
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Error executing generated query after {max_retries} attempts: {error_message}")
                # Otherwise, continue to the next iteration
                continue
        else:
            # If unable to get a valid response, raise an error
            if attempt == max_retries - 1:
                raise RuntimeError("Failed to get a valid pandas query after multiple attempts.")
            continue

    # Write the resulting DataFrame to the output file
    result_df.to_csv(output_file_path, index=False)

    # Create FileList object
    file_list = FileList(files=[FileItem(file_path=output_file_path)])

    # Convert FileList to JSON
    def file_item_to_dict(file_item):
        return {"file_path": file_item.file_path}

    file_list_dict = {
        "files": [file_item_to_dict(file_item) for file_item in file_list.files]
    }
    file_list_json = json.dumps(file_list_dict, indent=2)
    return file_list_json

@assistant_tool
async def load_csv_file(input_file_path: str):
    with open(input_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
    
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
    
GLOBAL_TOOLS_FUNCTIONS = {name: func for name, func in globals().items(
) if callable(func) and getattr(func, 'is_assistant_tool', False)}


# import asyncio
# import os
# import pandas as pd

# async def test_query_dataframes():
#     # Setup: Create a temporary CSV file with sample data
#     input_csv_path = '/tmp/leads_gtm/scored_leads_test.csv'
#     output_csv_path = '/tmp/leads_gtm/totalled_score.csv'
#     sample_data = {
#         'job_title_match_score': [1, 2, 3],
#         'skill_relevance_match_score': [1, 2, 3],
#         'location_match_score': [1, 2, 3],
#         'education_history_match_score': [1, 2, 3],
#         'job_history_match_score': [1, 2, 3],
#         'company_match_score': [1, 2, 3],
#         'industry_match_score': [1, 2, 3],
#         'keywords_match_score': [1, 2, 3]
#     }
#     df = pd.DataFrame(sample_data)
#     df.to_csv(input_csv_path, index=False)

#     # Define the input parameters
#     input_csv_files = [input_csv_path]
#     user_query = "Sum the columns 'job_title_match_score', 'skill_relevance_match_score', 'location_match_score', 'education_history_match_score', 'job_history_match_score', 'company_match_score', 'industry_match_score', 'keywords_match_score' to create a new column 'aggregate_score'. Save the output to '/tmp/totalled_score.csv'."
#     output_file = output_csv_path

#     # Call the function
#     result = await query_dataframes(input_csv_files, user_query, output_file)

#     # Verify the output
#     assert os.path.exists(output_csv_path), "Output file was not created."
#     result_df = pd.read_csv(output_csv_path)
#     expected_aggregate_score = [8, 16, 24]
#     assert 'aggregate_score' in result_df.columns, "Column 'aggregate_score' not found in the output."
#     assert result_df['aggregate_score'].tolist() == expected_aggregate_score, "Aggregate scores do not match the expected values."

# async def main():
#     await test_query_dataframes()

# if __name__ == '__main__':
#     asyncio.run(main())
    