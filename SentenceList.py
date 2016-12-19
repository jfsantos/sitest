class SentenceList:
    """This class just converts the Harvard sentence list in txt format to a Python dictionary."""

    def __init__(self, filepath):
        txt = file(filepath).readlines()
        list_idx = 0
        self.sentences = {}
        for line in txt:
            if line.startswith('H'):
                list_idx += 1
            else:
                line = line.strip().split('.')
                sentence_idx = int(line[0])
                sentence_txt = line[1].strip()
                sentence_name = 'S_%02d_%02d' % (list_idx, sentence_idx)
                self.sentences[sentence_name] = sentence_txt
