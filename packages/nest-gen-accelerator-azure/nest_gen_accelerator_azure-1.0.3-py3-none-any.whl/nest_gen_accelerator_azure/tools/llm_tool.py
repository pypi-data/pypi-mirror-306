import os
from typing import Optional

import requests
from jinja2 import Template
from promptflow.connections import CustomConnection
from promptflow.core import tool
from promptflow.tools.common import parse_chat


def get_connection_params(connection: CustomConnection):
    """
    Retrieve secrets and configuration needed for the connection.

    Args:
        connection: CustomConnection object.

    Returns:
        dict: Secrets and config dictionaries.
    """
    # Get params and configs from CustomConnection object
    secrets = {
        "client_id": connection.secrets["client_id"],
        "client_secret": connection.secrets["client_secret"],
    }

    configs = {
        "endpoint": connection.configs["endpoint"],  # actual endpoint
        "content_type": "application/json",
        "accept": "application/json",
    }
    return secrets, configs


def build_headers(secrets: dict, configs: dict):
    """
    Constructs the HTTP headers for the request.

    Args:
        secrets (dict): Dictionary containing secret values.
        configs (dict): Dictionary containing configuration values.

    Returns:
        dict: HTTP headers.
    """
    return {
        "Content-Type": configs["content_type"],
        "Accept": configs["accept"],
        "client_id": secrets["client_id"],
        "client_secret": secrets["client_secret"],
    }


def send_post_request(endpoint: str, headers: dict, payload: dict):
    """
    Sends a POST request to the specified endpoint.

    Args:
        endpoint (str): URL of the API endpoint.
        headers (dict): HTTP headers.
        payload (dict): Data payload for the request.

    Returns:
        dict: API response in JSON format, or None in case of error.
    """
    try:
        ORG_MIDDLE_CERT_PATH = os.getenv("ORG_MIDDLE_CERT_PATH")
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            verify=ORG_MIDDLE_CERT_PATH if ORG_MIDDLE_CERT_PATH else True,
        )
        response.raise_for_status()  # Raises error for HTTP codes >= 400
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {}


def extract_payload(prompt: Template, model_params: Optional[dict] = None):
    if not model_params:
        model_params = {}

    messages = parse_chat(prompt)
    return {"messages": messages, **model_params}


@tool
def llm_tool(
    connection: CustomConnection, rendered_prompt: Template, model_params: Optional[dict] = None
):
    try:
        """
        Tool to establish connection, send POST request, and return the API response.

        Args:
            connection: CustomConnection object.
            client_id: Client ID.
            payload: Data payload to be sent to the API.
            model_params: Model parameters to be sent to the API.

        Returns:
            dict: API response in JSON format.
        """
        # Get connection secrets and configurations
        secrets, configs = get_connection_params(connection)

        # Build headers using secrets and configs
        headers = build_headers(secrets, configs)

        # Retrieve the API endpoint from configs
        endpoint = configs["endpoint"]

        # Get payload input from prompt object
        payload = extract_payload(rendered_prompt, model_params)

        # Send the POST request and get the response
        response_json = send_post_request(endpoint, headers, payload)
        response_json.update({"params": model_params})

        return response_json

    except Exception as e:
        return {"error": str(e)}
