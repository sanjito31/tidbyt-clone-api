from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from math import sin, cos, radians

DISP_WIDTH      = 64
DISP_HEIGHT     = 32

def draw_text(
        text: str,
        width: int = DISP_WIDTH,
        height: int = DISP_HEIGHT,
        fontsize: int = 12,
        bg: tuple = (0, 0, 0),
        fg: tuple = (255, 255, 255),
        align: tuple = ('c', 'c')
):
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("./fonts/JetBrainsMonoNL-Regular.ttf", fontsize)
    except OSError:
        font = ImageFont.load_default(fontsize)

    bbox = draw.textbbox((0, 0), text, font=font)

    x_off = bbox[0]
    y_off = bbox[1]

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Horizontal Align
    if align[0] == 'c':
        x = (width - text_width) // 2
    elif align[0] == 'l':
        x = 0 - x_off
    elif align[0] == 'r':
        x = width - text_width

    # Vertical Align
    if align[1] == 'c':
        y = (height - text_height) // 2
    elif align[1] == 't':
        y = 0 - y_off
    elif align[1] =='b':
        y = height - text_height


    draw.text((x - x_off, y - y_off), text, font=font, fill=fg)


    buf = BytesIO()
    img.save(buf, "WEBP")
    return buf.getvalue()


def draw_time(text: str,
        width: int = DISP_WIDTH,
        height: int = DISP_HEIGHT,
        fontsize: int = 15,
        bg: tuple = (0, 0, 0),
        fg: tuple = (255, 255, 255),
        align: tuple = ('c', 'c')
        ):
    
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("./fonts/JetBrainsMonoNL-Bold.ttf", fontsize)
    except OSError:
        font = ImageFont.load_default(fontsize)


    hour_text, rest = text.split(":")
    minute_text = rest[:2]
    meridian_text = rest[2:]

    hour = Text(hour_text, draw, font)
    minute = Text(minute_text, draw, font)


    v_space = (height - hour.height - minute.height) // 3
    h_space = (((width // 2) - max(hour.width, minute.width)) // 2)


    draw.text(hour.coords(width - h_space - hour.width, v_space), hour.text, font=hour.font, fill=fg)
    draw.text(minute.coords(width - h_space - minute.width, height - v_space - minute.height), minute.text, font=minute.font, fill=fg)

    # circle center
    x = width // 4
    y = height // 2
    radius = x - v_space

    draw.circle((x,y), radius, fill=None, outline=fg, width=1)


    # Minute hand
    MINUTES_PER_HOUR = 60.0
    MINUTE_HAND_LENGTH = 0.9  # Fraction of Radius
    hour_frac = (float(minute.text) / MINUTES_PER_HOUR)
    min_hand_angle = 360 * hour_frac

    x_min_hand = (radius * MINUTE_HAND_LENGTH) * sin(radians(min_hand_angle)) + x
    y_min_hand = (radius * MINUTE_HAND_LENGTH) * -cos(radians(min_hand_angle)) + y

    draw.line([(x, y), (x_min_hand, y_min_hand)], fill=fg, width=1)


    # Hour hand
    HOURS_PER_CIRCLE = 12
    MINUTES_PER_CIRCLE = HOURS_PER_CIRCLE * MINUTES_PER_HOUR
    HOUR_HAND_LENGTH = 0.5 # Fraction of Radius


    minutes_past_twelve = ((int(hour.text) % HOURS_PER_CIRCLE) * MINUTES_PER_HOUR + int(minute.text)) 
    hour_hand_angle = 360 * (minutes_past_twelve / MINUTES_PER_CIRCLE)

    x_hour_hand = (radius * HOUR_HAND_LENGTH) * sin(radians(hour_hand_angle)) + x
    y_hour_hand = (radius * HOUR_HAND_LENGTH) * -cos(radians(hour_hand_angle)) + y

    draw.line([(x,y), (x_hour_hand, y_hour_hand)], fill=fg, width=1)

    # Meridian
    if meridian_text == "PM":
        p = Text("P", draw, font=ImageFont.truetype("./fonts/JetBrainsMonoNL-Thin.ttf", 4))
        draw.text(p.coords(width - h_space, height - v_space - minute.height), p.text, fill=fg)



    buf = BytesIO()
    img.save(buf, "WEBP")
    return buf.getvalue()





# print(f"left: {bbox[0]}")
# print(f"top: {bbox[1]}")
# print(f"right: {bbox[2]}")
# print(f"bottom: {bbox[3]}")

class Text():

    def __init__(self, text, draw, font):
        self.text = text
        self.draw = draw
        self.font = font
        self.bbox = draw.textbbox((0, 0), text, font=font)
        
        self.width = self.bbox[2] - self.bbox[0]
        self.height = self.bbox[3] - self.bbox[1]

        self.x_off = self.bbox[0]
        self.y_off = self.bbox[1]

    def coords(self, x, y):
        return (x - self.x_off, y - self.y_off)
    
    def print_bbox(self):
        print(f"{self.text}")
        print(f"left: {self.bbox[0]}")
        print(f"top: {self.bbox[1]}")
        print(f"right: {self.bbox[2]}")
        print(f"bottom: {self.bbox[3]}")
        print(f"width: {self.width}")
        print(f"height: {self.height}")

    

def draw_weather(   weather: dict,
                    width: int = DISP_WIDTH,
                    height: int = DISP_HEIGHT,
                    fontsize: int = 6,
                    bg: tuple = (0, 0, 0),
                    fg: tuple = (255, 255, 255),
                    align: tuple = ('c', 'c')
                ):
    
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("./fonts/JetBrainsMonoNL-Regular.ttf", fontsize)
    except OSError:
        font = ImageFont.load_default(fontsize)

    temp = Text(weather["temp"]+"F", draw, font)
    temp.x_off = temp.x_off + 2
    temp.y_off = temp.y_off + 1
    description = Text(weather["description"], draw, font)

    margin = 2

    
    draw.text(description.coords(margin, height-description.height-margin), description.text, fill=fg)

    draw.text(temp.coords(width-temp.width-margin, height-temp.height-margin), temp.text, fill=fg)
    
    if description.text is "sunny" or "clear sky":
    
        yellow = (255, 255, 0)

        draw.circle((2, 2), 10, fill=yellow, outline=yellow)
        draw.line([(2, 14), (2, 18)], fill=yellow)
        draw.line([(14, 2), (18, 2)], fill=yellow)

        def sun_rays(angle, length):
            x = length * sin(radians(angle)) + 2
            y = length * -cos(radians(angle)) + 2
            return x, y

        draw.line([(sun_rays(25+90, 14)), (sun_rays(25+90, 18))], fill=yellow)
        draw.line([(sun_rays(45+90, 14)), (sun_rays(45+90, 18))], fill=yellow)
        draw.line([(sun_rays(65+90, 14)), (sun_rays(65+90, 18))], fill=yellow)

    buf = BytesIO()
    img.save(buf, "WEBP")
    return buf.getvalue()
