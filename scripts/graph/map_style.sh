#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

# Constants
INPUTFILE=/mnt/data/dataset/fb15k-237/train.txt
INPUTFILESIZE=1
TYPE=m
WORKLOAD=graph
ITR=1

# RocksDB
# DS=rd
# for workers in 0 8 16 32
# do
#     WORKERS=$workers
#     for rowsperkeysize in 1 128 256 512 1024
#     do
#         WRITE=1
#         ROWSPERKEY=$rowsperkeysize
#         for batchsize in 128 256 512 1024
#         do
#             BATCHSIZE=$batchsize
#             OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
            
#             echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
#             if [ $WRITE -eq 1 ]
#             then
#                 python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
#                 WRITE=0
#             else 
#                 python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -skip-write True > $OUTPUTFILE
#             fi
#         done
#     done
# done

# Awaiting fix
# TileDB
# DS=td
# ROWSPERKEY=1
# WRITE=1
# for workers in 0 8 16 32
# do 
#     WORKERS=$workers
#     for batchsize in 128 256 512 1024
#     do
#         BATCHSIZE=$batchsize
#         OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
        
#         echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
#         if [ $WRITE -eq 1 ]
#         then
#             python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
#             WRITE=0
#         else 
#             python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -skip-write True > $OUTPUTFILE
#         fi
#     done
# done
    
# Tensorstore
DS=ts
ROWSPERKEY=1
WRITE=1
for workers in 0 8 16 32
do 
    WORKERS=$workers
    for batchsize in 128 256 512 1024
    do
        BATCHSIZE=$batchsize
        OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
        
        echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE} ${NOCOLOR}"
        if [ $WRITE -eq 1 ]
        then
            python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
            WRITE=0
        else 
            python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -skip-write True > $OUTPUTFILE
        fi
    done
done