# Sette variabler
execfile(Modellering + 'TestVariabler.py')

# INFO DUMP
if Interface and Createmodel and not noFibertest:
    print 'Interface elements aspect ratio: ' + str(round(meshsize / (rinterface * rmean), 2))
    print 'Interface element thickness    : ' + str(float(ElementInterfaceT * rmean))
if not noFibertest and FiberSirkelResolution < 20:
    print
    'Feil, For grov opplosning, avslutter..'
    error =1

if nf == 0 or Vf == 0 or noFibertest:
    nf = 0
    Vf = 0
    dL = rmean * 4
    noFiber = 1
if not nf == 0:  # RVE dL er relativ av nf, rmean og V
    dL = ((nf * pi * rmean ** 2) / (Vf)) ** 0.5
    noFiber = 0


