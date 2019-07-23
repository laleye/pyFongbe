import argparse, os
import wave, contextlib, csv


FIELDNAMES = ['wav_filename', 'wav_filesize', 'transcript']

def getduration(wavfile):
    with contextlib.closing(wave.open(wavfile,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        
    return duration
    
    
def write_in_csv(data, output_csv):
    with open(output_csv, 'w') as output_csv_file:
        print('Writing CSV file for DeepSpeech.py as: ', output_csv)
        writer = csv.DictWriter(output_csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for filename, file_size, transcript in data:
            writer.writerow({'wav_filename': filename, 'wav_filesize': file_size, 'transcript': transcript})
       
def main(directory, textfile, datatype):
    data = list()
    with open(textfile, 'r', encoding='utf8') as in_:
        for line in in_:
            line = line.strip()
            filename = '{}.wav'.format(line.split()[0])
            transcript = ' '.join(line.split()[1:])
            dirname = filename.split('_')[0]
            wavfile = os.path.join(os.path.abspath(directory), os.path.join(dirname, filename))
            duration = getduration(wavfile)
            data.append((wavfile, duration, transcript))
    outputcsv = os.path.join(directory, '{}.csv'.format(datatype))
    write_in_csv(data, outputcsv)
                
            
        #print(entry.name)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('datadir', help='data folder')
    parser.add_argument('textfile', help='text filename')
    parser.add_argument('datatype', help='data type')
    #parser.add_argument('out', help='name of file to process')
    
    args = parser.parse_args()
    
    main(args.datadir, args.textfile, args.datatype)
