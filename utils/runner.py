import re
import requests
import streamlit as st

def run_code(task, code):
    testcases = task["test-cases"]

    try:
        for testcase in testcases:
            url = 'https://piston-dev.kubernetes.blazej-smorawski.com/api/v2/execute'
            payload = {
                "language": "python",
                "version": "3.10.0",
                "files": [
                    {
                        "name": "code.py",
                        "content": code
                    }
                ],
                # Replace \\n with \n
                "stdin": testcase["input"].replace('\\n', '\n')
            }
            req = requests.post(url, json=payload)
            result = req.json()

            if req.status_code == 200 and result['run']['code'] == 0 and re.match(testcase["output"].replace('\\n', '\n'), result['run']['stdout']):
                st.success(f"Test zaliczony", icon="✅")
            else:
                st.error(f"Test niezaliczony", icon="❌")

            input_col, output_col = st.columns([3, 3])
            input_col.write("Wejście programu")
            input_col.code(testcase["input"].replace('\\n', '\n'))
            output_col.write("Wyjście programu")
            output_col.code(result['run']['stdout'])

            if result['run']['stderr'] != "":
                st.write("Błędy wykonania programu:")
                st.code(result['run']['stderr'])
    except:
        st.error("Coś poszło nie tak, sprawdź przypadki testowe")