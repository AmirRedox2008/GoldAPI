from fastapi import FastAPI 
from api.prices import router as prices_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.database.database import Base,engine
from fastapi import Request
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.prices import router as prices_router, scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)

app = FastAPI(title="Gold & Currency Price API", lifespan=lifespan)
app.include_router(prices_router)
Base.metadata.create_all(engine)
app = FastAPI()
templates = Jinja2Templates(directory="api/templates")

app.include_router(prices_router)

@app.get("/dashboard", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")
