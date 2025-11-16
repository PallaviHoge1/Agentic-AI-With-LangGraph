#!/bin/bash

# Create main project folder
# mkdir -p langgraph-math-agent
# cd langgraph-math-agent

# Create src folders
mkdir -p src
mkdir -p src/agent
mkdir -p src/tools
mkdir -p src/utils

# Create test folder
mkdir -p tests

# Create notebooks folder (optional for experimentation)
mkdir -p notebooks

# Create environment files
touch requirements.txt
touch README.md

# Starter Python files
touch src/agent/__init__.py
touch src/agent/graph.py
touch src/tools/__init__.py
touch src/tools/math_tools.py
touch src/utils/__init__.py
touch src/utils/router.py
touch src/utils/llm_client.py

# Starter test file
touch tests/test_tools.py

echo "Project structure created successfully."
