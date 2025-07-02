from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from geopy.geocoders import Nominatim
import folium
import os

# App setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Create templates folder
os.makedirs("templates", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
def form_post(request: Request, city: str = Form(...)):
    geolocator = Nominatim(user_agent="map_app")
    location = geolocator.geocode(city)

    if not location:
        return templates.TemplateResponse("form.html", {"request": request, "error": "City not found"})

    lat, lon = location.latitude, location.longitude

    # Create Folium map
    m = folium.Map(location=[lat, lon], zoom_start=11)
    folium.Circle(
        location=[lat, lon],
        radius=25000,
        color="blue",
        fill=True,
        fill_opacity=0.3,
    ).add_to(m)

    map_path = "templates/map.html"
    m.save(map_path)

    return templates.TemplateResponse("map.html", {"request": request, "city": city})
