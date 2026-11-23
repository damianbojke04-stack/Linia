# Rewir: dwie wersje tej samej gry (od v200)

## 1. Jeden plik: `zrodla/rewir.html` (ZRÓDŁO, tu robimy zmiany)
- Działa wszędzie: otwarty na telefonie w podglądzie pliku, z dysku i na Netlify (jako `index.html`).
- three.js (grafika 3D) pobiera się dopiero po otwarciu zakładki Silos, a nie przy każdym starcie.
- Rozmiar: 2,4 MB pliku, ok. 740 KB do pobrania po kompresji na serwerze.

## 2. Wersja dla serwera: folder `rewir/` (generowana automatycznie)
- Pobiera tylko potrzebne części. Start po polsku to ok. 460 KB zamiast ok. 860 KB.
  - `index.html`: rdzeń gry.
  - `i18n-en.js`: słownik angielski, tylko gdy gra jest po angielsku.
  - `img/*.webp`: obrazki budynków, pobierane przy rysowaniu.
  - `m/silo3d.js`: silos 3D, przy pierwszym otwarciu zakładki.
- Działa TYLKO z serwera (Netlify), bo potrzebuje sąsiednich plików. Otwarty sam w podglądzie na telefonie
  pokaże przekrój silosu i komunikat zamiast widoku 3D.
- Na Netlify wgraj całą zawartość `rewir/` obok obecnych plików (`sw.js`, manifest, ikony, `fox/` zostają bez zmian).
- Po każdej zmianie w `zrodla/rewir.html` zbuduj na nowo:  `python3 narzedzia/podziel.py`

Raz pobrane moduły i słownik zostają w pamięci telefonu, więc działają bez internetu.
Archiwum wersji sprzed zmian: `archiwum/rewir-v199-jeden-plik.html`.
