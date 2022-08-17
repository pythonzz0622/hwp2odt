#!/bin/bash

for entry in `ls ./dataset/`; do
    python source/hwp2odt.py --file_name=$entry --output_dir="output"
done