from fastapi import APIRouter
from fastapi.responses import FileResponse  
from api.scrap import get_arz, all_arzs, get_coin, all_coins
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.database.database import session_local
from api.database.models import save_prices
from api.History import get_latest_table
from pydantic import BaseModel
from datetime import datetime


class CreatePricesReq(BaseModel):
    name : str 
    price : str 
    change : str 
    low : str 
    high : str 
    Updatetime : str 

router = APIRouter()
scheduler = AsyncIOScheduler()
db = session_local()

def fetch_arzs():
    scraped_data = all_arzs()
    db = session_local()
    try:
        for arz_data in scraped_data.values():
            db.add(save_prices(
                name=arz_data.get("name", "-"),
                price=str(arz_data.get("price", "0")),
                change=arz_data.get("change", "-"),
                low=arz_data.get("low", "-"),
                high=arz_data.get("high", "-"),
                Updatetime=datetime.now(),
            ))
        db.commit()
    except Exception as e:
        db.rollback()
        print("DB error:", e)
    finally:
        db.close()

def save_arzs(userreq: CreatePricesReq):
    create_user_model = save_prices(
        name=userreq.name,
        price=userreq.price, 
        change=userreq.change,
        low=userreq.low,
        high=userreq.high,
        Updatetime=userreq.Updatetime  
    )
    db.add(create_user_model)
    db.commit()

@router.post("/set-schedule/{hours}")
async def set_schedule(hours: int):
    if hours < 1 or hours > 6:
        return {"error": "invalid hour"}
    scheduler.add_job(fetch_arzs, 'interval', hours=hours, id="fetch_arz_job", replace_existing=True)
    return {"status": "success", "message": f"Schedule updated to {hours} hours"}

@router.on_event("startup")
async def startup_event():
    try:
        scheduler.start()
        print("Scheduler started successfully!")
    except Exception as e:
        print(f"Scheduler is already running or error: {e}")

@router.on_event("shutdown")
async def shutdown_event():
    try:
        scheduler.shutdown(wait=False)
    except Exception as e:
        print(f"Scheduler shutdown warning: {e}")

@router.get("/prices/all")
async def get_prices_all():
    return all_arzs()

@router.get("/prices/{symbol}")
async def get_price(symbol: str):
    return get_arz(symbol)

@router.get("/prices/history/{Arz_name}")
async def HistorySend(Arz_name: str):
    filename = get_latest_table(Arz_name)
    if filename:
        return FileResponse(
            path=filename,
            filename="history_prices.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    return {"error": "File not created!"}

@router.get("/prices/coins")
async def show_coins():
    return all_coins()  
    
@router.get("/prices/coin/{coin_name}")
async def show_coin(coin_name: str):  
    return get_coin(coin_name)