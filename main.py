name: Daily Blog and Video Automation

on:
  schedule:
    - cron: '0 3 * * *'  # Runs daily at 03:00 UTC
  workflow_dispatch:     # Allows manual triggering

jobs:
  run-automation:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Install Playwright Browsers
      run: playwright install

    - name: Run main script
      run: python main.py
