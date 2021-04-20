# Media Server

* ## About the project
A szerver fő feladata, hogy folymatosan figyelje a a rádió mappáját, amelyben elhelyezésre kerülnek tematikusan a a zenék. Figyeli, folyamatosan, ha új zene kerül be vagy épp törölve lesz vagy egy adott file modosításra kerül. Ezért a Watchdog rész felel. Ha új zene kerül feltöltésre vagy törlése, akkor értelem szerűen az adatbázisból ezt törli vagy létrehozza. A zenei fájlok meta adatát is olvassa ezeket is elmenti. A másik fő része egy webes kis alkalmazás, ez jelenleg elég elmaradott. Szerepe, hogy az adatbázisban megtalálható zenéket lehessen listázni és a meta adatokat szerkeszteni. (Ezeket tudja jelenleg, de van mit optimalizálni a kód minőségén)

Jelenleg a szerver Flaskben van írva. A szerver egy REST API-t is biztosít külső kliensek számára, amelyen keresztül lehetne a zenei adatbázsban keresni. Ez jelenleg a kliens számára a legfontosabb. Egy auth is jó lenne bele, hogy esetleg a műsorvezetői kliensbe egy bejelentkezés felület is legyen a későbbiekben ez tovább fejlesztés céljából lenne jó.


* ## Further steps
Az egyik legfontosabb lépés a szerver rendberakása, mert ez a központja az egész mókának. Itt is több teendő van. A legfontosabb lenne átstruktúrálni a kódot és tényelegesen szétválasztani a különböző rétegeket. 
Mindenképp a Modell Controller réteget szépen el kell különíteni de akár egy olyan struktúrát is el tudok képzelni, hogy Controller Service Repository és Model. A repository (dao) réteg talán azért lenne jó, mert azt akár használhatná a Watchdog is minden további nélkül.

A kód szervezéshez bevezetésre szeretnénk hozni a Depedency Injection ( https://python-dependency-injector.ets-labs.org/ , https://github.com/alecthomas/flask_injector ) ezzel sokminden egyszerűsödhetne. Ennek valami kezdeménye volt az App osztály de jobbank látom olyan megvalósításra támaszkodni, amely könynen használható. 

Egyenlőre magának a webservice-nek pusztány annyit kell tudni, hogy le lehessen kérdezni az összes zenét, erre én továbbra is támogatom a pagebale ötletet valamint esetleg egy két filter paraméter nem ártana a különböző meta adatok szerint. 

A szerver másik része maga a library kezelő. A library kezelő igazából nagyjából rendben is lenne csak valamilyen formában jó lenne elkülöníteni a többi részétől az alkalmazásnak és átültetni ezt is OOP keretek közé. Igazából teljesen futthatna a háttérben. 

A media serverből a kliens teljesen ki fog kerülni és a MediaClient fogja ellátni ezt a feladatot is a definált API-n keresztül

A Flaskhez léteznek JWT támogtaó library ez tök jó lenne, mert maga a MediaClient egy egyszerű webalkalmazás lenne, amit szeretnénk elválasztani a szervertől, hogy könnyen mozgatható legyen a szerver nélkül is. 
