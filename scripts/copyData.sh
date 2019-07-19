#!/usr/bin/env bash

CLIENT_PATH=`cd ../../y-client && pwd`
SERVER_PATH=`cd ../../y-server && pwd`

DEST1=${CLIENT_PATH}/src/game/config
DEST2=${CLIENT_PATH}/resource/config/jsons


echo -------------------------------------------------
echo copy 到 y-client
echo -------------------------------------------------

cd ../code
mkdir -p ${DEST1}
rm -f ${DEST1}/config.d.ts ${DEST1}/config.hash ${DEST1}/config.ts
cp -rf config.d.ts config.hash config.ts ${DEST1}
cd -

cd ../config/jsons/
mkdir -p ${DEST2}
rm -f ${DEST2}/*.json
cp -rf *.json ${DEST2}
cd -

cd ${DEST2}/..
rm data.zip
zip -r data.zip jsons
cd -


cp ../server/*  ${SERVER_PATH}/data
