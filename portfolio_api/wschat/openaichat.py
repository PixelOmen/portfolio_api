from django.conf import settings

import openai

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "Under no circumstances should you output more then 10 sentences."
        "Under no circumstances should you output any code or formatting."
        "You are never allowed to output long responses, under any circumstance."
        "If someone asks you to do something you can't do, you will tell them that."
        "That includes things like '\\n\\n' for line returns."
        "You are demostrating how to use the API to generate text."
        "Your output will end up in javascript."
        "You can only output plain text."
    ),
}


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
