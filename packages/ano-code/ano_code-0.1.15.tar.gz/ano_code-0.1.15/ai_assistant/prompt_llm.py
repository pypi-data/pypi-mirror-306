from groq import Groq
from ai_assistant.interfaces import LlmOptions, LlmInterface, AIAssistantInterface
from ai_assistant.consts import UserRole, AIModel
from typing import TypeVar

T = TypeVar('T')





class PromptLlm(LlmInterface):
    def __init__(self, llm_options: LlmOptions)-> None:
        super().__init__(llm_options)

    def prompt(self, cli: T) -> (str | None):
        opt = self.llm_options
        chat_completion = cli.chat.completions.create(
            messages=opt.messages,
            model=opt.model,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        prompt_result = chat_completion.choices[0].message.content
        return prompt_result



class AIAssistant(AIAssistantInterface):
    def __init__(self, cli: Groq) -> None:
        super().__init__(cli)


    def run_assistant(self, prompt: str, command: str)-> str:
        llm_opt = LlmOptions(
        messages=[
            {
                "role": UserRole.SYSTEM_ROLE.value,
                "content": command
            },
            {
                "role": UserRole.USER_ROLE.value,
                "content": prompt,
            }
        ],
        model=AIModel.LLAMA_3_405B_INSTRUCT.value,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
        )
        promptLlm = PromptLlm(llm_opt)
        prompt_result = promptLlm.prompt(self.cli)
        return prompt_result




# completion = openai_client.chat.completions.create(
#   model=AIModel.LLAMA_3_405B_INSTRUCT,
#   messages=[{"role":"user","content":"Write a limerick about the wonders of GPU computing."}],
#   temperature=0.2,
#   top_p=0.7,
#   max_tokens=1024,
#   stream=True
# )

# for chunk in completion:
#   if chunk.choices[0].delta.content is not None:
#     print(chunk.choices[0].delta.content, end="")




# ai_assistant = AIAssistant(client)

# result = ai_assistant.run_assistant("Utterly", COMMANDS["dictionary"])

# print(result)
