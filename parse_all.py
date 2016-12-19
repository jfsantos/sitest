from ResultsParser import ResultsParser

pids = range(1,11)
results = []

for x in pids:
    p = ResultsParser("/home/jfsantos/Dropbox/INRS/Summer 2013/Thesis/participant_%d.dat" % x)
    results.append(p.process())

keys = results[0].keys()

for key in keys:
    x = [y.get(key) for y in results]
    print '%s: %2.1f' % (key, 100*sum(x)/len(x))
