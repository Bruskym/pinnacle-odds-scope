BASE_URL = "https://www.pinnacle.com"
APP_CONFIG_URL = f"{BASE_URL}/config/app.json"

BASE_API_URL = "https://guest.api.arcadia.pinnacle.com/0.1/"
LEAGUES_URL = f"{BASE_API_URL}/sports/29/leagues?all=false&brandId=0"

HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-BR,pt;q=0.7",
    "Content-Type": "application/json",
    "Cookie": "UserPrefsCookie=languageId=10&priceStyle=decimal&linesTypeView=a&device=d&languageGroup=all",
    "Referer": "https://www.pinnacle.com/pt/soccer/brazil-serie-a/matchups/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
}
