import wave, os, argparse
import contextlib

def main(data_folder):
    home = data_folder
    folders = ['train/wav', 'test/wav']
    fduration = 0
    for folder in folders:
        directory = os.path.join(home, folder)
        folder_duration = 0
        for subdir in os.listdir(directory):
            subdir = os.path.join(directory, subdir)
            subduration = 0
            for fname in os.listdir(subdir):
                fname = os.path.join(subdir, fname)
                if 'wav' in fname:
                    with contextlib.closing(wave.open(fname,'r')) as f:
                        frames = f.getnframes()
                        rate = f.getframerate()
                        duration = frames / float(rate)
                    subduration = subduration + duration
            
            folder_duration = folder_duration + subduration
        print('{} > {}'.format(folder, folder_duration/3600.045))
        fduration = fduration + folder_duration
    print('total duration : {}'.format(fduration/3600.045))
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('data_folder', help='data folder')
    
    args = parser.parse_args()
    
    main(args.data_folder)
        
