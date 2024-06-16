from prompts import SYSTEM_PROMPT
from tool_descriptions import tools
from utils import chat_completion_request, create_open_ai_client, handle_tool_call

client = create_open_ai_client()
MASTER_MODEL = "gpt-4o"
SLAVE_MODEL = "gpt-3.5-turbo-0125"

messages = []
messages.append({"role": "system", "content": SYSTEM_PROMPT})


def chat(query):
    messages.append({"role": "user", "content": query})
    try:
        response = chat_completion_request(
            client, messages, tools=tools, model=MASTER_MODEL
        )
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        return e

    response_message = response.choices[0].message
    messages.append(response_message)

    tool_calls = response_message.tool_calls
    if tool_calls:
        model_message, tool_result = handle_tool_call(
            client, tool_calls, messages
        )
        return model_message, tool_result

    else:
        return response_message.content


while 1:
    query = input("User: ")
    print("Assistant:", chat(query))
