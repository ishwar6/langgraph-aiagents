import requests
from bs4 import BeautifulSoup

def google_search(query: str, num: int = 5):
    resp = requests.get("https://www.google.com/search", params={"q": query, "num": num}, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    out = []
    for g in soup.select("div.g"):
        a = g.find("a")
        t = g.find("h3")
        if not a or not t:
            continue
        s = g.find("span", class_="aCOpRe")
        out.append({"title": t.text, "link": a["href"], "snippet": s.text if s else ""})
        if len(out) >= num:
            break
    return out
