import openai
import re
import sys
from io import StringIO

def generate_code(question, data=None, data_context=""):
    client = openai.Client(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    system_prompt = """
        Generate python code that:
        - uses only provided veriables
        - Prints results
        - Include any needed imports
    """

    user_message = f"{data_context}\nAvailable veriables{list[data.keys()] if data is not None else []}\n\nTask:{question}"


    chat_data = client.chat.completions.create(
        model="deepseek-r1:70b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    response = chat_data.choices[0].message.content
    return get_clean_llm_code_response(response)


def get_clean_llm_code_response(code):
    response = re.sub(r'<think>.*?</think>', '', code, flags=re.DOTALL)
    code_match = re.search(r'```python\n(.*?)```', response, flags=re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    
    return response.strip()

def execute_code(code, data=None):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    local_vars = data or {}

    try:
        exec(code, local_vars)
        output = sys.stdout.getvalue()
        return {"output": output, "errors": None, "results": local_vars}
    except Exception as e:
        return {"output": None, "errors": str(e), "results": None}
    finally:
        sys.stdout=old_stdout


def agent(question, data, data_context):
    solution = generate_code(question, data, data_context)
    print('generated code: ')
    print(solution)

    result = execute_code(solution, data)

    print("\nRESULTS: ")
    if result['errors']:
        print(f'error: {result['errors']}')
    else:
        print(result['output'])

    return solution, result

sys.modules[__name__] = agent