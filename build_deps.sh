#!/usr/bin/env bash
set -o pipefail

pushd "deps/pomorski_czarodziej_components"

pushd "front_page_component/frontend"

npm install
npm run build

popd

# You might want to use pip install -e .
pip install "$(pwd)"

popd
