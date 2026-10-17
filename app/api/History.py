import requests
from bs4 import BeautifulSoup 
from openpyxl import Workbook

def get_latest_table(arz):
    url = f"https://www.tgju.org/profile/{arz}/history"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    if not table:
        return None

    tbody = table.find("tbody")
    if not tbody:
        tbody = table

    rows = tbody.find_all("tr")
    
    wb = Workbook()
    ws = wb.active
    
    ws.append(["بازگشایی", "کمترین", "بیشترین", "پایانی", "میزان تغییر", "درصد تغییر", "تاریخ میلادی", "تاریخ شمسی"])
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 8:
            row_data = []
            for cell in cells:
                text = cell.get_text(strip=True)
                if "," in text:
                    text = text.replace(",", "")
                
                try:
                    if "." in text:
                        text = float(text)
                    else:
                        text = int(text)
                except ValueError:
                    pass
                
                row_data.append(text)
            
            ws.append(row_data) 
            
    filename = "latest_table.xlsx"
    wb.save(filename)
    return filename