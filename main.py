import sys

from PIL import Image
from pathlib import Path


def crop(image, new_filename):
    pix = image.load()
    print(f'{image.format=}', f'{image.size=}', f'{image.mode=}')
    print('Размер изображения', image.size[0], image.size[1])

    width = image.size[0]  # Определяем ширину
    height = image.size[1]  # Определяем высоту

    up, bottom, left, right = 0, 0, 0, 0
    color = [pix[1, 1][0], pix[1, 1][1], pix[1, 1][2]]
    print('Цвет пикселя (1,1)', f'{color=}')

    for y in range(height):
        if not up:
            for x in range(width):
                # print('2', x, y, [pix[x, y][0], pix[x, y][1], pix[x, y][2]])
                if color != [pix[x, y][0], pix[x, y][1], pix[x, y][2]]:
                    up = y - 1
                    break

    for y in reversed(range(height)):
        if not bottom:
            for x in range(width):
                if color != [pix[x, y][0], pix[x, y][1], pix[x, y][2]]:
                    bottom = y + 1
                    break

    for x in range(width):
        if not left:
            for y in range(height):
                if color != [pix[x, y][0], pix[x, y][1], pix[x, y][2]]:
                    left = x - 1
                    break
    for x in reversed(range(width)):
        if not right:
            for y in range(height):
                if color != [pix[x, y][0], pix[x, y][1], pix[x, y][2]]:
                    right = x + 1
                    break

    print('Координаты обрезки', f'{up=} {bottom=} {left=} {right=}')
    image_crop = image.crop((left, up, right, bottom))
    image_crop.save(f'{new_filename}', "PNG")


def get_new_filename(file_path):
    p = Path(file_path)
    return p.parent.joinpath(p.stem + '_crop' + '.png')


if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
        image = Image.open(file_path)
        new_filename = get_new_filename(file_path)
        print('\n===============!!===============')
        print(f'Пациент - {file_path}')
        crop(image=image, new_filename=new_filename)

    except IndexError as e:
        print(f"Write path to your file as in the example.\n{e=}")
    except FileNotFoundError as e:
        print(f"No such file or directory: {file_path} \n{e=}")
    except Exception as e:
        print(e)
