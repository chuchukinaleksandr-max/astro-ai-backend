from fastapi import FastAPI
from pydantic import BaseModel
from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime
from flatlib.chart import Chart
from flatlib import aspects, const

app = FastAPI()


class NatalRequest(BaseModel):
    date: str
    time: str
    lat: float
    lon: float
    tz: float


def planet_data(chart, planet):
    obj = chart.get(planet)
    return {
        "name": planet,
        "sign": obj.sign,
        "lon": round(obj.lon, 4),
        "lat": round(obj.lat, 4),
        "speed": round(obj.speed, 4),
        "house": obj.house
    }


@app.post("/natal")
def calculate_natal(data: NatalRequest):
    dt = Datetime(data.date, data.time, data.tz)
    pos = GeoPos(data.lat, data.lon)
    chart = Chart(dt, pos)

    planets = [
        const.SUN, const.MOON, const.MERCURY, const.VENUS,
        const.MARS, const.JUPITER, const.SATURN,
        const.URANUS, const.NEPTUNE, const.PLUTO
    ]

    planet_list = [planet_data(chart, p) for p in planets]

    houses = {str(i): {"cusp": round(chart.houses.cusp(i), 4)} for i in range(1, 13)}

    aspect_list = []
    for a in aspects.MAJOR_ASPECTS:
        asp = chart.getAspect(a)
        if asp:
            aspect_list.append({
                "p1": asp.p1,
                "p2": asp.p2,
                "type": asp.type,
                "degree": round(asp.d, 2)
            })

    return {
        "status": "ok",
        "planets": planet_list,
        "houses": houses,
        "aspects": aspect_list,
        "asc": round(chart.ascendant.lon, 4),
        "mc": round(chart.midheaven.lon, 4)
    }


@app.get("/")
def home():
    return {"status": "astro-ai backend работает"}
