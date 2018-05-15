"""Relative free energy calculations

Example implementation using Abigail and NAMD.

"""
import os
import sys

import numpy as np

from htbac import Runner, System, Simulation, Protocol, AbFile
from htbac.protocols import Rfe


def run_rfe():
    sys_names = sys.argv[1:-1]
    systems = list()
    for sys_name in sys_names:
    
        folder = os.path.abspath('../systems/{}'.format(sys_name))
        pdb = AbFile('{}/complex.pdb'.format(folder), tag='pdb').with_prefix(sys_name)
        top = AbFile('{}/complex.top'.format(folder), tag='topology').with_prefix(sys_name)
        tag = AbFile('{}/tags.pdb'.format(folder), tag='alchemicaltags').with_prefix(sys_name)
        cor = AbFile('{}/complex.crd'.format(folder), tag='coordinate').with_prefix(sys_name)
        system = System(name=sys_name, files=[pdb, top, tag, cor])
        systems.append(system)
        
    p = Protocol(clone_settings=False)

    for step, numsteps in zip([Rfe.step0, Rfe.step1, Rfe.step1, Rfe.step1, Rfe.step1, Rfe.step1, Rfe.step1], [10000, 1000, 1000, 1000, 1000, 10000,  3000000]):

        rfe = Simulation()
        rfe.engine = 'namd_mpi'
        rfe.cores = 32

        rfe.cutoff = 12.0
        rfe.switchdist = 10.0
        rfe.pairlistdist = 13.5
        rfe.numsteps = numsteps

        rfe.add_input_file(step, is_executable_argument=True)

        rfe.add_ensemble('replica', range(5))
        rfe.add_ensemble('lambdawindow', np.linspace(0, 1, 65))
        rfe.add_ensemble('system', systems)
        
        p.append(rfe)

    ht = Runner('bw_aprun', comm_server=('two.radical-project.org', int(sys.argv[-1])))
    ht.add_protocol(p)
    ht.run(walltime=1440, queue='high')


if __name__ == '__main__':

    if len(sys.argv) < 3:
        raise ValueError
    
    run_rfe()
