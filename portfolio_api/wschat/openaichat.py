from django.conf import settings

import openai

openai.api_key = settings.OPENAI_API_KEY

# client = OpenAI()
# stream = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "write a haiku about ai"},
#     ],
#     stream=True,
# )

# for chunk in stream:
#     if chunk.choices and chunk.choices[0].delta.content:
#         print(chunk.id)
#         print()
#         pprint(chunk.choices[0].delta.content, indent=2)
#         print()
#         print()
#     # if chunk.choices[0].delta.content is not None:
#     #     pprint(chunk.choices[0], indent=2)
#     #     print()


async def stream_response(messages):
    client = openai.OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield {"id": chunk.id, "content": chunk.choices[0].delta.content}
