#!/usr/bin/env bash

pushd "deps/pomorski_czarodziej_components"

pushd "front_page_component/frontend"

npm install
npm run build

popd

pip install -e .

popd
