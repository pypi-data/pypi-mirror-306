from .llm_constants import support_msg
from .sfn_openai.sfn_openai_completions import sfn_openai_completions
# from sfn_blueprint.utils.llm_handler.anthropic.anthropic_client import sfn_anthropic_client

class SFNAIHandler:
    def __init__(self):
        self.client_map = {
            'openai': sfn_openai_completions,
            # 'anthropic': sfn_anthropic_client,
        }

    def route_to(self, llm_provider, model, configuration):
        if llm_provider in self.client_map:
            client = self.client_map[llm_provider]()
            return client.execute_api_call(model, configuration)
        else:
            print(support_msg(llm_provider))