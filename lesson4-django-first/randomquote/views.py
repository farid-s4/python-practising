import random
from datetime import datetime

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
def index(request: HttpRequest) -> HttpResponse:
    quotes = [
        "Успех — это сумма небольших усилий, повторяемых изо дня в день.",
        "Не бойся ошибаться — бойся не попробовать.",
        "Лучшее время начать было вчера. Следующее лучшее время — сегодня.",
        "Большие результаты начинаются с маленьких шагов.",
        "Терпение и постоянство превращают знания в навыки.",
        "Не обязательно быть лучшим — важно становиться лучше.",
        "Каждая ошибка — это возможность чему-то научиться.",
        "Дорогу осилит идущий.",
        "Сложные задачи становятся проще, когда разбиваешь их на части.",
        "Продолжай двигаться вперёд, даже если шаг совсем маленький."
    ]
    random_quote = random.choice(quotes)
    return HttpResponse(random_quote)
# Create your views here.
