#!/bin/bash
cd /home/kavia/workspace/code-generation/digital-id-card-manager-04b007d0/id_backend_api
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

