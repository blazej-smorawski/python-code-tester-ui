from io import StringIO
import json
import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="test-code",
    layout="wide"
)

c1, c2 = st.columns([2, 3])

with open('./example_code.py') as f:
    c1.download_button('Download example code', f, file_name='example_code.py')

with open('./example_cases.txt') as f:
    c2.download_button('Download example tests', f, file_name='example_test_cases.txt')

code_string = ""

c1.markdown("#### Choose a script to test")
code_file = c1.file_uploader(
    "Chose a script to test", label_visibility="hidden")
if code_file is not None:
    # To read file as bytes:
    bytes_data = code_file.getvalue()

    # To convert to a string based IO:
    stringio = StringIO(code_file.getvalue().decode("utf-8"))

    # To read file as string:
    code_string = stringio.read()
    c1.code(code_string, language="python")

c2.markdown("#### Choose test cases")
tests_file = c2.file_uploader(
    "Choose a file with test cases", label_visibility="hidden")
if tests_file is not None:
    df = pd.read_json(tests_file, orient="records")
    c2.write(df)

code_ran = False
if tests_file is not None and code_file is not None:
    run_tests = c2.button("Run tests")
    if run_tests:
        code_ran = True

if code_ran:
    renamed_df = df.rename(columns = {'Input':'input', 'OutputRegex':'output_regex'})
    payload = '{{"code": {}, "test_cases": {}}}'.format(json.dumps(code_string), renamed_df.astype(str).to_json(orient="records"))
    request = requests.post('https://server.blazej-smorawski.com/test_code', data=payload)
    #request = requests.post('http://localhost:4000/test_code', data=payload)

    if 200 <= request.status_code <= 299:    
        response = request.json()

        count = len(response['results'])
        output = ["" for _ in range(count)]
        for n in range(count):
            case_output = response['results'][n]
            output[case_output['test_case']] = case_output['output']

        passed = [0 for _ in range(count)]
        for n in response['passed']:
            passed[n] = 1

        df['Output'] = output
        df['Passed'] = passed

        def highlight(s):
            if s.Passed == 1:
                return ['background-color: mediumseagreen'] * len(s)
            else:
                return ['background-color: tomato'] * len(s)

        c2.write(df.style.apply(highlight, axis=1))
    else:
        c2.write(request)
