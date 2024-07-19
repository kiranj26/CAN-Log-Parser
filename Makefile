.PHONY: lint check

# Install dependencies
install:
	pip install -r requirements.txt

# Lint the code using flake8
lint:
	flake8 src test --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 src test --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Check if all Python files are error-free using mypy
check:
	mypy src test

# Run all checks
all: install lint check
