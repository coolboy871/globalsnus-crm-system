#!/usr/bin/env python
"""
Simple script to check server paths and permissions
"""
import os
import sys

def check_paths():
    try:
        print("Current working directory:", os.getcwd())
        print("\nDirectory contents:", os.listdir())
        print("\nHome directory:", os.path.expanduser("~"))
        print("\nScript location:", os.path.dirname(os.path.abspath(__file__)))
        print("\nPython path:", sys.path)
        print("\nEnvironment variables:", dict(os.environ))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    check_paths()
