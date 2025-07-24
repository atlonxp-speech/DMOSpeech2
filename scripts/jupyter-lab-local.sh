#!/bin/bash
echo "Starting Jupyter Lab on http://127.0.0.1:8888"
echo "For remote access, use SSH tunnel: ssh -L 8888:localhost:8888 user@host"
jupyter lab --ip=127.0.0.1 --no-browser --port=8888