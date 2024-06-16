import os
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from tool_descriptions import tools
from prompts import TOOL_CALL_SUMMARISE_PROMPT
from db.mongo_call import (
    findDoctors,
    getDoctorSchedule,
    getUserAppointments,
    bookAppointment,
)
import inspect

load_dotenv()
MASTER_MODEL = "gpt-4o"
SLAVE_MODEL = "gpt-3.5-turbo-0125"
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")


def create_open_ai_client():
    client = OpenAI(api_key=OPEN_AI_API_KEY)
    return client


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(
    client, messages, tools=None, tool_choice=None, model=MASTER_MODEL
):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            max_tokens=500,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def execute_function(func_name, func_args):
    functions = {
        "findDoctors": findDoctors,
        "getDoctorSchedule": getDoctorSchedule,
        "getUserAppointments": getUserAppointments,
        "bookAppointment": bookAppointment,
    }

    if func_name not in functions:
        return {"status": False, "error": f"Function '{func_name}' not found"}

    func = functions[func_name]
    args = [func_args.get(arg) for arg in inspect.signature(func).parameters]
    result = func(*args)

    if not result["status"]:
        return {"status": False, "error": str(result["error"])}
    else:
        return {"status": True, "data": str(result["data"])}


def handle_tool_call(client, tool_calls, messages):
    tool_call_id = tool_calls[0].id
    tool_function_name = tool_calls[0].function.name
    tool_function_arguments = eval(tool_calls[0].function.arguments)

    results = execute_function(tool_function_name, tool_function_arguments)

    if not results["status"]:
        results = str(results["error"])
    else:
        results = str(results["data"])

    tool_call_init_message = messages[-1]
    tool_call_results_message = {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "name": tool_function_name,
        "content": results,
    }

    messages.append(tool_call_results_message)

    model_response_with_function_call = chat_completion_request(
        client,
        [
            {"role": "system", "content": TOOL_CALL_SUMMARISE_PROMPT},
            tool_call_init_message,
            tool_call_results_message,
        ],
        model=SLAVE_MODEL,
        tools=tools,
        tool_choice=None,
    )
    model_message = model_response_with_function_call.choices[0].message.content
    return (model_message, results)
