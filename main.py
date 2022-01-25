import datetime
import requests

# átalakítja epoch time formátumra
def to_epoch(date:str):
    date = date.strip().split(".")
    return datetime.datetime(int(date[0]), int(date[1]), int(date[2])).timestamp()

# beállít a lekérdezésnek kezdő és vég pontot
kezdet = to_epoch(input("Kezdő dátum(yyyy.mm.dd): "))
veg = to_epoch(input("Végdátum(yyyy.mm.dd): "))

# lekérdezi, a kijelölt időközben lévő túrákat
turak = requests.get(f"https://tturak.hu/api/hikeoccasion/list?from={kezdet}&to={veg}").json()

# régiók, melyekre szűr
helyek = [8, 9]
kulcs_szavak = ["TTT Kupa", "TTT Kupának", "TTT (volt Budapest) Kupa", "TTT (volt Budapest) Kupának"]

for tura in turak:
    # megnézi, hogy melyik van a kijelölt régiókban
    if tura["regions"][0] in helyek:
        #lekérdezi azok leírását
        description = requests.get(f"https://tturak.hu/api/hikeoccasion/{tura['id']}").json()["description"]
        #megnézi, hogy benne van-e valamelyik a keresett kifejezések közül
        for kulcs_szo in kulcs_szavak:
            if kulcs_szo in description:
                print(tura["displayName"], "\t", datetime.date.fromtimestamp(tura["date"]), "\t", f"https://tturak.hu/hikeOccasion/{tura['id']}/details")
                break
