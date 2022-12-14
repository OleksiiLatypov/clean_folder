import sys
import re
from pathlib import Path
import shutil



# check for correct user input
if len(sys.argv) != 2:
    print('Please provide correct path')
    quit()


# translate cyrillic symbols

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_")

TRANS = {}
for c, t in zip(tuple(CYRILLIC_SYMBOLS), TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()


def normalize(file: str) -> str:
        file = file.translate(TRANS)     # change letters
        file = re.sub(r'\W', '_', file)  # replace any no alphanumeric symbols to '_'
        return file

# extensions for validation
archive_ext =  ['ZIP', 'GZ', 'TAR']
image_ext = ['JPEG', 'PNG', 'JPG', 'SVG']
video_ext = ['AVI', 'MP4', 'MOV', 'MKV']
document_ext = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
music_ext = ['MP3', 'OGG', 'WAV', 'AMR']



p = Path(sys.argv[1])   # transfer our path

# create folder for sorted and normalized files
ARCHIVES = p / 'archives'
ARCHIVES.mkdir(exist_ok=True, parents=True)
#print(ARCHIVES)

IMAGES = p / 'images'
IMAGES.mkdir(exist_ok=True, parents=True)

VIDEO = p / 'video'
VIDEO.mkdir(exist_ok=True, parents=True)

AUDIO = p / 'audio'
AUDIO.mkdir(exist_ok=True, parents=True)

DOCUMENTS = p / 'documents'
DOCUMENTS.mkdir(exist_ok=True, parents=True)

OTHER = p / 'other'
OTHER.mkdir(exist_ok = True, parents = True)

image_list = []
video_list = []
document_list = []
music_list = []
other_ext_list = []

# scan our input folder
def read_folder(p):
    # list of files and directories in directory
    files = [x.rename(p / Path(normalize(x.stem) + x.suffix)) for x in p.iterdir()]
    #print(files) just for check
    for file in files:
        if file.is_dir():
            # recursive read directory
            read_folder(file)
            # check for empty folder
            try:
                if file.suffix == '' and file not in (AUDIO, VIDEO, ARCHIVES, OTHER, IMAGES, DOCUMENTS):
                    file.rmdir()
            except:
                print('FOLDER IS NOT EMPTY')
        # check for extensions
        elif file.suffix[1:].upper() in image_ext:
            try:
                shutil.move(file.rename(p / Path(normalize(file.stem) + file.suffix)), IMAGES)
            except:
                print(f'{file} is already in folder images')

        elif file.suffix[1:].upper() in video_ext:
            try:
                shutil.move(file.rename(p / Path(normalize(file.stem) + file.suffix)), VIDEO)
            except:
                print(f'{file} is already in folder video')

        elif file.suffix[1:].upper() in document_ext:
            try:
                shutil.move(file.rename(p / Path(normalize(file.stem) + file.suffix)), DOCUMENTS)
            except:
                print(f'{file} is already in folder documents')

        elif file.suffix[1:].upper() in music_ext:
            try:
                shutil.move(file.rename(p / Path(normalize(file.stem) + file.suffix)), AUDIO)
            except:
                print(f'{file} is already in folder audio')
        elif file.suffix[1:].upper() in archive_ext:
            try:
                shutil.unpack_archive(file.rename(p / Path(normalize(file.stem) + file.suffix)), ARCHIVES / file.stem)
            except:
                print(f'{file} is already in folder!')
        else:
            try:
                shutil.move(file.rename(p / Path(normalize(file.stem) + file.suffix)), OTHER)
            except:
                print(f'{file} is already in foder other')
    return image_list, video_list, document_list, music_list, other_ext_list

if __name__ == '__main__':
    print(f'Start in folder {p}')
    read_folder(Path(p))
