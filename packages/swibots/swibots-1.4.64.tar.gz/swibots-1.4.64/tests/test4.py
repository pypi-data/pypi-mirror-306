file = "file {r}.mp4"
print(file.format(d="ahh"))
exit()
from PIL import Image, ImageFilter
img = Image.open("y.png")
img.thumbnail((img.height // 2, img.width // 2), Image.BILINEAR)
img.filter(ImageFilter.GaussianBlur(6)).save("x.png", quality=32, optimize=True)