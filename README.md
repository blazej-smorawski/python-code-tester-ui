# python-code-tester-ui

Simple frontend for hosting python programming competitions.

### Usage

The best way to use python-code-tester-ui is by using docker:
```bash
docker compose up
```

### Workarounds

In order to improve look of our site in search engines we supply `index.html` and `favicon.png` inside our containers. Please be careful when updating streamlit, because it might break the `index.html`. In case of problems with the file, you can compare it with `index.html` distributed alongside streamlit library: `./env/lib/python3.10/site-packages/streamlit/static/index.html`(Assuming you are using venv inside `env` directory).
