from PIL import Image, ImageFilter, ImageDraw

image = Image.open('./test.png')
pix = image.load()
print(image.format, image.size, image.mode)
print(image.size[0], image.size[1])

draw = ImageDraw.Draw(image)

width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту

for x in range(width):
    for y in range(height):
        r = pix[x, y][0]  # узнаём значение красного цвета пикселя
        g = pix[x, y][1]  # зелёного
        b = pix[x, y][2]  # синего
        sr = (r + g + b) // 3  # среднее значение
        draw.point((x, y), (sr, sr, sr))  # рисуем пиксель


color = pix[1, 1][0]
for x in range(width):
    for y in range(height):
        if color!=pix[x, y][0]:
            draw.point((x, y), (255, 0, 0))  # рисуем пиксель

image.save("result.jpg", "JPEG")
