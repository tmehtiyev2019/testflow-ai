# Makefile for TestFlow AI
# Simplifies Docker commands for common tasks

.PHONY: help build test test-verbose test-creation test-execution test-swap clean shell

help: ## Show this help message
	@echo "TestFlow AI - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker image
	docker-compose build

test: ## Run all acceptance tests
	docker-compose run --rm testflow behave acceptance_tests/

test-verbose: ## Run all tests with verbose output
	docker-compose run --rm testflow behave acceptance_tests/ --verbose

test-creation: ## Run test creation scenarios only
	docker-compose run --rm testflow behave acceptance_tests/test_creation.feature

test-execution: ## Run test execution scenarios only
	docker-compose run --rm testflow behave acceptance_tests/test_execution.feature

test-swap: ## Run SWAP CHALLENGE scenario
	docker-compose run --rm testflow behave acceptance_tests/ai_capabilities.feature

test-name: ## Run specific scenario by name (usage: make test-name NAME="scenario name")
	docker-compose run --rm testflow behave acceptance_tests/ --name "$(NAME)"

shell: ## Open bash shell in container
	docker-compose run --rm testflow bash

clean: ## Remove containers and clean up
	docker-compose down
	rm -rf reports/ screenshots/

rebuild: ## Rebuild Docker image from scratch
	docker-compose down
	docker-compose build --no-cache

version: ## Check Behave version
	docker-compose run --rm testflow behave --version
