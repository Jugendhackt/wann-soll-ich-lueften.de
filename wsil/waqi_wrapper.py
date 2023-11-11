from dotenv import load_dotenv
from os import getenv
from json import loads
from pydantic import BaseModel, field_validator
from requests import get, Response
from datetime import datetime, date
from typing import Optional
from functools import lru_cache

load_dotenv()
API_TOKEN = getenv("WAQI_API_TOKEN")


class PollutionTime(BaseModel):
    s: datetime     # local time of the measurement
    tz: str     # station timezone


class StationTime(BaseModel):
    vtime: int
    stime: datetime     # local time of the measurement
    tz: str     # station timezone


class City(BaseModel):
    name: str
    geo: list[float]
    url: str


class AQI(BaseModel):
    v: float  # value


class IAQI(BaseModel):
    pm25: AQI
    pm10: AQI
    no2: AQI


class DailyForecastType(BaseModel):
    avg: int
    day: date
    max: int
    min: int


class DailyForecast(BaseModel):
    pm25: list[DailyForecastType]
    pmp10: Optional[list[DailyForecastType]] = None
    o3: list[DailyForecastType]
    uvi: list[DailyForecastType]


class Forecast(BaseModel):
    daily: DailyForecast


class PollutionResponse(BaseModel):
    idx: int    # unique id for the monitoring station
    aqi: int    # real-time air quality
    time: PollutionTime   # time data
    iaqi: IAQI   # current measurements
    forecast: Forecast   # expected measurements


class Station(BaseModel):
    uid: int
    aqi: Optional[int] = None
    time: StationTime
    city: Optional[City] = None

    @field_validator("aqi", mode="before")
    @classmethod
    def check_type(cls, aqi: int | str):
        if isinstance(aqi, str):
            return None
        return aqi


def _check_response(response: Response):
    if response.status_code != 200:
        raise ConnectionError(f"WAQI API returned {response.status_code}")

    json_response = loads(response.text)
    if json_response["status"] != "ok":
        raise ConnectionError(f"WAQI API returned {json_response['status']}")


def get_pollution_data(location: str) -> PollutionResponse:
    response = get(f"https://api.waqi.info/feed/{location}/?token={API_TOKEN}")
    _check_response(response)

    # transform the raw response json into an easily readable python class
    return PollutionResponse(**loads(response.text)["data"])    # pollution data


@lru_cache()
def get_stations_by_name(name: str) -> list[Station]:
    response = get(f"https://api.waqi.info/search/?keyword={name}&token={API_TOKEN}")
    _check_response(response)

    return [Station(**station) for station in loads(response.text)["data"]]
