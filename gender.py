import glob
import nltk
import string

class Gender(object):
    
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'
    BOTH = 'both'

    MALE_WORDS=set(['guy','spokesman','chairman',"men's",'men','him',"he's",'his',
              'boy','boyfriend','boyfriends','boys','brother','brothers','dad',
              'dads','dude','father','fathers','fiance','gentleman','gentlemen',
              'god','grandfather','grandpa','grandson','groom','he','himself',
              'husband','husbands','king','male','man','mr','nephew','nephews',
              'priest','prince','son','sons','uncle','uncles','waiter','widower',
              'widowers'])
    
    FEMALE_WORDS=set(['heroine','spokeswoman','chairwoman',"women's",'actress','women',
                "she's",'her','aunt','aunts','bride','daughter','daughters','female',
                'fiancee','girl','girlfriend','girlfriends','girls','goddess',
                'granddaughter','grandma','grandmother','herself','ladies','lady',
                'lady','mom','moms','mother','mothers','mrs','ms','niece','nieces',
                'priestess','princess','queens','she','sister','sisters','waitress',
                'widow','widows','wife','wives','woman'])
    
    @classmethod
    def genderize(self, words):
        
        mwlen = len(self.MALE_WORDS.intersection(words))
        fwlen = len(self.FEMALE_WORDS.intersection(words))

        if mwlen > 0 and fwlen == 0:
            return self.MALE
        elif mwlen == 0 and fwlen > 0:
            return self.FEMALE
        elif mwlen > 0 and fwlen > 0:
            return self.BOTH
        else:
            return self.UNKNOWN

class WordCase(object):

    UPPER = 'upper'
    LOWER = 'lower'
    
    def __init__(self):
        self._data = { }

    def __getitem__(self, key):
        return self._data[key.lower()]

    def __setitem__(self, key, val):
        raise Exception("Cannot set items directly, use increment or decrement methods")

    def __contains__(self, key):
        return key in self._data

    def get_case(self, word):
        case = self.UPPER if word[0].isupper() else self.LOWER
        word = word.lower()

        if word not in self:
            self._data[word] = {self.UPPER:0, self.LOWER:0}
        return case

    def increment(self, word):
        case = self.get_case(word)
        word = word.lower()
        self._data[word][case] += 1

    def decrement(self, word):
        case = self.get_case(word)
        word = word.lower()
        if self._data[word][case] > 0:
            self._data[word][case] -= 1

class Counters(object):
    
    def __init__(self):
        
        sexes = [Gender.MALE, Gender.FEMALE, Gender.UNKNOWN, Gender.BOTH]
        
        self.sents = {sex:0 for sex in sexes}
        self.words = {sex:0 for sex in sexes}
        self.wfreq = {sex:{} for sex in sexes}
        self.wcase = WordCase()

    def handle_sentence(self, sentence):
        gender = Gender.genderize(set([w.lower() for w in sentence]))
        self.sents[gender] += 1
        self.words[gender] += len(sentence)

        for idx, word in enumerate(sentence):
            self.wfreq[gender][word] = self.wfreq[gender].get(word, 0) + 1
            if idx < 1: continue
            self.wcase.increment(word)

class GenderParser(object):
    
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    
    def __init__(self, path):
        self.path = path
        self.counters = Counters()

    def parse(self):
        with open(self.path, 'rb') as text:
            for sentence in self.tokenizer.tokenize(text.read()):
                sentence = self.unpunct(sentence)
                sentence = sentence.split()
                self.counters.handle_sentence(sentence)

    def unpunct(self, s):
        return s.translate(string.maketrans("", ""), string.punctuation)

if __name__ == "__main__":

    parser = GenderParser('doyle.txt')
    parser.parse()

    print "%(male)i male sentences, %(female)i female sentences, %(unknown)i unknown, and %(both)i both." % parser.counters.sents
