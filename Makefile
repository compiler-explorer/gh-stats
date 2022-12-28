export POETRY_HOME=$(CURDIR)/.poetry
POETRY:=$(POETRY_HOME)/bin/poetry
POETRY_VENV=$(CURDIR)/.venv
POETRY_DEPS:=$(POETRY_VENV)/.deps
SYS_PYTHON:=$(shell env PATH='/bin:/usr/bin:/usr/local/bin:$(PATH)' bash -c "command -v python3.11 || command -v python3.10 || command -v python3.9 || echo .python-not-found")
export PYTHONPATH=$(CURDIR)/bin

.PHONY: help
help: # with thanks to Ben Rady
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

$(SYS_PYTHON):
	@echo "Python 3.9 or 3.10 not found on path. Please install (sudo apt install python3.9 or similar)"
	@exit 1

.PHONY: clean
clean:  ## Cleans up everything
	rm -rf $(POETRY_HOME) $(POETRY_VENV)

.PHONY: deps poetry
deps: $(POETRY) $(POETRY_DEPS)  ## Installs and configures dependencies
poetry: $(POETRY)
$(POETRY): $(SYS_PYTHON)
	curl -sSL https://install.python-poetry.org | $(SYS_PYTHON) -
	@touch $@

$(POETRY_DEPS): $(POETRY) pyproject.toml poetry.lock
	$(POETRY) install --sync
	@touch $@
