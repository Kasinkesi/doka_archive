# relative import:
# from ..rle import *
from lib.codecs.rle.rle import *

rle = Rle()
rle.compress_file(r'C:\projects\doka_archive\tests\data\filetest.txt', r'C:\projects\doka_archive\tests\data\bytefile.txt')
rle.decompress_file(r'C:\projects\doka_archive\tests\data\bytefile.txt', r'C:\projects\doka_archive\tests\data\control.txt')
rle.compress_file(r'C:\projects\doka_archive\tests\data\test.png', r'C:\projects\doka_archive\tests\data\bytefile_png.txt')
rle.decompress_file(r'C:\projects\doka_archive\tests\data\bytefile_png.txt', r'C:\projects\doka_archive\tests\data\control.png')
rle.compress_file(r'C:\projects\doka_archive\tests\data\Noize MC - Работа.mp3', r'C:\projects\doka_archive\tests\data\bytefile_mp3.txt')
rle.decompress_file(r'C:\projects\doka_archive\tests\data\bytefile_mp3.txt', r'C:\projects\doka_archive\tests\data\control.mp3')
try:
    rle.decompress_file(r'C:\projects\doka_archive\tests\data\broken_bytefile.txt', 'broken_control.txt')
except MagicMismatchError:
    print(sys.exc_info()[0:2])

