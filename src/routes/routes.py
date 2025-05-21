from fastapi import APIRouter
from fastapi.responses import HTMLResponse

homepage = APIRouter()

@homepage.get("/", response_class=HTMLResponse)
def home_page():
    ...
