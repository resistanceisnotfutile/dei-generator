"""Use a local AI agent to generate fake (but believable) reports for the DEInied site."""

import sys
import getopt
from ctypes import ArgumentError

import ollama
from ollama import ChatResponse, chat, ResponseError
from tools import get_school_information

available_functions = {
    "get_school_information": get_school_information,
}

MODELS_SUPPORTING_TOOLS = [
    "qwq",
    "llama3.3",
    "llama3.2",
    "llama3.1",
    "mistral",
    "qwen2.5",
    "qwen2.5-coder",
    "qwen2",
    "mistral-nemo",
    "mixtral",
    "smollm2",
    "mistral-small",
    "command-r",
    "hermes3",
    "mistral-large",
    "command-r-plus",
    "granite3.1-dense",
    "athene-v2",
    "nemotron-mini",
    "nemotron",
    "granite3-dense",
    "llama3-groq-tool-use",
    "aya-expanse",
    "granite3-moe",
    "granite3.1-moe",
    "phi4-mini",
    "command-r7b",
    "firefunction-v2",
    "granite3.2-vision",
    "granite3.2",
    "command-r7b-arabic",
]


def load_system_prompt(filepath="system_prompt.txt"):
    """Load and return a sytem prompt. Use a sane default if the file is not found."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"System prompt not found at {filepath}. Using default system prompt.")
        return "You are a helpful AI agent."


def generate_response(
    use_model,
    user_prompt="Tell me about my child's school.",
    system_prompt_file="system_prompt.txt",
):
    """Generate a response from the custom agent."""
    system_prompt = load_system_prompt(system_prompt_file)

    if system_prompt is None:
        return None

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    supports_tool = use_model.split(":")[0] in MODELS_SUPPORTING_TOOLS

    try:
        tools = [get_school_information] if supports_tool else None
        chat_response: ChatResponse = chat(
            model=use_model, messages=messages, tools=tools
        )
        if supports_tool:
            if chat_response["message"]["tool_calls"]:
                for tool in chat_response["message"]["tool_calls"]:
                    output = {}
                    if function_to_call := available_functions.get(tool.function.name):
                        output = function_to_call()
                    else:
                        print(f"Function {tool.function.name} not found.")

                    messages.append(chat_response["message"])
                    messages.append(
                        {
                            "role": "tool",
                            "content": str(output),
                            "name": tool.function.name,
                        }
                    )
                    final_repsonse: ChatResponse = chat(
                        model=use_model, messages=messages
                    )
                    return final_repsonse["message"]["content"]

        return chat_response["message"]["content"]
    except ResponseError as re:
        print(f"ResponseError generating response: {re}")

    return None


if __name__ == "__main__":
    USER_PROMPT = "Tell me about my child's school."
    SYSTEM_PROMPT_FILE = "system_prompt.txt"

    argument_list = sys.argv[1:]
    OPTIONS = "hm:"
    long_options = ["Help", "Model="]

    # Define a default model.
    models = ollama.list()["models"]
    if len(models) == 0:
        raise ArgumentError("No models found.")
    model = models[0]["model"]

    try:
        arguments, values = getopt.getopt(argument_list, OPTIONS, long_options)
        for current_argument, current_value in arguments:
            if current_argument in ("-h", "--help"):
                print(
                    f"""
Generate fake submission data for the End DEI page.

-h / --help:                  Display this message.
-m [model] / --model=[model]: Use the specific model. Default: {model}
"""
                )
                sys.exit(0)
            elif current_argument in ("-m", "--Model"):
                model = current_value
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    response = generate_response(
        use_model=model,
        user_prompt=USER_PROMPT,
        system_prompt_file=SYSTEM_PROMPT_FILE,
    )
    print(response)
