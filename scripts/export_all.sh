#!/usr/bin/env bash
CURRENT_DIR=`cd "$(dirname $0)"; pwd`

cd ${CURRENT_DIR}

mkdir -p ../code/config
mkdir -p ../config/jsons
mkdir -p ../server

rm -f ../code/config.*
rm -f ../config/jsons/*
rm -f ../server/*

cd gen_config
python export.py 
cd ../gen_dts
python gen_dts.py
cd ../pack
python pack.py
cd ${CURRENT_DIR}
bash copyData.sh

