import os 
from dotenv import load_dotenv
import logging 
from google import genai 
from google.genai import types
import argparse
import prompts
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function
from typing import List 
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger() 
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file, 
        schema_get_file_content, 
        schema_run_python_file],
)

def get_result_str(content, verbose:bool, function_results:List[str]):
    if content.function_calls != None and isinstance(content.function_calls, list):
        for function_call in content.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            print(f"Function result: {function_call}")
            function_call_result = call_function(function_call, verbose)
            response =  function_call_result.parts[0].function_response
            if response == None:
                raise Exception("No response found calling function")
            # function_results.append(function_call_result.parts[0].function_response.response)
            function_results.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(content.text)
        function_results.append(content.text)
    return function_results

def main(user_prompt:str, verbose:bool=False):
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    function_results = []

    content = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=prompts.system_prompt, 
                                               tools=[available_functions],
                                               temperature=0.2))
    for _ in range(10):
        if content.candidates != None:

            messages.extend(content.candidates)
        content = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=prompts.system_prompt, 
                                               tools=[available_functions],
                                               temperature=0.2))
        print(f"{content.candidates}")
        if verbose==True:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
        
        get_result_str(content, verbose, function_results)

        if "task completed" in function_results[-1]:
            break 
        messages.append(types.Content(role="user", parts=function_results))

        
    


def test_inputs(user_prompt, verbose):
    print(f"{user_prompt=}, {verbose=}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    test_inputs(args.user_prompt, args.verbose)
    main(args.user_prompt, verbose=args.verbose) 
    