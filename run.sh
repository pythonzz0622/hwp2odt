#!/bin/bash

:<<'END'
dataset경로를 통해 파일을 읽어오는 코드입니다.
END

for entry in `ls ./dataset/`; do
    python source/hwp2odt.py --file_name=$entry --output_dir="output"
done