import sys

from PIL import Image
from pathlib import Path


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


def get_new_filename(file_path):
    p = Path(file_path)
    return p.parent.joinpath(p.stem + '_crop' + '.png')


if __name__ == "__main__":
    file_path = Path(sys.argv[1])
    if not file_path.is_file():
        print(f"No such file or directory: {file_path}. Are u wrote it as in example? ")

    image = Image.open(file_path)
    new_filename = get_new_filename(file_path)
    print('\n===============!!===============')
    print(f'Пациент - {file_path}')
    crop(image=image, new_filename=new_filename)
