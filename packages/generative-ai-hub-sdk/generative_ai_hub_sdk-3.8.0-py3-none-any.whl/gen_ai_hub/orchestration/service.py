import dacite
import requests

from dataclasses import dataclass
from typing import List, Optional

from enum import Enum

from gen_ai_hub import GenAIHubProxyClient
from gen_ai_hub.orchestration.exceptions import OrchestrationError
from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.config import OrchestrationConfig
from gen_ai_hub.orchestration.models.message import Message
from gen_ai_hub.orchestration.models.template import TemplateValue
from gen_ai_hub.orchestration.models.response import OrchestrationResponse
from gen_ai_hub.proxy import get_proxy_client


@dataclass
class OrchestrationRequest(JSONSerializable):
    """
    Represents a request for the orchestration process, including configuration, template values, and message history.

    Attributes:
        config: The configuration settings for the orchestration.
        template_values: A list of template values to be used in the request.
        history: The history of messages exchanged, typically used to maintain context.
    """

    config: OrchestrationConfig
    template_values: List[TemplateValue]
    history: List[Message]

    def to_dict(self):
        return {
            "orchestration_config": self.config.to_dict(),
            "input_params": {value.name: value.value for value in self.template_values},
            "messages_history": [message.to_dict() for message in self.history],
        }


class OrchestrationService:
    """
    A service for executing orchestration requests, allowing for the generation of LLM-generated content
    through a pipeline of configured modules.

    Attributes:
        api_url: The base URL for the orchestration API, through which all requests are made.
        config: An optional default configuration for the orchestration pipeline, which can be overridden per request.
        proxy_client: An optional proxy client for managing HTTP requests, facilitating communication with the API.
    """

    def __init__(
        self,
        api_url: str,
        config: Optional[OrchestrationConfig] = None,
        proxy_client: Optional[GenAIHubProxyClient] = None,
    ):
        if not api_url:
            raise ValueError("API URL must be provided and cannot be empty.")

        self.api_url = api_url
        self.config = config
        self.proxy_client = proxy_client or get_proxy_client(proxy_version="gen-ai-hub")

    def run(
        self,
        config: Optional[OrchestrationConfig] = None,
        template_values: Optional[List[TemplateValue]] = None,
        history: Optional[List[Message]] = None,
    ) -> OrchestrationResponse:
        """
        Executes an orchestration request, combining various modules into a pipeline
        and generating a response.

        Args:
            config: The configuration for this orchestration run. If not provided, the default configuration set
                    during initialization will be used.
            template_values: A list of key-value pairs to populate the request templates, allowing dynamic input.
            history: The message history, maintaining context across multiple interactions.

        Returns:
            OrchestrationResponse: The response from the Orchestration Service,
            containing the results of the executed pipeline.

        Raises:
            ValueError: If no configuration is provided either during initialization
                or in the method call, as the pipeline cannot be executed without it.
            OrchestrationError: If the API request fails due to an HTTP error, with
                details provided by the service's error response.
        """
        if self.config is None and config is None:
            raise ValueError(
                "OrchestrationConfig must be provided either during initialization or in the run method."
            )

        config = config or self.config

        request = OrchestrationRequest(
            config=config,
            template_values=template_values or [],
            history=history or [],
        )

        response = requests.post(
            self.api_url + "/completion",
            headers=self.proxy_client.request_header,
            json=request.to_dict(),
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            if not response.content:
                raise error

            error_content = response.json()
            raise OrchestrationError(
                request_id=error_content.get("request_id"),
                message=error_content.get("message"),
                code=error_content.get("code"),
                location=error_content.get("location"),
                module_results=error_content.get("module_results", {}),
            ) from error

        return dacite.from_dict(
            data_class=OrchestrationResponse,
            data=response.json(),
            config=dacite.Config(cast=[Enum]),
        )
