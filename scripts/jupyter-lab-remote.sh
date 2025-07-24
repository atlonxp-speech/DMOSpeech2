#!/bin/bash
echo "Starting Jupyter Lab on http://0.0.0.0:8888 (network accessible)"
echo "WARNING: This exposes Jupyter to your local network"
jupyter lab --ip=0.0.0.0 --no-browser --port=8888

