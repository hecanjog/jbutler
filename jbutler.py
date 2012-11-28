from pippi import dsp

dsp.quiet = False
dsp.timer('start')
dsp.seed('jbutler')

cathedral = dsp.read('sounds/cathedral.wav')

def fracture(snd):
    numpoints = dsp.randint(3, 20)
    poscurve = dsp.breakpoint([0] + [dsp.rand() for i in range(4)] + [0], numpoints)
    poscurve = [ p * (dsp.flen(snd) - dsp.mstf(210)) for p in poscurve ]

    lencurve = dsp.breakpoint([0] + [dsp.rand() for i in range(4)] + [0], numpoints)
    lencurve = [ l * dsp.mstf(200) + dsp.mstf(10) for l in lencurve ]

    pancurve = dsp.breakpoint([0] + [dsp.rand() for i in range(4)] + [0], numpoints)

    speeds = [1.0, 2.0, 0.5, 0.75]

    grains = [ dsp.cut(snd, poscurve[i], lencurve[i]) for i in range(numpoints) ]
    grains = [ dsp.pan(grains[i], pancurve[i]) for i in range(numpoints) ]
    grains = [ dsp.env(grain, 'gauss', True) for grain in grains ]
    grains = [ dsp.transpose(grain, dsp.randchoose(speeds)) for grain in grains ]

    etypes = ['line', 'phasor', 'tri', 'sine', 'gauss']

    snd = dsp.env(''.join(grains), dsp.randchoose(etypes))
    snd = dsp.pad(snd, 0, dsp.mstf(dsp.rand(100, 400)))

    return snd

def smear(snd):
    snd = dsp.split(snd, dsp.mstf(dsp.rand(3000, 6000)))
    snd = dsp.randshuffle(snd)
    snd = [ dsp.env(s) for s in snd ]
    snd = [ s * dsp.randint(1, 4) for s in snd ]

    return dsp.drift(''.join(snd), dsp.rand(0.01, 0.1))

out = ''

out += dsp.mix([ ''.join([ fracture(cathedral.data) for i in range(100) ]) for i in range(3) ])

out += dsp.mix([ smear(cathedral.data) for i in range(10) ])

dsp.write(out, 'jj', False)

dsp.timer('stop')
