ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

TARGET_PYTHON_VERSION = python3

VENV_DIR := $(ROOT_DIR)/.venv
VENV_PIP := $(VENV_DIR)/bin/pip
VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_MYPY := $(VENV_DIR)/bin/mypy
VENV_FMT := $(VENV_DIR)/bin/autopep8

CONFIGS_DIR := $(ROOT_DIR)/config

ENTRYPOINT_FILE := $(ROOT_DIR)/main.py
REQUIREMENTS_FILE := $(ROOT_DIR)/requirements.txt

RESOURCES_FILE := $(CONFIGS_DIR)/resources.json

ENV_FILE := $(ROOT_DIR)/.env
ENV_EXAMPLE_FILE := $(ROOT_DIR)/.env.example

SOURCE_FOLDER := $(ROOT_DIR)/multi_parser

ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env
endif

run:
	$(VENV_PYTHON) $(ENTRYPOINT_FILE) --resources-path $(RESOURCES_FILE) --logging-level info

install: venv-dir
	$(VENV_PIP) install -r $(REQUIREMENTS_FILE)

clean:
	rm -rf $(VENV_DIR)

check:
	$(VENV_MYPY) $(SOURCE_FOLDER)

fmt:
	$(VENV_FMT) --in-place --recursive $(SOURCE_FOLDER)

venv-dir:
	virtualenv --python=$(TARGET_PYTHON_VERSION) $(VENV_DIR)

env:
	cp $(ENV_EXAMPLE_FILE) $(ENV_FILE)

calc-lines:
	( find $(SOURCE_FOLDER) -name '*.py' -print0 | xargs -0 cat ) | wc -l
