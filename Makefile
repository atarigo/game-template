PYTHON := uv run 

.PHONY: help dev code.test code.format code.clean

# Color definitions
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

help: ## Show this help message
	@echo "$(CYAN)Available commands:$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""

dev: code.format code.test ## Run the development server
	@$(PYTHON) python main.py

code.test: ## Run tests
	@$(PYTHON) pytest -v -rP

code.format: ## Format code
	@$(PYTHON) ruff check . --fix
	@$(PYTHON) ruff format .

code.clean: ## Clean cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
