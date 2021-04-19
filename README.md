# r2-mediaserver-client projekt

## media szerver
A szerver fő feladata, hogy folymatosan figyelje a a rádió mappáját, amelyben elhelyezésre kerülnek tematikusan a a zenék. Figyeli, folyamatosan, ha új zene kerül be vagy épp törölve lesz vagy egy adott file modosításra kerül. Ezért a Watchdog rész felel. Ha új zene kerül feltöltésre vagy törlése, akkor értelem szerűen az adatbázisból ezt törli vagy létrehozza. A zenei fájlok meta adatát is olvassa ezeket is elmenti. A másik fő része egy webes kis alkalmazás, ez jelenleg elég elmaradott. Szerepe, hogy az adatbázisban megtalálható zenéket lehessen listázni és a meta adatokat szerkeszteni. (Ezeket tudja jelenleg, de van mit optimalizálni a kód minőségén)

Jelenleg a szerver Flaskben van írva de gondolkodunk rajta, hogy djnago is megérhetné. A szerver egy REST API-t is biztosít külső kliensek számára, amelyen keresztül lehetne a zenei adatbázsban keresni. Ez jelenleg a kliens számára a legfontosabb. Egy auth is jó lenne bele, hogy esetleg a műsorvezetői kliensbe egy bejelentkezés felület is legyen a későbbiekben ez tovább fejlesztés céljából lenne jó.

## media client
A kliens lényegében az adást lebonyolító műsorvezetők számára érdekes. Ezen keresztül tudnak keresni a zenei adatbázisban. Ha egy adott zene pl a kívánságműsorhoz kell, akkor ezen keresztül le lehet tölteni. Ezt jelenleg egy egyszerű ftp kliensel képzeltem el. Tudjuk, hogy a szervern hol található az adott zene és minden műsorvezetőnek van FTP hozzáférése ezt felhasználva le lehet tölteni a zenéket. 

Jelenleg a kliens is flask alkalmazás, de bármilyen megoldás elképzelhető :) 

## Elképzelés

### MediaServer

Az egyik legfontosabb lépés a szerver rendberakása, mert ez a központja az egész mókának. Itt is több teendő van. A legfontosabb lenne átstruktúrálni a kódot és tényelegesen szétválasztani a különböző rétegeket. 
Igazából most az lenne megcélozva, hogy az eddigi flaskes alkalmazást lehet lecserélnénk FastAPI-ra (https://fastapi.tiangolo.com/ ; https://www.section.io/engineering-education/choosing-between-django-flask-and-fastapi/)
Mindenképp a Modell Controller réteget szépen el kell különíteni de akár egy olyan struktúrát is el tudok képzelni, hogy Controller Service Repository és Model. A repository (dao) réteg talán azért lenne jó, mert azt akár használhatná a Watchdog is minden további nélkül.

A kód szervezéshez bevezetésre szeretnénk hozni a Depedency Injection ( https://python-dependency-injector.ets-labs.org/ ) ezzel sokminden egyszerűsödhetne. Ennek valami kezdeménye volt az App osztály de jobbank látom olyan megvalósításra támaszkodni, amely könynen használható. 

Van gy jó példa pont SQLAlchemy + FastAPI + PythonDepedencyInjector ( https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html )

Egyenlőre magának a webservice-nek pusztány annyit kell tudni, hogy le lehessen kérdezni az összes zenét, erre én továbbra is támogatom a pagebale ötletet valamint esetleg egy két filter paraméter nem ártana a különböző meta adatok szerint. 

A szerver másik része maga a library kezelő. A library kezelő igazából nagyjából rendben is lenne csak valamilyen formában jó lenne elkülöníteni a többi részétől az alkalmazásnak és átültetni ezt is OOP keretek közé. Igazából teljesen futthatna a háttérben. 

A media serverből a kliens teljesen ki fog kerülni és a MediaClient fogja ellátni ezt a feladatot is a definált API-n keresztül

A FastAPI támogatja az OAuth-ot ez tök jó lenne, mert maga a MediaClient egy egyszerű webalkalmazás lenne, amit szeretnénk elválasztani a szervertől, hogy könnyen mozgatható legyen a szerver nélkül is. 

### MediaClient

Igazából nagyjából az egész lecserélésre kerül HTML + CSS + JS forntendre és maga a python rész pusztán annyiból fog állni, mint most. Lesz, ami betölti a kliens oldalait, valamint egy download url, amely lecsrélésre kerül és kap egy zenei id-t és az annak megfelelő zenéni fájlhoz tartozó path alapján letölti egy mappába a zenét első körben FTP kliensen keresztül. Itt fontos, hogy álíltható legyen felületből a különböző beállítás (pl hova mentse a letöltött zenéket, milyen ftp adatokkal lépjen be a szerverre stb), hogy a műsorvezetők ezt könnyedén használni tudják. Első körben itt is JSON konfigurációs fájlt fogunk használni később ez is cserélhető lenne.  Ennek megvalósításra meghagynánk a Falsk-et. 

A MediaClient-en keresztül lehet regisztrálni a műsorvezetőket a MediaSzerverre és be lehet jelentkezni, hogy elérhető váljanak azok az API végpontok, amelyek nem publikusak. Ebből későbbiekben egyre több lesz, mert szeretnénk, ha a Hallgatók túdnánka közvetlenül a MediaServeren keresztül eznét kérni, de ez már nagy a jövő zenéje :)

