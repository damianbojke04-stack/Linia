# Jak wgrać grę na Netlify (od wersji v200)

Gra nie jest już jednym plikiem. Na serwer trafia **cała zawartość folderu `rewir/`**:

| Plik / folder | Co to | Kiedy telefon go pobiera |
|---|---|---|
| `index.html` | rdzeń gry (mapa, jazda, baza, blokada ekranu…) | przy starcie |
| `i18n-en.js` | słownik angielski | tylko gdy gra jest po angielsku |
| `m/silo3d.js` | silos 3D | przy pierwszym otwarciu zakładki Silos |
| `img/*.webp` | obrazki budynków (poziomy I–III) | tylko te budynki, które są rysowane |

Pliki, które już masz na Netlify (`sw.js`, `manifest.webmanifest`, ikony, `fox/`, `og.jpg`), zostają bez zmian.

Moduły i słownik, które telefon raz pobrał, zostają w jego pamięci, więc działają bez internetu.
Gdy `sw.js` dostanie listę nowych plików, będą dostępne offline także zanim gracz pierwszy raz ich użyje.

## Zmiany w kodzie
- Rdzeń: `rewir/index.html`.
- Silos 3D: edytuj `zrodla/silo3d.js`, potem uruchom `python3 narzedzia/zbuduj-moduly.py`.
- Teksty angielskie: `rewir/i18n-en.js`.
- Wersja jednoplikowa sprzed podziału: `archiwum/rewir-v199-jeden-plik.html`.
