from lib.codecs.rle.main import Rle

rle = Rle(2000)
rle.archive('filetest.txt', 'byte_file.txt')
rle.dearchive('byte_file.txt', 'control.txt')
rle.archive('test.png', 'byte_file_png.txt')
rle.dearchive('byte_file_png.txt', 'control.png')
rle.archive(r'C:\projects\doka_archive\lib\codecs\rle\tests\Noize MC - Работа.mp3', 'byte_file_mp3.txt')
rle.dearchive('byte_file_mp3.txt', 'control.mp3')


