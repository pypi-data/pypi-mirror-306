GLOBAL_ASSISTANT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_html_content_from_url",
            "description": "Retrieve the HTML content from a given URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the webpage to fetch."
                    }
                },
                "required": ["url"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_content_from_googledrive_by_name",
            "description": "Searches for a file by name in Google Drive using a service account, downloads it, saves it with a unique filename, and returns the local file path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file to search for and download from Google Drive."
                    }
                },
                "required": ["file_name"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_dataframes",
            "description": "Query multiple dataframes based on a user query and write the output dataframe to a specified output file path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_query": {
                        "type": "string",
                        "description": "User query in natural language. This will be converted to pandas query syntax."
                    },
                    "input_files": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Optional list of paths to CSV files to be loaded into dataframes. If not specified, default files will be used."
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "Optional path to the output file where the resulting dataframe will be saved. If not specified, a unique file path will be generated in '/tmp/run_interim_outputs/'."
                    }
                },
                "required": ["user_query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email_using_service_account",
            "description": "Sends an email using the Gmail API with a service account. The service account must have domain-wide delegation to impersonate the sender.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sender": {
                        "type": "string",
                        "description": "The email address of the sender (must be a user in the domain)."
                    },
                    "recipient": {
                        "type": "string",
                        "description": "The email address of the recipient."
                    },
                    "subject": {
                        "type": "string",
                        "description": "The subject of the email."
                    },
                    "body": {
                        "type": "string",
                        "description": "The body text of the email."
                    }
                },
                "required": ["sender", "recipient", "subject", "body"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_calendar_events_using_service_account",
            "description": "Retrieves a list of events from a user's Google Calendar using a service account. Events are filtered based on the provided start and end date range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_email": {
                        "type": "string",
                        "description": "The email address of the user whose calendar events are to be retrieved."
                    },
                    "start_date": {
                        "type": "string",
                        "description": "The start date (inclusive) to filter events. Format: 'YYYY-MM-DD'."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date (exclusive) to filter events. Format: 'YYYY-MM-DD'."
                    }
                },
                "required": ["user_email", "start_date", "end_date"],
                "additionalProperties": False
            }
        }
    }
]
