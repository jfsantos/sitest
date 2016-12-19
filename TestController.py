from ConfigParser import ConfigParser
import string
from random import shuffle
from cPickle import Pickler

class TestController:
    """An instance of this class should be used to control a single
    test session. It is responsible for defining the presentation
    order of the samples and storing the results."""

    def __init__(self, participant_id=None):
        if participant_id is None:
            self.participant_id = 0
        else:
            self.participant_id = participant_id
        self.cfg = ConfigParser()
        self.cfg.read('test.cfg')
        self.test_sentences = {}
        self.sample_dir = self.cfg.get('setup','sample_dir')
        for slist in self.cfg.get('setup','lists').split():
            txt = file(slist).readlines()
            self.test_sentences[slist] = map(string.strip,txt)
            shuffle(self.test_sentences[slist])
        self.list_order = self.test_sentences.keys()
        shuffle(self.list_order)
        # TODO: add training list here (so it does not get shuffled.)
        self.train_list = self.cfg.get('setup','train')
        train_txt = file(self.train_list).readlines()
        train_sentences = map(string.strip, train_txt)
        self.test_sentences[self.train_list] = train_sentences
        self.list_order.insert(0, self.train_list)
        self.current_list_idx = 0
        self.current_sentence_idx = -1
        self.current_sample = 0
        self.total_samples = sum(len(l) for l in self.test_sentences.values())
        self.results = {}
    
    def next_sample(self):
        n_sentences_on_list = len(self.test_sentences[self.list_order[self.current_list_idx]])
        if self.current_sentence_idx < n_sentences_on_list - 1:
            self.current_sentence_idx += 1
        elif self.current_list_idx < len(self.list_order) - 1:
            self.current_sentence_idx = 0
            self.current_list_idx += 1
        else:
            self.pickle_results()
            raise IndexError('End of test samples.')
        self.current_sample += 1
        msg = '%d/%d' % (self.current_sample, self.total_samples)
        filepath = self.test_sentences[self.list_order[self.current_list_idx]][self.current_sentence_idx]
        return self.sample_dir + filepath, msg

    def is_training_sample(self):
        if self.current_sample < len(self.test_sentences[self.train_list]):
            return True
        else:
            return False
    
    def save_result(self, result):
        result_list = self.list_order[self.current_list_idx]
        result_sample = self.test_sentences[result_list][self.current_sentence_idx]
        if not self.results.has_key(result_list):
            self.results[result_list] = {}
            print 'Initializing result list for %s' % result_list
        print 'Saving results for sample %s @ %s: %s' % (result_sample, result_list, result)
        self.results[result_list][result_sample] = result

    def pickle_results(self):
        data = file('participant_%d.dat' % self.participant_id,'w')
        p = Pickler(data)
        experiment = {}
        experiment['test_sentences'] = self.test_sentences
        experiment['results'] = self.results
        p.dump(experiment)
    
