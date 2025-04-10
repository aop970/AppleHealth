
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import math
import os

LAT = 33.0034
LON = -97.2020
IMAGE_SIZE = 500
CENTER = IMAGE_SIZE // 2
RADIUS = 180
SUN_COLOR = (255, 215, 0)
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUTPUT_PATH = "data/daylight_arc.png"

font_large = ImageFont.truetype(FONT_PATH, 36)
font_small = ImageFont.truetype(FONT_PATH, 24)

def fetch_astronomy_data():
    url = f"https://api.sunrise-sunset.org/json?lat={LAT}&lng={LON}&formatted=0"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['results']

def time_to_angle(iso_time):
    dt = datetime.fromisoformat(iso_time)
    minutes = dt.hour * 60 + dt.minute
    return (minutes / 1440.0) * 360 - 90

def draw_arc(draw, start, end, color, width):
    draw.arc([CENTER - RADIUS, CENTER - RADIUS, CENTER + RADIUS, CENTER + RADIUS],
             start=start, end=end, fill=color, width=width)

def create_daylight_graphic(data):
    img = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), BG_COLOR)
    draw = ImageDraw.Draw(img)

    sunrise_angle = time_to_angle(data['sunrise'])
    sunset_angle = time_to_angle(data['sunset'])
    draw_arc(draw, sunrise_angle, sunset_angle, SUN_COLOR, 20)

    seconds = int(data['day_length'])
    hours, remainder = divmod(seconds, 3600)
    minutes = remainder // 60
    center_text = f"{hours}h {minutes}m"
    bbox = draw.textbbox((0, 0), center_text, font=font_large)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text((CENTER - w // 2, CENTER - h // 2), center_text, fill=TEXT_COLOR, font=font_large)

    draw.text((CENTER - RADIUS - 10, CENTER - 15), "☀️", font=font_small)
    draw.text((CENTER + RADIUS - 30, CENTER - 15), "☀️", font=font_small)

    return img

def generate_daylight_arc():
    data = fetch_astronomy_data()
    img = create_daylight_graphic(data)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH)
    print(f"Saved: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_daylight_arc()
