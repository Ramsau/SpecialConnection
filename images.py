from PIL import Image, ImageOps, ImageFont, ImageDraw
import numpy as np
import math

IMG_WIDTH = 800
IMG_HEIGHT = 480

TEXT_MARGIN = 20
FONT_NAME = "./C059-BdIta.ttf"

def convert_image(in_path, out_path):
    img_in = Image.open(in_path)
    resize_factor = min(IMG_WIDTH / float(img_in.width), IMG_HEIGHT / float(img_in.height))
    img_width = int(img_in.width * resize_factor)
    img_height = int(img_in.height * resize_factor)
    img_in = img_in.resize((img_width, img_height), Image.LANCZOS)
    img_width_diff = IMG_WIDTH - img_width
    img_height_diff = IMG_HEIGHT - img_height
    img_in = ImageOps.expand(img_in, border=(math.floor(img_width_diff / 2), math.floor(img_height_diff / 2),
                                             math.ceil(img_width_diff / 2), math.ceil(img_height_diff / 2)), fill="white")
    img_bw = np.array(img_in.convert("L"))
    img_dithered = np.random.binomial(1, img_bw / 255.0)
    img_out = Image.fromarray(img_dithered * 255.0).convert(
        "1"
    )
    img_out.save(out_path)


def wrap_text(text, fontname, max_size, min_size, max_width, max_height, draw):
    forced_lines = text.splitlines()

    font_size = max_size
    while font_size >= min_size:
        font = ImageFont.truetype(fontname, font_size)
        font_downsize = False
        all_lines = []

        for forced_line in forced_lines:
            words = forced_line.split()
            if not words:
                all_lines.append('')
                continue

            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                width = draw.textlength(test_line, font=font)
                if width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        all_lines.append(' '.join(current_line))
                    if draw.textlength(word, font=font) > max_width:
                        font_downsize = True
                        break
                    current_line = [word]

            if font_downsize:
                break

            if current_line:
                all_lines.append(' '.join(current_line))

        if font_downsize:
            font_size -= 1
            print(font_size)
            continue

        if font_size * len(all_lines) <= max_height:
            return all_lines, font_size

        font_size -= 1

    raise Exception("Text too large to fit in box")

def convert_text(text, out_path):
    img = Image.new("1", (IMG_WIDTH, IMG_HEIGHT), "white")
    d = ImageDraw.Draw(img)
    lines, font_size = wrap_text(text, FONT_NAME, 100, 10,
                                 IMG_WIDTH - TEXT_MARGIN * 2, IMG_HEIGHT - TEXT_MARGIN * 2,
                                 d)
    font = ImageFont.truetype(FONT_NAME, font_size)

    for i, line in enumerate(lines):
        d.text((IMG_WIDTH / 2, IMG_HEIGHT / 2  + (i + 0.5 - len(lines)/2) * font_size), line, font=font, fill="black", anchor="mm")
    img.save(out_path)




if __name__ == "__main__":
#     convert_image("test_img.jpg", "test_out.png")
    convert_text("nice face...\nmind if i kiss it?", "test_out.png")