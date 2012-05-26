#possibly use analysis.windowed or analysis.discrete?

import rules

class rule_crawler(object):
    def __init__(self, score, ruleset):
        self.score = score
        self.ruleset = []
        self.direction = kwargs.get('direction','backward')

        self.total_length
        self.rule_max
        self.rule_min

        self._load_score()
        self._load_rules(ruleset)

    def _load_score(self):
        self.total_length = len(score._fbline_stream.flat.getElementsByClass(note.Note))
        self.rule_min = self.total_length

    def _load_rules(self):
        self.ruleset = rules.getRules(self.ruleset) #TODO
        for rule in self.ruleset:
            if rule.size > self.rule_max: self.rule_max = rule.size
            if rule.size < self.rule_min: self.rule_min = rule.size

    def _chunkify(self,start_index,end_index):
        chunk.intervals = []
        chunk.content = []
        chunk.extra = []
        chunk.
        return chunk

    def apply_rules(self,where='notes'):
        applying = True

        while applying == True:

            #get chunk
            START = 1 #TODO
            END = 5 #TODO
            chunk = self.score._chunkify(START,END)
            if True: applying = False #todo update

            #for each rule in rules, try rule
            for rule in self.ruleset:
                figures = rule.test_rule(chunk)
                LOG.info("%s is %s at chunk for range %s - %s", rule.__class__.__name__, str(figures), str(START), str(END))
                if figures:
                    #write to notes? #write to log?
                    #For now, notes (make optional)
                    for i in range(len(figures)):
                        score_note_[i].addlyricssomehow(figures[i])


