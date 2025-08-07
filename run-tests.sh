#!/bin/bash
cd /home/alex/Ornithoptere
source .venv/bin/activate
python -m pytest source/tests/ -v
