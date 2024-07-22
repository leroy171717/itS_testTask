from django.http import HttpResponse
from django.views import View
from django.utils.text import slugify
from video.models import Text  # Импортируйте модель
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class RunningTextVideo(View):
    def get(self, request, text):
        # Сохраните введённый текст в базу данных
        Text.objects.create(text=text)  # Сохраняем текст в БД

        # Устанавливаем шрифт
        font = ImageFont.truetype('arial.ttf', 50)

        # Генерируем текст для бегущей строки
        #text = slugify(text)  # Преобразуем текст для URL, если это необходимо
        text = text.replace("-", " ")  # Возвращаем пробелы вместо дефисов

        # Создаем видео файл
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter('running_text.avi', fourcc, 30, (100, 100))

        # Расчет ширины текста
        text_width = font.getlength(text)
        speed = text_width / 90 + 1  # Скорость движения текста

        # Генерируем кадры с бегущим текстом
        for i in range(90):
            image = Image.new('RGB', (100, 100), color=(255, 0, 255))
            draw = ImageDraw.Draw(image)
            draw.text((100 - int(i * speed), 5), text, font=font, fill=(255, 255, 255))
            frame_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            video.write(frame_np)

        video.release()
        cv2.destroyAllWindows()

        # Возвращаем созданный видео файл как ответ
        with open('running_text.avi', 'rb') as f:
            response = HttpResponse(f.read(), content_type='video/avi')
            response['Content-Disposition'] = 'attachment; filename="running_text.avi"'
            return response
