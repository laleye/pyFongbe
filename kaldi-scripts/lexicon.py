import os

dict_directory = "data/local/dict"

if not os.path.exists(dict_directory):
    os.makedirs(dict_directory)
    
word_list = os.path.join(os.path.dirname(dict_directory), 'fongbe_wordlist.txt')
lexicon = os.path.join(dict_directory, 'lexicon.txt')
non_silence = os.path.join(dict_directory, 'nonsilence_phones.txt')
optional_silence = os.path.join(dict_directory, 'optional_silence.txt')
silence_phones = os.path.join(dict_directory, 'silence_phones.txt')

files = []

if os.path.exists(lexicon):
    os.remove(lexicon)
if os.path.exists(non_silence):
    os.remove(non_silence)
if os.path.exists(optional_silence):
    os.remove(optional_silence)
if os.path.exists(silence_phones):
    os.remove(silence_phones)
    
with open(lexicon, 'a', encoding='utf8') as fwrite:
    fwrite.write('!SIL SIL\n<UNK> SPN\n')

letters = list()
    
with open(word_list, 'r', encoding='utf8') as f:
    for line in f:
        line = line.strip()
        with open(lexicon, 'a', encoding='utf8') as fwrite:
            fwrite.write(line)
            for c in line:
                fwrite.write(' '+c)
                if c not in letters:
                    letters.append(c)
            fwrite.write('\n')
    
letters.sort()
with open(non_silence, 'a', encoding='utf8') as f:
    for letter in letters:
        f.write(letter+'\n')
        
with open(optional_silence, 'a', encoding='utf8') as f:
    f.write('SIL\n')
with open(silence_phones, 'a', encoding='utf8') as f:
    f.write('SIL\nSPN\n')

