# GoldAPI

![GitHub repo](https://img.shields.io/badge/github-repo-blue?logo=github)
![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)

API دریافت قیمت لحظه‌ای ارز و رمزارز

با این API می‌توانید قیمت لحظه‌ای دلار، ۱۸ ارز خارجی و رمزارزها را دریافت کنید.

## اندپوینت‌ها

| متد | مسیر | توضیح |
|-----|------|-------|
| GET | `/prices/all` | قیمت همه‌ی ارزها |
| GET | `/prices/{symbol}` | قیمت یک ارز خاص |
| POST | `/set-schedule/{hours}` | ذخیره‌ی خودکار |
| GET | `/prices/history/{symbol}` | دریافت تاریخچه‌ی ارز |
| GET | `/prices/coins` | لیست تمام رمزارزها |
| GET | `/prices/coin/{coin_name}` | قیمت یک رمزارز خاص |

## نمونه درخواست

```bash
curl http://127.0.0.1:8000/prices/price_dollar_rl
```

پاسخ:

```json
{
  "price_dollar_rl": {
    "price": 260258.0,
    "change": "+0.14%",
    "low": "259,100",
    "high": "261,500",
    "time": "14:30"
  }
}
```

## ویژگی‌ها

- استخراج قیمت ۱۸ ارز خارجی (دلار، یورو، درهم، پوند، لیر، یوان و...) از سایت tgju.org
- دریافت اطلاعات رمزارزها (بیت‌کوین، اتریوم و سایر ارزهای دیجیتال) همراه با بیشترین و کمترین قیمت روز
- ذخیره‌ی خودکار قیمت‌ها در دیتابیس SQLite به کمک SQLAlchemy ORM
- امکان فعال‌سازی زمان‌بندی خودکار برای اسکرپ و ذخیره‌ی اطلاعات (هر ۱ تا ۶ ساعت) با APScheduler
- دانلود تاریخچه‌ی کامل قیمت هر ارز در قالب فایل Excel (xlsx)
- مستندات تعاملی خودکار (Swagger UI) به لطف FastAPI، بدون نوشتن حتی یک خط کد اضافه
- استفاده از هدر User-Agent برای جلوگیری از مسدود شدن درخواست‌ها

## نصب و راه‌اندازی

```bash
# ۱) کلون کردن پروژه
git clone https://github.com/AmirRedox2008/GoldAPI.git
cd GoldAPI

# ۲) ساخت و فعال‌سازی محیط مجازی
python -m venv venv
source venv/bin/activate          # لینوکس / مک
# venv\Scripts\activate           # ویندوز

# ۳) نصب پیش‌نیازها
pip install -r requirements.txt

# ۴) اجرای سرور
cd app
uvicorn main:app --reload
```

## دریافت قیمت‌ها با پایتون

### قیمت همه‌ی ارزها

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

response = requests.get(f"{BASE_URL}/prices/all", timeout=10)
response.raise_for_status()

for slug, info in response.json().items():
    print(f"{info['name']}: {info['price']}")
```

### قیمت یک ارز خاص

```python
response = requests.get(f"{BASE_URL}/prices/price_dollar_rl", timeout=10)
response.raise_for_status()

dollar = response.json()["price_dollar_rl"]
print(f"قیمت دلار: {dollar['price']} | تغییر: {dollar['change']}")
```

### دانلود تاریخچه در قالب اکسل

```python
response = requests.get(f"{BASE_URL}/prices/history/price_dollar_rl", timeout=30)
response.raise_for_status()

with open("history_prices.xlsx", "wb") as file:
    file.write(response.content)
print("file saved....")
```


###سایت :

<img width="1920" height="3950" alt="Screenshot 2026-10-17 at 10-12-08 پلتفرم GoldAPI داشبورد و مستندات" src="https://github.com/user-attachments/assets/28692819-93ca-4965-98f7-4585a32979a3" />


