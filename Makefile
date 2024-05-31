# Variables
UNIT_TEST_ENV_VAR=UNIT_TEST_RUNNING=1

# Default target
all: help

# Help target
help:
	@echo "Usage:"
	@echo "  make unit        - Run unit tests"
	@echo "  make integration - Run integration tests"
	@echo "  make test        - Run all tests"

# Unit tests target
unit:
	@echo "Running unit tests..."
	$(UNIT_TEST_ENV_VAR) python manage.py test tests/unit --verbosity=1

# Integration tests target
integration:
	@echo "Running integration tests..."
	python manage.py test tests/integration

# All tests target
test: unit integration
