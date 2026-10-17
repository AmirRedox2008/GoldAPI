import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

url = "https://www.tgju.org/"
url_crypto = "https://www.tgju.org/crypto/ath"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
crypto_response = requests.get(url_crypto, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
crypto_soup = BeautifulSoup(crypto_response.text, "html.parser")

all_arz = {
    "دلار": "price_dollar_rl", "یورو": "price_eur", "درهم": "price_aed", "پوند": "price_gbp",
    "لیر": "price_try", "فرانک": "price_chf", "یوان": "price_cny", "ین": "price_jpy",
    "وون": "price_krw", "دلار کانادا": "price_cad", "دلار استرالیا": "price_aud",
    "دلار نیوزیلند": "price_nzd", "دلار سنگاپور": "price_sgd", "روپیه هند": "price_inr",
    "روپیه پاکستان": "price_pkr", "دینار عراق": "price_iqd", "لیر سوریه": "price_syp",
    "افغانی": "price_afn"
}

# ---- ARZ 

def all_arzs(): 
    all_info = {}
    for key, values in all_arz.items():
        price = "0"
        change = "-"
        low = "-"
        high = "-"
        time = "-"
        tabel = soup.find_all("tr", {"data-market-nameslug": values})
        try:
            for i in tabel: 
                if i.find("td", class_="market-price"):
                    price = i.find("td", class_="market-price").text.strip()
                    
                change_td = i.find("td", class_="high") or i.find("td", class_="low")
                if change_td:
                    change = change_td.text.strip()
                    
                if i.find("td", class_="market-low"):
                    low = i.find("td", class_="market-low").text.strip()
                    
                if i.find("td", class_="market-high"):
                    high = i.find("td", class_="market-high").text.strip()
                    
                if i.find("td", class_="market-time"):
                    time = i.find("td", class_="market-time").text.strip()
        except Exception as e : 
            print(e)

        all_info[values] = {
            "name": key,
            "price": float(str(price).replace(",", "")),
            "change": change, 
            "low": low, 
            "high": high, 
            "time": time
        }
    return all_info

def get_arz(ARZ):
    all_info = {}
    tabel = soup.find_all("tr", {"data-market-nameslug": ARZ})
    for i in tabel:
        price = "0"
        change = "-"
        low = "-"
        high = "-"
        time = "-"
        try:
            if i.find("td", class_="market-price"):
                price = i.find("td", class_="market-price").text.strip()
                
            change_td = i.find("td", class_="high") or i.find("td", class_="low")
            if change_td:
                change = change_td.text.strip()
                
            if i.find("td", class_="market-low"):
                low = i.find("td", class_="market-low").text.strip()
                
            if i.find("td", class_="market-high"):
                high = i.find("td", class_="market-high").text.strip()
                
            if i.find("td", class_="market-time"):
                time = i.find("td", class_="market-time").text.strip()
        except Exception as e:
            print(e)

        all_info[ARZ] = {
            "price": float(str(price).replace(",", "")),
            "change": change, 
            "low": low, 
            "high": high, 
            "time": time
        }
    return all_info

# ARZ DIGITAL

def all_coins():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        crypto_response = requests.get("https://www.tgju.org/crypto/ath", headers=headers)
        soup = BeautifulSoup(crypto_response.text, "html.parser")
    except Exception as e:
        print("Error fetching coins:", e)
        return []

    coins_list = []
    rows = soup.select("tbody tr")
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 5:
            name_cell = cells[1]
            
            spans = name_cell.find_all("span")
            name_fa = spans[0].get_text(strip=True) if len(spans) > 0 else name_cell.get_text(strip=True)
            name_en = spans[1].get_text(strip=True) if len(spans) > 1 else name_cell.get_text(strip=True)
            symbol = spans[2].get_text(strip=True) if len(spans) > 2 else ""
            
            price = cells[2].get_text(strip=True) if len(cells) > 2 else "-"
            high = cells[4].get_text(strip=True) if len(cells) > 4 else "-"
            low = cells[5].get_text(strip=True) if len(cells) > 5 else "-"
            time = cells[-2].get_text(strip=True) if len(cells) > 1 else "-"
            
            coins_list.append({
                "name_fa": name_fa,
                "name_en": name_en,
                "symbol": symbol,
                "price": price,
                "low": low, 
                "high": high, 
                "time": time
            })
            
    return coins_list


def get_coin(COIN_NAME):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        crypto_response = requests.get("https://www.tgju.org/crypto/ath", headers=headers)
        soup = BeautifulSoup(crypto_response.text, "html.parser")
    except Exception as e:
        print("Error fetching coin:", e)
        return {"error": "Could not fetch data"}

    rows = soup.select("tbody tr")
    
    for row in rows:
        cells = row.find_all("td")
        
        if len(cells) > 5:
            name_cell = cells[1]
            name_text = name_cell.get_text(" ", strip=True).lower()
            
            if COIN_NAME.lower() in name_text:
                spans = name_cell.find_all("span")
                name_fa = spans[0].get_text(strip=True) if len(spans) > 0 else name_cell.get_text(strip=True)
                name_en = spans[1].get_text(strip=True) if len(spans) > 1 else COIN_NAME
                symbol = spans[2].get_text(strip=True) if len(spans) > 2 else ""
                
                price = cells[2].get_text(strip=True) if len(cells) > 2 else "-"
                high = cells[4].get_text(strip=True) if len(cells) > 4 else "-"
                low = cells[5].get_text(strip=True) if len(cells) > 5 else "-"
                time = cells[-2].get_text(strip=True) if len(cells) > 1 else "-"
                
                return {
                    "name_fa": name_fa,
                    "name_en": name_en,
                    "symbol": symbol,
                    "price": price,
                    "low": low, 
                    "high": high, 
                    "time": time
                }
                
    return {"error": "Coin not found"}