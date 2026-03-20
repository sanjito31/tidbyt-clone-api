from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
from pytz import timezone

def draw_time():

    width = 64
    height = 32
    fontsize = 12
    fg = (255, 255, 255)

    text = datetime.now(timezone('US/Eastern')).strftime("%-I:%M%p")

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMonoNL-Regular.ttf", fontsize)
    except OSError:
        font = ImageFont.load_default(fontsize)

    bbox = draw.textbbox((0, 0), text, font=font)
    x = (width - bbox[2] + bbox[0]) // 2
    y = (height - bbox[3] + bbox[1]) // 2
    draw.text((x, y), text, font=font, fill=fg)

    buf = BytesIO()
    img.save(buf, "WEBP")
    return buf.getvalue()

def get_time_str():
    return datetime.now(timezone('US/Eastern')).strftime("%-I:%M%p")