import os
from groq import Groq
from openai import OpenAI

groq_client = Groq(
        api_key= "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",
        )
    

openai_client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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",
)
