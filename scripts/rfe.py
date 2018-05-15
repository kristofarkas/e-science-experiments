"""Relative free energy calculations

Example implementation using Abigail and NAMD.

"""

import numpy as np

from htbac import Runner, System, Simulation, Protocol, AbFile
from htbac.protocols import Rfe


def run_rfe():
    # SET THIS!
    sys_name = ''
    pdb = AbFile('../systems/complex.pdb', tag='pdb').with_prefix(sys_name)
    top = AbFile('../systems/complex.top', tag='topology').with_prefix(sys_name)
    tag = AbFile('../systems/tags.pdb', tag='alchemicaltags').with_prefix(sys_name)
    cor = AbFile('../systems/complex.crd', tag='coordinate').with_prefix(sys_name)
    system = System(name=sys_name, files=[pdb, top, tag, cor])

    p = Protocol(clone_settings=False)

    for step, numsteps in zip(Rfe.steps, [5000, 3000000]):

        rfe = Simulation()
        rfe.system = system
        rfe.engine = 'namd_mpi'
        rfe.cores = 32

        rfe.cutoff = 12.0
        rfe.switchdist = 10.0
        rfe.pairlistdist = 13.5
        rfe.numminsteps = 5000
        rfe.numsteps = numsteps

        rfe.add_input_file(step, is_executable_argument=True)

        rfe.add_ensemble('replica', range(5))
        rfe.add_ensemble('lambdawindow', np.linspace(0, 1, 65))

        p.append(rfe)

    ht = Runner('bw_aprun', comm_server=('two.radical-project.org', 33174))
    ht.add_protocol(p)
    ht.run(walltime=1440, queue='high')


if __name__ == '__main__':
    run_rfe()
