#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Number of arguments incorrect! Pass system rmq-port only!"; exit;
fi

export RADICAL_PILOT_DBURL='mongodb://user:user@ds239009.mlab.com:39009/inspire-2'
export RADICAL_PILOT_PROFILE=True
export RADICAL_ENMD_PROFILE=True
export RADICAL_ENMD_PROFILING=1
export RP_ENABLE_OLD_DEFINES=True

export RADICAL_ENTK_VERBOSE='DEBUG'
export RADICAL_SAGA_VERBOSE='DEBUG'
export RADICAL_PILOT_VERBOSE='DEBUG'

python rfe.py $1 $2 &> rfe.rp.session.log
