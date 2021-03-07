from PIL import Image, ImageFilter, ImageDraw
import random
import os


def xline(draw, y, width):
    for x in range(width):
        draw.point((x, y), (0, 0, 0))


image = Image.open('./test.png')
pix = image.load()
print(image.format, image.size, image.mode)
print(image.size[0], image.size[1])

draw = ImageDraw.Draw(image)

width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту

up, bottom, left, right = 0, 0, 0, 0
color = [pix[1, 1][0], pix[1, 1][1], pix[1, 1][2]]
print(f'{color=}')

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

print(f'{up=}', f'{bottom=}', f'{left=}', f'{right=}', )
image.save("result.jpg", "JPEG")

# draw.point((x, y), (0, 0, random.randint(1, 255)))  # рисуем пиксель
