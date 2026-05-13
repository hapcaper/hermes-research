#!/usr/bin/env python3
"""Quick check of available packages in venv"""
import subprocess
import sys

packages = ['fastapi', 'uvicorn', 'requests']
python = '/Users/lizihao/.hermes/hermes-agent/venv/bin/python3'

for pkg in packages:
    result = subprocess.run([python, '-c', f'import {pkg}; print("{pkg} OK")'],
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(f'{pkg}: NOT AVAILABLE')