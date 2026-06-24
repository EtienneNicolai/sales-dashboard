import sys

checks = [
    ("fastapi",           "from fastapi import FastAPI; FastAPI()"),
    ("uvicorn",           "import uvicorn"),
    ("pandas",            "import pandas as pd"),
    ("python-multipart",  "from multipart.multipart import parse_options_header"),
    ("anthropic",         "from anthropic import Anthropic"),
    ("pytest",            "import pytest"),
    ("pytest-asyncio",    "import pytest_asyncio"),
    ("httpx",             "import httpx"),
]

all_ok = True
for name, stmt in checks:
    try:
        exec(stmt)
        print(f"  ✓  {name}")
    except Exception as e:
        print(f"  ✗  {name}  ({e})")
        all_ok = False

if not all_ok:
    print("\nFix the above before writing any code.")
    print("Install with: python -m pip install --target=backend\\lib -r requirements.txt")
    sys.exit(1)
else:
    print("\nAll checks passed. Ready to build.")
