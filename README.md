# mediaserver-client

## media szerver
A szerver fő feladata, hogy folymatosan figyelje a a rádió mappáját, amelyben elhelyezésre kerülnek tematikusan a a zenék. Figyeli, folyamatosan, ha új zene kerül be vagy épp törölve lesz vagy egy adott file modosításra kerül. Ezért a Watchdog rész felel. Ha új zene kerül feltöltésre vagy törlése, akkor értelem szerűen az adatbázisból ezt törli vagy létrehozza. A zenei fájlok meta adatát is olvassa ezeket is elmenti. A másik fő része egy webes kis alkalmazás, ez jelenleg elég elmaradott. Szerepe, hogy az adatbázisban megtalálható zenéket lehessen listázni és a meta adatokat szerkeszteni. (Ezeket tudja jelenleg, de van mit optimalizálni a kód minőségén)

Jelenleg a szerver Flaskben van írva de gondolkodunk rajta, hogy djnago is megérhetné. A szerver egy REST API-t is biztosít külső kliensek számára, amelyen keresztül lehetne a zenei adatbázsban keresni. Ez jelenleg a kliens számára a legfontosabb. Egy auth is jó lenne bele, hogy esetleg a műsorvezetői kliensbe egy bejelentkezés felület is legyen a későbbiekben ez tovább fejlesztés céljából lenne jó.

## medi client
A kliens lényegében az adást lebonyolító műsorvezetők számára érdekes. Ezen keresztül tudnak keresni a zenei adatbázisban. Ha egy adott zene pl a kívánságműsorhoz kell, akkor ezen keresztül le lehet tölteni. Ezt jelenleg egy egyszerű ftp kliensel képzeltem el. Tudjuk, hogy a szervern hol található az adott zene és minden műsorvezetőnek van FTP hozzáférése ezt felhasználva le lehet tölteni a zenéket. 
