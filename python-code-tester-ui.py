"""
# My first app
Here's our first attempt at using data to create a table:
"""

from io import StringIO
import json
import requests
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.markdown("# python-code-tester-ui")

c1, c2 = st.columns([2,3])

code_string = ""

code_file = c1.file_uploader("Choose a script to test")
if code_file is not None:
    # To read file as bytes:
    bytes_data = code_file.getvalue()

    # To convert to a string based IO:
    stringio = StringIO(code_file.getvalue().decode("utf-8"))

    # To read file as string:
    code_string = stringio.read()
    c1.code(code_string, language="python")

tests_file = c2.file_uploader("Choose a file with test cases")
if tests_file is not None:
    df = pd.read_csv(tests_file, names=["Input","Expected Output"])  

    c2.write(df)

code_ran = False
if tests_file is not None and code_file is not None:
    run_tests = c2.button("Run tests")
    if run_tests:
        code_ran = True


if code_ran:
    test_cases_dict = [{'input': str(df['Input'][n]), 'output': str(df['Expected Output'][n])} for n in range(len(df['Expected Output']))]
    request = requests.post('https://server.blazej-smorawski.com/test_code', json={"code": code_string, "test_cases": test_cases_dict})
    response = request.json()

    count = len(response['results'])
    output = ["" for x in range(count)]
    for n in range(count):
        case_output = response['results'][n]
        output[case_output['test_case']] = case_output['output']

    passed = [0 for x in range(count)]
    for n in response['passed']:
        passed[n] = 1

    df['Output'] = output
    df['Passed'] = passed

    def highlight(s):
        if s.Passed == 1:
            return ['background-color: green'] * len(s)
        else:
            return ['background-color: red'] * len(s)


    c2.write(df.style.apply(highlight, axis=1))



