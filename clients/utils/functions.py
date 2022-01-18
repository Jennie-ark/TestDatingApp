from math import acos, cos, degrees, radians, sin

from PIL import Image
from django.core.mail import send_mail


def watermark(input_image_path):
    base_image = Image.open(input_image_path)
    watermark = Image.open('watermark.png')
    base_image.paste(watermark, (0, 0), watermark)
    image = base_image.save(str(input_image_path))
    return image


def send_email(user, user_like):
    send_mail(
        '',
        f'Вы понравились {user.first_name}, Почта участника:{user.email}',
        'testemailtest@yandex.ru',
        [user_like.email],
        fail_silently=False, )


def distance(lat_a, long_a, lat_b, long_b):
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (
            sin(lat_a) * sin(lat_b) + cos(lat_a) * cos(lat_b) * cos(long_diff))
    return int(degrees(acos(distance)) * 69.09)
