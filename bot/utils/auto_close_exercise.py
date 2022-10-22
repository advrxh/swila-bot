import json
from pathlib import Path

from bot.constants import Paths

import arrow


async def set_duration(days: int, exercise_no: int):
    with Paths.DATA_STORE.open("r+", encoding="utf-8") as ds_file:
        data = json.load(ds_file)

    Paths.DATA_STORE.unlink()
    Paths.DATA_STORE.touch()

    with Paths.DATA_STORE.open("r+", encoding="utf-8") as ds_file:
        data["exercise"] = {
            "duration": arrow.now().shift(days=days).timestamp(),
            "exercise_no": exercise_no,
        }
        json.dump(data, ds_file)


async def get_duration():

    with Paths.DATA_STORE.open("r+", encoding="utf-8") as ds_file:
        data = json.load(ds_file)
        duration = arrow.now().fromtimestamp(float(data["exercise"].get("duration")))
        exercise_no = data.get("exercise")["exercise_no"]

    return duration, exercise_no
