from typing import Optional, List

from gen_ai_hub.orchestration.models.base import JSONSerializable
from gen_ai_hub.orchestration.models.content_filter import ContentFilter
from gen_ai_hub.orchestration.models.llm import LLM
from gen_ai_hub.orchestration.models.data_masking import DataMasking
from gen_ai_hub.orchestration.models.template import Template


class OrchestrationConfig(JSONSerializable):
    """
    Configuration for the Orchestration Service's content generation process.

    Defines modules for a harmonized API that combines LLM-based content generation
    with additional processing functionalities.

    The orchestration service allows for advanced content generation by processing inputs through a series of steps:
    template rendering, text generation via LLMs, and optional input/output transformations such as data masking
    or filtering.

    Args:
        template: Template object for rendering input prompts.
        llm: Language model for text generation.
        input_filters: Filters applied to inputs. Defaults to an empty list.
        output_filters: Filters applied to outputs. Defaults to an empty list.
        data_masking: An optional data masking module to anonymize or pseudonymize sensitive information in inputs.
    """

    def __init__(
        self,
        template: Template,
        llm: LLM,
        input_filters: Optional[List[ContentFilter]] = None,
        output_filters: Optional[List[ContentFilter]] = None,
        data_masking: Optional[DataMasking] = None,
    ):
        self.template = template
        self.llm = llm
        self.data_masking = data_masking
        self.input_filters = input_filters or []
        self.output_filters = output_filters or []

    def to_dict(self):
        config = {
            "module_configurations": {
                "templating_module_config": self.template.to_dict(),
                "llm_module_config": self.llm.to_dict(),
            }
        }

        if self.data_masking:
            config["module_configurations"]["masking_module_config"] = self.data_masking.to_dict()

        filtering_config = {}

        if self.input_filters:
            filtering_config["input"] = {
                "filters": [f.to_dict() for f in self.input_filters]
            }

        if self.output_filters:
            filtering_config["output"] = {
                "filters": [f.to_dict() for f in self.output_filters]
            }

        if filtering_config:
            config["module_configurations"][
                "filtering_module_config"
            ] = filtering_config

        return config
