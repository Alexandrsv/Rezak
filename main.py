"""Справка программы Резак.
Usage:
  main.py [-hv] [--sensitivity=SENS]
          [--postfix=POSTFIX] [--verbose]
          [--void=PIXEL | --color=COLOR]
          FILES...

Arguments:
  FILES  Файлы для обработки, обязательный параметр, можно указывать несколько

Options:
  -h --help                 Показать эту справку
  --sensitivity=SENS        Чувствительность алгоритма. от 1 до 255,
                            1 - максимальная [default: 1]
  --void=PIXEL              Координаты пикселя из рамки [default: 1,1]
  --postfix=POSTFIX         Координаты пикселя из рамки [default: crop]
  --color=COLOR             Цвет рамки HEX  [default: False]
  --verbose                 Подробный вывод

Example, try:
  main.py --postfix=crop --sensitivity=2 --void=1,1 ./demo.png ./demo2.png
  main.py --sensitivity=200 --color=#FFFFFF demo.png
  main.py ./demo.png
"""

from PIL import Image, ImageColor
from pathlib import Path
from docopt import docopt


def get_color(pixels, x, y, sens):
    if isinstance(pixels[x, y], int):
        return pixels[x, y] // sens
    else:
        color = [pixels[x, y][0] // sens,
                 pixels[x, y][1] // sens,
                 pixels[x, y][2] // sens
                 ]
        return color


def crop(img, new_filename, arg):
    sens = int(arg['--sensitivity'])
    pix = img.load()
    if arg['--color'] == 'False':
        x, y = arg['--void'].split(',')
        x, y = int(x), int(y)
        color = get_color(pix, x, y, sens)
    else:
        color = ImageColor.getrgb(arg['--color'])
    if arg['--verbose']:
        print(f'{img.format=}', f'{img.size=}', f'{img.mode=}')
        print('Размер изображения', img.size[0], img.size[1])

    width = img.size[0]  # Определяем ширину
    height = img.size[1]  # Определяем высоту
    if arg['--verbose']:
        print(f'Цвет пустоты {color=}')

    up, bottom, left, right = -1, -1, -1, -1
    for y in range(height):
        if up < 0:
            for x in range(width):
                # print('2', x, y, [pix[x, y][0], pix[x, y][1], pix[x, y][2]])
                if color != get_color(pix, x, y, sens):
                    up = y - 1
                    break

    for y in reversed(range(height)):
        if bottom < 0:
            for x in range(width):
                if color != get_color(pix, x, y, sens):
                    bottom = y + 1
                    break

    for x in range(width):
        if left < 0:
            for y in range(height):
                if color != get_color(pix, x, y, sens):
                    left = x - 1
                    break
    for x in reversed(range(width)):
        if right < 0:
            for y in range(height):
                if color != get_color(pix, x, y, sens):
                    right = x + 1
                    break
    if arg['--verbose']:
        print('Координаты обрезки', f'{up=} {bottom=} {left=} {right=}')
    img_crop = img.crop((left, up, right, bottom))
    img_crop.save(f'{new_filename}', "PNG")
    print(f'Готово\nРезультат сохранен сюда - {new_filename}')


def get_new_filename(path, postfix):
    return path.parent.joinpath(f'{path.stem}_{postfix}.png')


if __name__ == "__main__":
    arguments = docopt(__doc__)
    if arguments['--verbose']:
        print(arguments)
    for f_path in arguments['FILES']:
        file_path = Path(f_path)
        if not file_path.is_file():
            print(f"No such file or directory: {file_path}")
        else:
            image = Image.open(file_path)
            new_filename = get_new_filename(file_path, arguments['--postfix'])
            if arguments['--verbose']:
                print('\n===============!!===============')
                print(f'Пациент - {file_path}')
            crop(img=image, new_filename=new_filename, arg=arguments)
