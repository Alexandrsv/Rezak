"""Справка программы Резак.
Usage:
  main.py [-h] [--sensitivity=SENS]
          [--postfix=POSTFIX]
          [--void=PIXEL | --color=COLOR]
          FILES...

Arguments:
  FILES  Файлы для обработки, обязательный параметр, можно указывать несколько

Options:
  -h --help                 Показать эту справку
  --sensitivity=SENS        Чувствительность алгоритма. от 1 до 128, 1 - максимальная [default: 1]
  --void=PIXEL              Координаты пикселя из рамки [default: 1,1]
  --postfix=POSTFIX         Координаты пикселя из рамки [default: crop]
  --color=COLOR             Цвет рамки HEX  [default: False]

Example, try:
  main.py --postfix=crop --sensitivity=2 --void=1,1 ./demo.png ./demo2.png
  main.py ./demo.png
"""

import sys

from PIL import Image
from pathlib import Path
from docopt import docopt

def crop(image, new_filename):
    pix = image.load()
    print(f'{image.format=}', f'{image.size=}', f'{image.mode=}')
    print('Размер изображения', image.size[0], image.size[1])

    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту

    up, bottom, left, right = -1, -1, -1, -1
    color = [pix[1, 1][0], pix[1, 1][1], pix[1, 1][2]]
    print('Цвет пикселя (1,1)', f'{color=}')

    for y in range(height):
        if up < 0:
            for x in range(width):
                # print('2', x, y, [pix[x, y][0], pix[x, y][1], pix[x, y][2]])
                if color != [pix[x, y][0], pix[x, y][1], pix[x, y][2]]:
                    up = y - 1
                    break

    for y in reversed(range(height)):
        if bottom < 0:
            for x in range(width):
                if color != [pix[x, y][0], pix[x, y][1], pix[x, y][2]]:
                    bottom = y + 1
                    break

    for x in range(width):
        if left < 0:
            for y in range(height):
                if color != [pix[x, y][0], pix[x, y][1], pix[x, y][2]]:
                    left = x - 1
                    break
    for x in reversed(range(width)):
        if right < 0:
            for y in range(height):
                if color != [pix[x, y][0], pix[x, y][1], pix[x, y][2]]:
                    right = x + 1
                    break

    print('Координаты обрезки', f'{up=} {bottom=} {left=} {right=}')
    image_crop = image.crop((left, up, right, bottom))
    image_crop.save(f'{new_filename}', "PNG")


def get_new_filename(path, postfix):
    return path.parent.joinpath(f'{path.stem}_{postfix}.png')


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    # file_path = Path(sys.argv[1])
    file_path = Path(arguments['FILES'][0])
    if not file_path.is_file():
        print(f"No such file or directory: {file_path}. Are u wrote it as in example? ")

    image = Image.open(file_path)
    new_filename = get_new_filename(file_path, arguments['--postfix'])
    print('\n===============!!===============')
    print(f'Пациент - {file_path}')
    crop(image=image, new_filename=new_filename)
