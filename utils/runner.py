import re
import requests
import streamlit as st
from time import time

# for rate limiting
prev_requests_times = []
running_counter = 0


def run_code(code, stdin):
    global running_counter
    domain = st.secrets["piston_url"]
    url = f"{domain}/api/v2/execute"

    wait = st.empty()
    wait.write("Wykonywanie programu. Proszę czekać...")

    payload = {
        "language": "python",
        "version": "3.10.0",
        "files": [
            {
                "name": "code.py",
                "content": code
            }
        ],
        "stdin": stdin
    }

    # rate limit (max 5 requests / 5 seconds)
    prev_requests_times.append(int(time()))
    while prev_requests_times[0] < int(time()) - 5:
        prev_requests_times.pop(0)
    if len(prev_requests_times) >= 5:
        wait.empty()
        return {"input": stdin, "output": "", "error": "Wysyłasz za dużo informacji. Zwojnij!", "code": -1}

    if running_counter > 3:
        return {"input": stdin, "output": "", "error": "Wysyłasz za dużo informacji. Zwojnij!", "code": -1}
    running_counter += 1

    req = requests.post(url, json=payload)

    running_counter -= 1

    if req.status_code != 200:
        return {"input": stdin, "output": "", "error": "Awaria serwisu `pomorskiczarodziej.pl`", "code": -1}

    result = req.json()

    wait.empty()
    if result['run']['signal'] == "SIGKILL":
        return {"input": stdin, "output": "", "error": "Nieodpowiedni kod (niebezpieczny lub za długi do wykonania)", "code": -1}

    return {"input": stdin, "output": result['run']['stdout'], "error": result['run']['stderr'], "code": result['run']['code']}


def test_code(task, code, private=False):
    testcases = task["test-cases"]

    try:
        results = []
        for testcase in testcases:
            # If private is False, we skip testcases without `public` key or with the key equal to False
            if private == False and (not "public" in testcase or testcase["public"] == False):
                continue

            stdin = testcase["input"].replace('\\n', '\n')
            result = run_code(code, stdin)

            if result['code'] == 0 and re.match(str(testcase["output"]).replace('\\n', '\n'), result['output']):
                results.append(
                    {"passed": True, **result})
            else:
                results.append(
                    {"passed": False, **result})

        return results
    except:
        st.error("Coś poszło nie tak, sprawdź przypadki testowe")
        return None


def display_run_result(code_result):
    if code_result["input"] != "":
        input_col, output_col = st.columns([3, 3])
        input_col.write("Wejście programu")
        input_col.code(code_result["input"])
        output_col.write("Wyjście programu")
        output_col.code(code_result["output"])
    else:
        st.write("Wyjście programu")
        st.code(code_result["output"])

    if code_result["error"] != "":
        st.write("Błędy wykonania programu:")
        st.code(code_result["error"])


def display_testcase_result(testcase):
    if testcase["passed"]:
        st.success(f"Test zaliczony", icon="✅")
    else:
        st.error(f"Test niezaliczony", icon="❌")
        display_run_result(testcase)
