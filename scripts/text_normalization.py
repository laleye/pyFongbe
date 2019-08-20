import os, unicodedata, argparse, sys, datetime

class text_normalization(object):
    
    def __init__(self):
        self.special_characters = {'ὲ':'ε', 'έ': 'ε', 'ɛ̆': 'ε', 'ε': 'ε', 'ɖ': 'ɖ', 'ɔ́':'ɔ', 'ɔ': 'ɔ', 'ɔ̆': 'ɔ', 'ɔ̀': 'ɔ', 'ĭ': 'i', 'í': 'i', 'ì': 'i', 'ĕ': 'e', 'ŭ': 'u', 'ĕ': 'e', 'é': 'e', 'è': 'e', 'ı́': 'i', 'ˋ': '', "'": '', 'ú': 'u', 'ù': 'u', 'ó': 'o', 'â': 'a', 'ô', 'o', 'ò': 'o'}
        self.french_list = 'abcdefghijklmnopqrstuvwxyz'
    
    def remove_accents_from_file(self, input_):
        content = list()
        if not os.path.exists(input_):
            sys.exit("[text_normalization error: {} doesn't exist]".format(input_))
        else:
            with open(input_, 'r', encoding='utf8') as in_:
                for i, line in enumerate(in_):
                    texts = line.strip().split()
                    text_ = ''
                    for word in texts:
                        len_wi = len(word)
                        try:
                            word_ = self.encode_ascii(word) 
                            if len(word_) == len_wi:
                                text_ = "{} {}".format(text_, word_)
                                print(i)
                            else:
                                word = [self.special_characters[w] if w in self.special_characters.keys() else w for w in word ]
                                word = ''.join(word)
                                chw = [w for w in word if w not in self.special_characters.keys() and w not in self.french_list]
                                if len(chw) > 0:
                                    chw = ''.join(chw)
                                    with open('oocs.txt', 'a') as ff:
                                        ff.write(chw+'\n')
                                text_ = "{} {}".format(text_.strip(), word)
                                #word_ = self.encode_ascii(word) 
                                #if len(word_) == len_wi:
                                    #text_ = "{} {}".format(text_, word_)
                                    #print(i)
                                #else:
                                    #sys.exit("[text_normalization error: problem with processing of {} from line {} in {}]".format(word, i, input_))
                        except:
                            sys.exit("[text_normalization error: problem with processing of {} from line {} in {}]".format(word, i, input_))
                    content.append(text_)
        return content
    
    
    def remove_accents_from_list(self, lst_textes):
        content = list()
        for i, line in enumerate(lst_textes):
            texts = line.strip().split()
            text_ = ''
            for word in texts:
                len_wi = len(word)
                try:
                    word_ = self.encode_ascii(word) 
                    if len(word_) == len_wi:
                        text_ = "{} {}".format(text_, word_)
                        print(i)
                    else:
                        word = [self.special_characters[w] if w in self.special_characters.keys() else w for w in word ]
                        word = ''.join(word)
                        chw = [w for w in word if w not in self.special_characters.keys() and w not in self.french_list]
                        if len(chw) > 0:
                            chw = ''.join(chw)
                            with open('oocs.txt', 'a') as ff:
                                ff.write(chw+'\n')
                        text_ = "{} {}".format(text_.strip(), word)
                except:
                    sys.exit("[text_normalization error: problem with processing of {} from line {} in {}]".format(word, i, input_))
            content.append(text_)
        return content
    
    def save_in_file(self, content, filename):
        try:
            with open(filename, 'a', encoding='utf8') as f:
                for line in content:
                    f.write(line+'\n')
        except:
            sys.exit("[text_normalization error: problem with {}]".format(filename))
                            
                    
                    
    def encode_ascii(self, w):
        word = unicodedata.normalize('NFD', w)
        word = word.encode('ascii', 'ignore')
        word = word.decode('utf8')
        return word

    def process_texts(self, input_filename, output_filename):
        lines = self.remove_accents_from_file(input_filename)
        self.save_in_file(lines, output_filename)
        
    def process_kaldi_text_file(self, filename, transcript=False):
        texts = list()
        targets = list()
        with open(filename, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip().split()
                target = targets.append(line[0])
                texts.append(' '.join(line[1:]))
        contents = self.remove_accents_from_list(texts)
        outfilename = 'text-{date:%Y-%m-%d_%H:%M:%S}.txt'.format( date=datetime.datetime.now() )
        if transcript:
            with open('alltranscripts.txt', 'a', encoding='utf8') as f:
                for line in contents:
                    f.write("{}\n".format(line))
        else:
            with open(outfilename, 'a', encoding='utf8') as f:
                for i, content in enumerate(contents):
                    f.write('{} {}\n'.format(targets[i].strip(), content.strip()))
                
                
        
    
        


if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    #parser.add_argument('input', help='input file')
    #parser.add_argument('output', help='output file')
    
    #args = parser.parse_args()
    
    #print(sys.argv[0])
    if sys.argv[1] == '-t':
        tn = text_normalization()
        tn.process_kaldi_text_file(sys.argv[2], transcript=True)
    elif len(sys.argv) < 1:
        raise SyntaxError("Insufficient arguments.")
    elif len(sys.argv) == 2:
        tn = text_normalization()
        tn.process_kaldi_text_file(sys.argv[1])
    elif len(sys.argv) == 3:
        tn = text_normalization()
        tn.process_texts(sys.argv[1], sys.argv[1])
