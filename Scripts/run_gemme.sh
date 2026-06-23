#!/usr/bin/env bash
set -euxo pipefail

STRUCTURE_DIR="/sstudio/structures"
MSA_DIR="/sstudio/msas"
MUT_DIR="/sstudio/processed_data"

cd /sstudio/model_scores/GEMME

mkdir -p ${DMS_ID}
cd ${DMS_ID}

echo ${GEMME_MUT_FILE}

python2.7 /sstudio/scripts/a2m_to_fasta.py ${MSA_DIR}/${MSA_FILENAME} ${DMS_ID}.fa

python2.7 $GEMME_PATH/gemme.py ${DMS_ID}.fa --mutations /sstudio/processed_data/${GEMME_MUT_FILE} -r input -f ${DMS_ID}.fa

cp *._normPred_evolCombi.txt ../${DMS_ID}.txt