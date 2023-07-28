import json
import math
from datetime import date
from parser.config import config
from parser.rabbit import publish
from typing import Any

import pandas as pd

dct_column_title_to_billboard_field = {
    "Город": "city",
    "Тип поверхности": "surface_type",
    "Сторона": "side",
    "Адрес": "address",
    "Вн. код": "internal_key",
    "Широта": "latitude",
    "Долгота": "longitude",
    "фото/схема": "image_url",
    "Прайс C НДС": "price",
    "Диджтал кол-во показов": "number_of_displays",
    "GRP": "grp",
    "OTS": "ots",
    "Код Эспар": "aspar_code",
    "Материал носителя": "fabric",
    "Ограничения по продукту": "restrictions",
    "Городской Округ": "district",
    "Тех. требования": "technical_requirements",
    "Монтаж. Прайс  с НДС": "price_per_installation",
    "Переклейка. Прайс с НДС": "price_per_update",
    "Разрешение ПО": "permitted_until",
    "Примечание": "comment",
}

dct_title_to_occupation_field = {
    "Июль 2023": str(date(2023, 7, 1)),
    "Август 2023": str(date(2023, 8, 1)),
    "Сентябрь 2023": str(date(2023, 9, 1)),
    "Октябрь 2023": str(date(2023, 10, 1)),
    "Ноябрь 2023": str(date(2023, 11, 1)),
    "Декабрь 2023": str(date(2023, 12, 1)),
}


def is_nan(value: Any) -> bool:
    return isinstance(value, type(0.1)) and math.isnan(value)


def do_parcing(file_name: str) -> None:
    df = pd.read_excel(file_name, sheet_name="Статус")
    df_dicts = df.to_dict("records")

    for row in df_dicts:
        # exclude not valid rows 28596-28605
        if not is_nan(row["Город"]):
            billboard_data = {}
            months_data = {}

            for key, value in row.items():
                # exclude nan values
                if key in dct_column_title_to_billboard_field.keys():
                    if not is_nan(value):
                        db_field = dct_column_title_to_billboard_field[key]
                        billboard_data[db_field] = value

                # reformat data about occupation
                elif key in dct_title_to_occupation_field.keys():
                    db_field = dct_title_to_occupation_field[key]
                    if is_nan(value):
                        value = "Свободно"
                    months_data[db_field] = value

            # some formatting
            billboard_data["has_backlight"] = row["Осв"] == "Да"

            # send data to api
            result_data = {"billboard": billboard_data, "months": months_data}
            publish(config.rabbit.results_queue, json.dumps(result_data))
