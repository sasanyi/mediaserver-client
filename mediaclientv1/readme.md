# Media Client

* ## About the project
A kliens lényegében az adást lebonyolító műsorvezetők számára érdekes. Ezen keresztül tudnak keresni a zenei adatbázisban. Ha egy adott zene pl a kívánságműsorhoz kell, akkor ezen keresztül le lehet tölteni. Ezt jelenleg egy egyszerű ftp kliensel képzeltem el. Tudjuk, hogy a szervern hol található az adott zene és minden műsorvezetőnek van FTP hozzáférése ezt felhasználva le lehet tölteni a zenéket. 

Jelenleg a kliens is flask alkalmazás, de bármilyen megoldás elképzelhető :) 

* ## Futher steps

Igazából nagyjából az egész lecserélésre kerül HTML + CSS + JS forntendre és maga a python rész pusztán annyiból fog állni, mint most. Lesz, ami betölti a kliens oldalait, valamint egy download url, amely lecsrélésre kerül és kap egy zenei id-t és az annak megfelelő zenéni fájlhoz tartozó path alapján letölti egy mappába a zenét első körben FTP kliensen keresztül. Itt fontos, hogy álíltható legyen felületből a különböző beállítás (pl hova mentse a letöltött zenéket, milyen ftp adatokkal lépjen be a szerverre stb), hogy a műsorvezetők ezt könnyedén használni tudják. Első körben itt is JSON konfigurációs fájlt fogunk használni később ez is cserélhető lenne.  Ennek megvalósításra meghagynánk a Falsk-et. 

A MediaClient-en keresztül lehet regisztrálni a műsorvezetőket a MediaSzerverre és be lehet jelentkezni, hogy elérhető váljanak azok az API végpontok, amelyek nem publikusak. Ebből későbbiekben egyre több lesz, mert szeretnénk, ha a Hallgatók túdnánka közvetlenül a MediaServeren keresztül eznét kérni, de ez már nagy a jövő zenéje :)

