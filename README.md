# Agent vizualizace

Lokální workflow pro modelování exteriéru domu v Blenderu a interaktivní zasazení do fotografie. Editor používá skutečnou vyhodnocenou geometrii modelu, nikoliv obrázek domu.

## Co je součástí

- Obecný demonstrační model: hmota domu, sedlová střecha a jednoduché fasádní prvky. Klientské modelovací skripty nejsou publikované.
- Export vyhodnocené geometrie a kalibrované kamery do editoru.
- Samostatný HTML editor bez knihoven a bez externích síťových požadavků.
- Posun v terénu, otočení kolem X/Y/Z, měřítko, zobrazení původní fotky.
- Export náhledu PNG 3600 × 2400 a přenositelného nastavení JSON.
- Přenos nastavení z editoru zpět do Blenderu.

Klientské fotografie, dokumentace, rendery, modely nábytku a přístupové údaje nejsou součástí zdrojového balíčku. Připojují se lokálně. Rozpracované zahradní úpravy ještě nejsou implementované v této verzi.

## Požadavky

Python 3.9+ pro sestavení editoru, Blender 5.2 pro modelování a export, prohlížeč s WebGL. Placené služby nejsou potřeba.

## Lokální postup

1. Připrav pracovní projekt mimo verzované zdrojové soubory a nastav `VIZ_PROJECT_DIR` na jeho absolutní cestu.
2. V Blenderu spusť postupně `blender/01_zaklad.py` a `blender/02_prvky.py`. Jde o obecný demonstrační dům 10 × 8 m, ne obecný převod libovolného stavebního výkresu. Skripty spouštěj jednou v nové scéně; opakované spuštění není idempotentní.
3. Ověř geometrii v renderu. Ukázka používá jednoduché fasádní panely; produkční ostění a stavební otvory je potřeba vymodelovat.
4. Nastav kameru podle vlastní fotografie. Kalibrace je ruční; aplikace ji automaticky neřeší. Fotografie a projekce jsou v této verzi určené pro poměr stran 3:2.
5. Spusť `blender/export_editor.py`. Vytvoří `output/model-data.json` ve tvém projektu.
6. Sestav editor:

```sh
python3 tools/build_editor.py --photo /cesta/foto.jpg --model /cesta/output/model-data.json --output /cesta/editor.html
```

Výsledný HTML soubor obsahuje fotografii i geometrii a lze jej otevřít přímo v prohlížeči. Pokud prohlížeč omezuje lokální soubory, spusť v jeho složce `python3 -m http.server 8765 --bind 127.0.0.1`.

7. Po úpravě klikni na **Uložit nastavení**. Nastav `VIZ_PLACEMENT_FILE` na stažený JSON a v Blenderu spusť `blender/apply_placement.py`. Scénu ulož pod novým názvem.

## Souřadnice a omezení

Metry; X východ, Y sever, Z nahoru. Eulerovy úhly se skládají v pořadí X, Y, Z. Pole `rotation` je historicky osa Z, `rotationX` a `rotationY` jsou náklony. Starší JSON bez náklonů je podporovaný. Výchozí otočení je 0°. Měřítko 100 % odpovídá základním rozměrům příkladu.

Shader v editoru používá zjednodušené materiály a projekční stín. Finální render vzniká v Blenderu. Terén je pracovní vodorovná rovina nastavená vlastností `ground_z` kořenového objektu; pro jiný projekt je nutné přizpůsobit rovinu, základní rozměry i kameru. Zasazení není geodetické zaměření.

Výsledný HTML obsahuje vloženou fotografii. Nesdílej jej veřejně, pokud fotografie není určená ke zveřejnění. `.gitignore` vylučuje běžné lokální podklady a adresáře výstupů; neposuzuje obsah libovolného HTML souboru.
