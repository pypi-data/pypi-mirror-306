import pytest

from nest_gen_accelerator_azure.components.output_parsers import JsonOutputParser
from nest_gen_accelerator_azure.components.outputs import ExitStrategy
from nest_gen_accelerator_azure.components.outputs.llm_response import LLMResponse


@pytest.fixture
def valid_llm_response():
    return {
        "choices": [
            {
                "message": {
                    "content": '{"content": "Do you know where my orders FR6A0889826 and FR6A0898073 are?", "callToAction": {"type": "NONE"}, "exitStrategy": ""}'
                }
            }
        ],
        "model": "test-model",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
        "params": {
            "seed": 42
        }
    }


@pytest.fixture
def handover_response():
    return {
        "choices": [
            {
                "message": {
                    "content": '{"content": "Can I talk to an agent?", "callToAction": {"type": "TO_LIVE_AGENT", "value": true}, "exitStrategy": ""}'
                }
            }
        ],
        "model": "test-model",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
        "params": {}
    }


@pytest.fixture
def invalid_llm_response():
    return {
        "choices": [],
        "model": "test-model",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
        "params": None
    }


def test_from_json_valid_response(valid_llm_response):
    tracking_id = "test-tracking-id"
    response = LLMResponse.from_json(valid_llm_response, tracking_id)

    assert (
        response.content
        == "Do you know where my orders FR6A0889826 and FR6A0898073 are?"
    )
    assert response.call_to_action.type == "NONE"
    assert response.exit_strategy == ExitStrategy.EMPTY
    assert response.model_details["name"] == "test-model"
    assert response.model_details["total_tokens"] == 30


def test_from_json_invalid_response(invalid_llm_response):
    tracking_id = "test-tracking-id"
    response = LLMResponse.from_json(invalid_llm_response, tracking_id)

    assert response.content == ""
    assert response.call_to_action.type == "NONE"
    assert response.exit_strategy == ExitStrategy.ON_ERROR
    assert response.model_details["name"] == "test-model"
    assert response.model_details["total_tokens"] == 30


def test_from_json_parsing_error(mocker, valid_llm_response):
    tracking_id = "test-tracking-id"
    mocker.patch.object(
        JsonOutputParser, "parse", side_effect=ValueError("Parsing error")
    )

    response = LLMResponse.from_json(valid_llm_response, tracking_id)

    assert response.content == ""
    assert response.call_to_action.type == "NONE"
    assert response.exit_strategy == ExitStrategy.ON_ERROR
    assert response.model_details["name"] == "test-model"
    assert response.model_details["total_tokens"] == 30


def test_from_json_handover_response(handover_response):
    tracking_id = "test-tracking-id"
    response = LLMResponse.from_json(handover_response, tracking_id)

    assert response.content == "Can I talk to an agent?"
    assert response.call_to_action.type == "TO_LIVE_AGENT"
    assert response.call_to_action.value is True
    assert response.exit_strategy == ExitStrategy.EMPTY
    assert response.model_details["name"] == "test-model"
    assert response.model_details["total_tokens"] == 30
