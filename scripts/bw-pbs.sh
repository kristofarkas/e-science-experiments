#!/bin/bash

export RADICAL_PILOT_DBURL='mongodb://user:user@ds223760.mlab.com:23760/adaptivity'
export RADICAL_PILOT_PROFILE=True
export RADICAL_ENMD_PROFILE=True
export RADICAL_ENMD_PROFILING=1
export RP_ENABLE_OLD_DEFINES=True

export RADICAL_ENTK_VERBOSE='DEBUG'
export RADICAL_SAGA_VERBOSE='DEBUG'
export RADICAL_PILOT_VERBOSE='DEBUG'

python rfe.py  &> rfe.rp.session.log
