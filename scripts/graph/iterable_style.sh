#!/bin/sh
BLUE='\033[0;44m'
NOCOLOR='\033[0m'

# Constants
INPUTFILE=/mnt/data/dataset/fb15k-237/train.txt
INPUTFILESIZE=1
TYPE=i
WORKLOAD=graph
ITR=1

# RocksDB
DS=rd
ROWSPERKEY=1
WRITE=1
for workers in 0 8 16 32
do
    WORKERS=$workers
    for prefetchsize in 128 256 512 1024
    do
        PF=$prefetchsize
        for batchsize in 128 256 512 1024
        do
            BATCHSIZE=$batchsize
            OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}_p${PF}"
            
            echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE}, PF={$PF} ${NOCOLOR}"
            if [ $WRITE -eq 1 ]
            then
                python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -pf $PF > $OUTPUTFILE
                WRITE=0
            else
                python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -pf $PF -skip-write True > $OUTPUTFILE
            fi
        done
    done
done

# Awaiting data loader fix
# TileDB
# DS=td
# ROWSPERKEY=1
# WRITE=1
# for workers in 0 8 16 32
# do 
#     WORKERS=$workers
#     for prefetchsize in 128 256 512 1024
#     do
#         PF=$prefetchsize
#         for batchsize in 128 256 512 1024
#         do
#             BATCHSIZE=$batchsize
#             OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}_p${PF}"
            
#             echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE}, PF={$PF} ${NOCOLOR}"
#             if [ $WRITE -eq 1 ]
#             then
#                 python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -pf $PF > $OUTPUTFILE
#                 WRITE=0
#             else
#                 python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -pf $PF -skip-write True > $OUTPUTFILE
#             fi
#         done
#     done
# done
    
# Tensorstore - not present
# DS=ts
# ROWSPERKEY=1
# WRITE=1
# for workers in 0 8 16 32
# do 
#     WORKERS=$workers
#     for prefetchsize in 128 256 512 1024
#     do
#         PF=$prefetchsize
#         for batchsize in 128 256 512 1024
#         do
#             BATCHSIZE=$batchsize
#             OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}_p${PF}"
            
#             echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE}, PF={$PF} ${NOCOLOR}"
#             if [ $WRITE -eq 1 ]
#             then
#                 python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -pf $PF > $OUTPUTFILE
#                 WRITE=0
#             else
#                 python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -num-workers $WORKERS -input-rows-per-key $ROWSPERKEY -type $TYPE -batch-size $BATCHSIZE -pf $PF -skip-write True > $OUTPUTFILE
#             fi
#         done
#     done
# done


# Baseline 
DS=base
ROWSPERKEY=1
WORKERS=0
for batchsize in 128 256 512 1024
do
    BATCHSIZE=$batchsize
    OUTPUTFILE="../output/${DS}/${WORKLOAD}/i${INPUTFILESIZE}_w${WORKERS}_r${ROWSPERKEY}_t${TYPE}_b${BATCHSIZE}"
    
    echo "${BLUE} DS=${DS}, WORKLOAD=${WORKLOAD}, WORKERS=${WORKERS}, TYPE=${TYPE}, ROWSPERKEY=${ROWSPERKEY}, BATCHSIZE=${BATCHSIZE}, ${NOCOLOR}"
    python ../$WORKLOAD/main.py -ds $DS -input-file $INPUTFILE -type $TYPE -batch-size $BATCHSIZE > $OUTPUTFILE
done
