#!/bin/bash
uvicorn map_api:app --host=0.0.0.0 --port=$PORT
