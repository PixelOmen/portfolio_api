from django.conf import settings

import openai


async def stream_response(messages):
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield {"chat_id": chunk.id, "content": chunk.choices[0].delta.content}
