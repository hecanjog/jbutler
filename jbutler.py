from pippi import dsp
from pippi import tune
import math

dsp.quiet = False
dsp.timer('start')
dsp.seed('jbutler')

cathedral = dsp.read('sounds/cathedral.wav')

def fade(snd, time=dsp.mstf(1)):
    first = dsp.cut(snd, 0, time)
    middle = dsp.cut(snd, time, dsp.flen(snd) - (time * 2))
    last = dsp.cut(snd, dsp.flen(middle) + time, time)

    snd = dsp.env(first, 'line') + middle + dsp.env(last, 'phasor')
    
    return snd

def ding(length=44100, notes=[['g', 3], ['a', 4], ['e', 3]]):
    tone = dsp.read('sounds/ding.wav').data

    freqs = [ tune.ntf(note[0], note[1]) / tune.ntf('g', 3) for note in notes ]

    tones = [ dsp.transpose(tone, freq) for freq in freqs ]
    tones = [ dsp.cut(tones[i % len(tones)], dsp.mstf(dsp.rand(0, 100)), length + dsp.randint(0, 1000)) for i in range(32) ]

    tones = [ dsp.drift(tone, 0.03) for tone in tones ]

    tones = [ fade(tone) for tone in tones ]
    
    return ''.join(tones) 

def slurp(snd):
    snd = dsp.split(snd, dsp.flen(snd) / 100)
    numcycles = len(snd)
    curve_a = dsp.breakpoint([1.0] + [dsp.rand(0.1, 1.0) for r in range(dsp.randint(2, 10))] + [0], numcycles)
    curve_b = dsp.wavetable('cos', numcycles)
    wtable = [ curve_a[i] * curve_b[i] for i in range(numcycles) ]
    wtable = [ math.fabs((f * 5) + 0.75) for f in wtable ]

    snd = [ dsp.transpose(snd[i], wtable[i]) for i in range(numcycles) ]

    return ''.join(snd)

def fracture(snd):
    numpoints = dsp.randint(3, 20)
    poscurve = dsp.breakpoint([0] + [dsp.rand() for i in range(4)] + [0], numpoints)
    poscurve = [ p * (dsp.flen(snd) - dsp.mstf(210)) for p in poscurve ]

    lencurve = dsp.breakpoint([0] + [dsp.rand() for i in range(4)] + [0], numpoints)
    lencurve = [ l * dsp.mstf(200) + dsp.mstf(10) for l in lencurve ]

    pancurve = dsp.breakpoint([0] + [dsp.rand() for i in range(4)] + [0], numpoints)

    prepadcurve = dsp.breakpoint([0] + [dsp.rand() for i in range(4)] + [0], numpoints)
    prepadcurve = [ int(p * dsp.mstf(20)) for p in prepadcurve ]

    postpadcurve = dsp.breakpoint([0] + [dsp.rand() for i in range(4)] + [0], numpoints)
    postpadcurve = [ int(p * dsp.mstf(20)) for p in postpadcurve ]

    speeds = [1.0, 2.0, 0.5, 0.75]

    grains = [ dsp.cut(snd, poscurve[i], lencurve[i]) for i in range(numpoints) ]
    grains = [ dsp.pan(grains[i], pancurve[i]) for i in range(numpoints) ]
    grains = [ dsp.env(grain, 'gauss', True) for grain in grains ]
    grains = [ dsp.transpose(grain, dsp.randchoose(speeds)) for grain in grains ]
    grains = [ dsp.pad(grains[i], prepadcurve[i], postpadcurve[i]) for i in range(numpoints) ]

    for i in range(numpoints):
        if dsp.randint(0, 3) == 0:
            grains[i] = slurp(grains[i])

    etypes = ['line', 'phasor', 'tri', 'sine', 'gauss']

    snd = dsp.env(''.join(grains), dsp.randchoose(etypes))
    snd = dsp.pad(snd, 0, dsp.mstf(dsp.rand(100, 400)))

    return snd

def smear(snd):
    snd = dsp.split(snd, dsp.mstf(dsp.rand(5000, 10000)))
    snd = dsp.randshuffle(snd)
    snd = [ dsp.env(s) for s in snd ]
    snd = [ s * dsp.randint(1, 8) for s in snd ]

    return dsp.drift(''.join(snd), dsp.rand(0.01, 0.1))

out = ''

#sparks = dsp.mix([ ''.join([ fracture(cathedral.data) for i in range(20) ]) for i in range(3) ])

smears = dsp.mix([ smear(cathedral.data) for i in range(10) ])

notes = [
        ['g', 3],
        ['a', 4],
        ['e', 3],
        ['d', 4],
        ]

l1 = ding(30000, notes)

notes = [
        ['e', 4],
        ['d', 4],
        ['a', 4],
        ]

l2 = ding(20000, notes)

dings = dsp.mix([l1, l2])

out = dsp.mix([dsp.amp(dings, 0.5), smears])

dsp.write(out, 'jj', False)

dsp.timer('stop')
