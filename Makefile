APP_NAME:=dify-plugin-broker
PYTHON_VER:=3.12.9

.PHONY: test clean

all: test clean

test: clean
	@echo "[MAKEFILE] Testing"
	pytest --cov=tools tests/

clean:
	@echo "[MAKEFILE] Cleaning..."
	rm -rf .pytest_cache
	rm -rf .coverage
	@echo "[MAKEFILE] Cleaned"
