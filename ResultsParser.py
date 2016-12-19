
from cPickle import Unpickler
from SentenceList import SentenceList
from ConfigParser import ConfigParser
import re, string

class ResultsParser:

    def __init__(self, filepath):
        try:
            u = Unpickler(file(filepath))
            self.results = u.load()['results']
        except IOError, KeyError:
            self.results = None
        self.sentence_list = SentenceList('harvsents.txt')
    
    def process(self):
        # load lists
        cfg = ConfigParser()
        cfg.read('test.cfg')
        tested_lists = cfg.get('setup', 'lists').split()
        # variable to hold the mean intelligibility for each list
        list_intel = {}
        # load list items one by one and compute intelligibility scores
        for l in tested_lists:
            txt = file(l).readlines()
            test_sentences = map(string.strip,txt)
            intels = []
            for s in test_sentences:
                # testing if the key is present
                if self.results[l].has_key(s):
                    x = cleanup(self.results[l][s].lower())
                    print x
                    y = cleanup(self.sentence_list.sentences[clean_name(s)].lower())
                    print y
                    n_matches = len(filter(lambda b: b in y, x))
                    print 'Matches: %d/%d' % (n_matches, len(y))
                    intels.append(float(n_matches)/len(y))
                else:
                    print 'Key %s was not present' % s
                    intels.append(0.0)
            list_intel[l] = float(sum(intels))/len(intels)
        return list_intel
                    
def cleanup(x):
    return map(lambda a: filter(lambda b: b.isalpha(), a), x.split())
    
def clean_name(x):
    idx = re.search('S_[0-9]{2}_[0-9]{2}', x)
    return x[idx.start():idx.end()]
