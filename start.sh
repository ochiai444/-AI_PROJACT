#!/usr/bin/env bash
export PYTHONPATH=.
uvicorn app.app.main:app --host 0.0.0.0 --port "${PORT:-10000}"