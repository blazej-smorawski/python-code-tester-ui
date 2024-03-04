# python-code-tester-ui

Simple frontend for hosting python programming competitions.

### Usage

```bash
pip install -r requirements.txt
python -m streamlit run test-code.py
```

Alternatively, you can run the code in a container:

```bash
docker run -p8501:8501 -v$(pwd)/.streamlit:/app/.streamlit docker.io/library/python-code-tester-ui:latest test-code.py
```

### Building

The project consists of frontend written in streamlit and components using javascript. To use the components, please install them using:

```bash
./build_deps.sh
```

The small script will build and install dependencies into your current python environment.

### Workarounds

In order to improve look of our site in search engines we supply `index.html` and `favicon.png` inside our containers. Please be careful when updating streamlit, because it might break the `index.html`. In case of problems with the file, you can compare it with `index.html` distributed alongside streamlit library: `./env/lib/python3.10/site-packages/streamlit/static/index.html`(Assuming you are using venv inside `env` directory).
