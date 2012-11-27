from pippi import dsp

dsp.quiet = False
dsp.timer('start')

cathedral = dsp.read('sounds/cathedral.wav')

out = dsp.mix([ dsp.transpose(cathedral.data, 1 + (( float(i) / 10 ) * 0.1)) for i in range(10) ])

dsp.write(out, 'jj', False)

dsp.timer('stop')
