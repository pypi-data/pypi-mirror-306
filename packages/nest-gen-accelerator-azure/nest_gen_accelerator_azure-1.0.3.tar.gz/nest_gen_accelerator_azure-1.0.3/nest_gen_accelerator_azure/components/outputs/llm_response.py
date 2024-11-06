import logging
from typing import Union

from nest_gen_accelerator_azure.components.output_parsers import JsonOutputParser
from nest_gen_accelerator_azure.components.outputs import CallToAction, ExitStrategy

logger = logging.getLogger(__name__)


class LLMResponse:
    """LLMResponse class encapsulating the response structure and parsing logic."""

    def __init__(
        self,
        content: str,
        call_to_action: Union[CallToAction, dict],
        exit_strategy: Union[ExitStrategy, str],
        model_details: dict,
    ):
        self.content = content
        self.call_to_action = (
            CallToAction(**call_to_action)
            if isinstance(call_to_action, dict)
            else call_to_action
        )
        try:
            self.exit_strategy = ExitStrategy(exit_strategy)
        except ValueError:
            logger.error(
                f"Invalid exit strategy provided: {exit_strategy}. Defaulting to 'ON_ERROR'.",
                extra={"exit_strategy": exit_strategy},
            )
            self.exit_strategy = ExitStrategy.ON_ERROR

        self.model_details = model_details

    @classmethod
    def from_json(cls, llm_response: dict, tracking_id: str) -> "LLMResponse":
        # TODO Check whether this structure is LLM-provider specific
        try:
            # Extract the complete response content from the LLM response dictionary
            choices = llm_response.get("choices")
            if not choices or not isinstance(choices, list) or len(choices) == 0:
                raise ValueError(
                    "Generation error: 'choices' is missing or empty in llm_response."
                )

            message = choices[0].get("message")
            if not message or "content" not in message:
                raise ValueError(
                    "Generation error: 'message' or 'content' is missing in the first choice."
                )

            message_content = JsonOutputParser.parse(message["content"])
            content = message_content.get("content")

            # TODO Determine call to action through prompt
            if (
                message_content
                and message_content.get("callToAction", {}).get("type")
                == "TO_LIVE_AGENT"
            ) or (content and "dolce-gusto.fr/nous-contacter" in content):
                call_to_action = CallToAction(type="TO_LIVE_AGENT", value=True)
            else:
                call_to_action = CallToAction(type="NONE")

            exit_strategy = message_content.get("exitStrategy")

            model_details = {
                "name": llm_response["model"],
                "prompt_tokens": llm_response["usage"]["prompt_tokens"],
                "completion_tokens": llm_response["usage"]["completion_tokens"],
                "total_tokens": llm_response["usage"]["total_tokens"],
                "params": llm_response["params"],
            }

            response_instance = cls(
                content=content,
                call_to_action=call_to_action,
                exit_strategy=exit_strategy,
                model_details=model_details,
            )

            logger.info(
                "Successfully parsed JSON response.",
                extra={
                    "content": content,
                    "tracking_id": tracking_id,
                    "total_tokens": model_details["total_tokens"],
                    "exit_strategy": exit_strategy,
                },
            )

            return response_instance

        except Exception as e:
            logger.error(
                f"Error processing LLM response: {e}",
                extra={"tracking_id": tracking_id},
            )
            return cls(
                content="",
                call_to_action=CallToAction(type="NONE"),
                exit_strategy=ExitStrategy.ON_ERROR,
                model_details={
                    "name": llm_response["model"],
                    "prompt_tokens": llm_response["usage"]["prompt_tokens"],
                    "completion_tokens": llm_response["usage"]["completion_tokens"],
                    "total_tokens": llm_response["usage"]["total_tokens"],
                    "params": llm_response["params"],
                },
            )

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "callToAction": self.call_to_action.model_dump(exclude_none=True),
            "exitStrategy": self.exit_strategy.value,
            "modelStats": self.model_details,
        }
