import pytest

from promptflow.connections import CustomConnection
from nest_gen_accelerator_azure.tools.llm_tool import llm_tool


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    return CustomConnection(
        {
            "client_id": "my-client-id",
            "client_secret": "my-client-secret",
        },
        {
            "endpoint": "my-endpoint",
        },
    )


@pytest.fixture
def my_llm_mock_response():
    return {
        "usage": {"total_tokens": 42},
        "choices": [{"message": {"content": "This is a mock response"}}],
    }


def test_llm_tool(mocker, my_custom_connection, my_llm_mock_response):
    mock_requests_post = mocker.patch(
        "nest_gen_accelerator_azure.tools.llm_tool.requests.post"
    )
    mock_requests_post.return_value.json.return_value = my_llm_mock_response
    mock_requests_post.return_value.status_code = 200

    result = llm_tool(my_custom_connection, rendered_prompt="user:\nThis is a test")
    assert result["usage"]["total_tokens"] > 0
    assert result["choices"][0]["message"]["content"] == "This is a mock response"
