name: Build APK

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libsqlite3-dev lld libffi-dev python3-setuptools
        pip install --upgrade pip
        pip install buildozer cython virtualenv

    - name: Build with Buildozer
      run: |
        yes | buildozer android debug
      env:
        ACCEPT_SDK_LICENSE: "y"

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: Ponto-APK
        path: bin/*.apk
