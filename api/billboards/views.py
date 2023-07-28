import datetime
import json
import math
from typing import Any

from billboards.models import Billboard, City, MonthYear, Occupation
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


def is_nan(value: Any) -> bool:
    return isinstance(value, type(0.1)) and math.isnan(value)


@method_decorator(csrf_exempt)
@require_http_methods(["POST"])
def add(request):
    data = json.loads(request.body.decode())
    billboard_data = data["billboard"]
    months_data = data["months"]

    # create city
    city_name = billboard_data["city"]
    city, _ = City.objects.get_or_create(name=city_name)
    billboard_data["city"] = city

    # permitted until transoform to date
    if "permitted_until" in billboard_data:
        permitted_until = billboard_data["permitted_until"]
        billboard_data["permitted_until"] = datetime.datetime.strptime(
            permitted_until, "%d.%M.%Y"
        ).date()

    # create billboard
    billboard = Billboard.objects.create(**billboard_data)

    # create occupation table

    for month_id in range(7, 13):
        month, _ = MonthYear.objects.get_or_create(month=datetime.date(2023, month_id, 1))

        state = months_data[str(month.month)].strip()
        comment = ""

        if state == "Свободно":
            state = Occupation.FREE
        elif state == "Продано":
            state = Occupation.SOLD
        elif "Продано" in state:
            state = Occupation.PARTLY
        elif "Не установлена" == state:
            state = Occupation.NOT_INSTALLED
        elif "Зарезервирована" in state:
            state = Occupation.RESERVED
        else:
            comment = state
            state = Occupation.OTHER

        Occupation.objects.create(billboard=billboard, month=month, state=state, comment=comment)

    return HttpResponse("Данные успешно добавлены", status=200)
