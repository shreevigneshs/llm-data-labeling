import json
from openai import OpenAI


OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY, organization="org-SqAqKbRAlkpTd28SbobD0Prf")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  seed=42,
  temperature=0,
  top_p=1,
  max_tokens=1,
  logprobs=True,
  top_logprobs=5,
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)


print(completion.choices)