import sys

from PIL import Image, ImageFilter, ImageDraw


def crop(image):
    pix = image.load()

    print(f'{image.format=}', f'{image.size=}', f'{image.mode=}')
    print('Размер изображения', image.size[0], image.size[1])

    draw = ImageDraw.Draw(image)

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
                    bottom = y + 2
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
                    right = x + 2
                    break

    print('Координаты обрезки', f'{up=}', f'{bottom=}', f'{left=}', f'{right=}', )
    image_crop = image.crop((left, up, right, bottom))
    image_crop.save("result_crop.png", "PNG")


if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
        image = Image.open(file_path)
        crop(image=image)

    except IndexError as e:
        print(f"Write path to your file as in the example")
    except FileNotFoundError as e:
        print(f"No such file or directory: {file_path}")
    except Exception as e:
        print(e)
