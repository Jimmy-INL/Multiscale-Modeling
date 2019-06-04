from random import *
from math import *
import numpy as np
import os
from sets import Set
import multiprocessing
import time
start_time = time.time()
print'\n>>>\tMultiscale Modelling, Microscale\n',
def CreateNewRVEModel():

    # Creates RVE model and orphanmesh. Lage 2D RVE shell, meshe RVE, extrudere til 3D part, lage orphanmesh og sette cohesive elementtype paa Interface
    execfile(Modellering+'RVEsketching.py')             # Lage 2D RVE fra fiberpopulasjon data
    execfile(Modellering+'RVEmeshpart.py')              # Meshe 2D RVE  til 3D part, lage orphan mesh part
    p = mod.parts[meshPartName]
    execfile(Modellering+'RVEelementsets.py')           # Fiber, sizing og matrix elementer i set og Fiber center datums for material orientation
    execfile(Modellering + 'RVEproperties.py')          # Sett materialegenskaper for elementset
    execfile(Modellering + 'RVE_Assembly_RP_CE.py')     # Assembly med RVE med x i fiber retning. Lage constrain equations til RVE modell og fixe boundary condition for rigid body movement
    if not noFiber and Interface:                       # Rearrange fiber interface nodes for controlled elementthickness and stable simulations
        execfile(Modellering + 'RVE_InterfaceElementThickness.py')
    execfile(Modellering + 'RVE_Boundaryconditions.py') # Boundaryconditions mot rigid body movement
def run_Job(Jobb, modelName):
    mdb.Job(name=Jobb, model=modelName, description='', type=ANALYSIS,
            atTime=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=numCPU,
            numDomains=numCPU, numGPUs=1)
    if Runjobs:
        try:
            mdb.jobs[Jobb].submit(consistencyChecking=OFF)
            mdb.jobs[Jobb].waitForCompletion()
            path = workpath + Jobb
            odb = session.openOdb(path + '.odb')
            fras = odb.steps[stepName].frames[-1]
        except:
            error=1
            pass
    else:
        mdb.jobs[Jobb].writeInput(consistencyChecking=OFF)
def Iterasjonfiks():
    global Jobsss
    Jobsss = workpath + 'Abaqusjobs.bat'
    Itra = open(Tekstfiler + 'Iterasjoner.txt', "r")
    Content = Itra.read()
    cals = Content.split('\n')
    number = len(cals) - 1
    Itra.close()
    InterestingParameter = 'ItraPara'
    Itra = open(Modellering + 'IterationParameters.py', "w")
    Itra.write('global ' + InterestingParameter + '\n' + InterestingParameter + ' = ' + str(int(number)))
    Itra.close()
def FrameFinder():
    limit = 0.05
    print Sigmapaths
    StressSi = np.genfromtxt(Sigmapaths)
    StressSi = StressSi[1:, 1:]
    for a in range(0, 6):
        if not (a == Ret[0] or a == Ret[1]):
            StressSi[1:, a] = np.multiply(StressSi[1:, a], 1 / StressSi[1:, Ret[0]])
    Sing = [0]*6
    Dob = [0]*6
    Trecharm = [0]*6
    StressFlags = [0]*6
    for kj in range(0,len(StressSi)):
        for sa in range(0,len(StressSi[0])):
            if not (sa==Ret[0]or sa==Ret[1]):
                if not Trecharm[sa]:
                    if not Dob[sa]:
                        if not Sing[sa]:
                            if abs(StressSi[kj][sa]) > limit:
                                Sing[sa]=1
                        else:
                            if abs(StressSi[kj][sa]) > limit:     #   Feilmargin
                                Dob[sa] = 1
                            else:
                                Sing[sa]=0
                    else:
                        if abs(StressSi[kj][sa]) > limit:  # Feilmargin
                            Trecharm[sa] = 1
                        else:
                            Sing[sa] = 0
                            Dob[sa] = 0
                else:
                    StressFlags[sa] = 1
        for sa in range(0, len(StressSi[0])):
            if StressFlags[sa]:
                return kj - 4, StressFlags, StressSi[kj-4]

    for sa in range(0, len(StressSi[0])):
        if Dob[sa]:
            return len(StressSi) - 2, Dob, StressSi[kj]
        if Sing[sa]:
            return len(StressSi) - 1, Sing, StressSi[kj]
    #del Ididtifying_diverging_frame_did_notwork
    print 'No divergence found'
    return len(StressSi)-1, StressFlags, StressSi[len(StressSi)-1]

# Intiering
GitHub = 'C:/Users/sondreor/Documents/GitHub/'
try:
    execfile(GitHub + 'Multiscale-Modeling/Abaqus_modellering/Init.py')
    execfile(Modellering + 'Initial.py')
except:
     if not error:
        print 'Feil i initiering'
        error=1
print '\tInitieringstid =', np.round(time.time() - start_time,)
ParameterSweep = SweepParametere[0]
n = [int(ParameterSweep * scsc + ItraPara * 169)]
ItraPara = 0
tests = 1  # Antall iterasjoner per startup

  # Arbeids lokke

while len(n)<=tests:
    #IMPORTERER ALT FRA ABAQUS
    from abaqus import *
    from abaqusConstants import *
    from odbAccess import *
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    execfile(Modellering + 'Multilucke.py')