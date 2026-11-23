# Silos pod Fox Landem: projekt poziomu (v198)

Inspiracja: serial o podziemnym silosie (centralne schody spiralne, numerowane piętra, ekran z widokiem na zewnątrz, śluza, podział społeczny według głębokości). Zapożyczone są tylko ogólne motywy architektoniczne. Nie ma nazw, postaci, logo ani scen z serialu.

## 1. Założenia

- Nie zmieniłem ekonomii ani zapisu gry. Poziom czyta te same dane `GD.silo` (głębokość, piętra, poziomy I–III, wydarzenie), które już istnieją od v133.
- Skala jest 1:1 w metrach. Stary widok 3D miał 3,4 m na każde 25-metrowe piętro. Nowy pokazuje prawdziwe 300 m głębokości.
- Przekrój 2D (📐) działa bez zmian.

## 2. Wymiary

| Element | Wartość | Uzasadnienie |
|---|---|---|
| Średnica wewnętrzna | 24 m (Ø zewn. 26,4 m) | Daje 8 m głębokości użytkowej pierścienia, czyli realne pomieszczenia |
| Ściana | 1,2 m żelbetu | Rząd wielkości typowy dla głębokich szybów |
| Sektor (= „piętro” w grze) | 25 m | Bez zmian (mechanika v133) |
| Kondygnacja | 5 m (strop 0,45 m, w świetle 4,55 m) | 5 kondygnacji na sektor, miejsce na kanały i oświetlenie |
| Atrium | promień 3,9 m | Pusta przestrzeń wokół schodów |
| Schody spiralne | promień 0,55–3,0 m, 28 stopni na kondygnację, 17,9 cm wysokości stopnia | Jeden pełny obrót na kondygnację, więc podest wypada zawsze w tym samym miejscu |
| Winda towarowa | kabina 2,1 × 2,1 m | Przystanek na każdej kondygnacji |

## 3. Układ pionowy

```
 +10 m  kopiec ziemny, maszt kamery (zasila Okno), 2 wywietrzniki, portal tunelu
   0 m  KOPUŁA: stołówka z ekranem „Okno”, kuchnia, śluza z drzwiami skarbcowymi
 −25…−100 m   STREFA GÓRNA     ciepłe światło, tynk z drewnianym cokołem
−100…−200 m   STREFA ŚRODKOWA  świetlówki, zielono-szare ściany
−200…−300 m   GŁĘBIA           sodowe światło, surowy beton z zaciekami rdzy, ciemniej
   dno  czoło wykopu (wiertnica, koparka, górnicy, kubeł urobku, pompa)
        albo MECHANIKA po osiągnięciu 300 m (generatory, pompownia, studzienka)
```

Przekrój gruntu jest uproszczony i orientacyjny dla Pomorza: gleba, glina zwałowa, piaski wodonośne (ok. 36–82 m), iły, piaski glaukonitowe, margle kredowe (wodonośne). Warstwy wodonośne uzasadniają wydarzenie „Awaria pompy”. To stylizacja, nie dane z odwiertu.

## 4. Sektor: plan kondygnacji

- **Centrum**: schody spiralne w atrium. To kręgosłup poziomu i jego najmocniejszy element wizualny.
- **Pierścień 3,9–12 m**: przy atrium biegnie korytarz z balustradą, za nim pomieszczenia otwarte w stronę kamery (przekrój „domek dla lalek”).
- **Podest**: zawsze z tyłu, na osi. Nad nim jest wymalowany szablonem numer głębokości („−130 m”), widoczny z każdego miejsca.
- **Dwa korytarze poprzeczne** prowadzą od atrium do ściany. Mieszkańcy chodzą korytarzem i nimi, a nie przez meble.
- **Piony instalacyjne** (woda, powietrze, kable) biegną przy ścianach, a pod sufitem kanał wentylacyjny.
- **Poziom I / II / III** oznacza 2 / 3 / 5 wyposażonych kondygnacji sektora. Reszta to plac budowy (rusztowanie, cement, lampa, ekipa). Rozbudowa ma więc widoczny efekt.

Wyposażenie typów: magazyn (regały paletowe), farma (3 łuki regałów hydroponicznych z lampami LED, zbiorniki), warsztat (stoły, tokarka, wieżyczka w montażu, kabina spawalnicza, suwnica), zbrojownia (stojaki rakiet, klatka, wózek startowy), schron (łóżka piętrowe, szafki, stoły), dział IT (szafy serwerowe z mrugającymi diodami, ściana z radarem na żywo, biurka), mieszkania (5 lokali po ok. 25–30 m²).

## 5. Opowiadanie światem (wydarzenia widoczne w 3D)

| Wydarzenie | Co widać |
|---|---|
| Awaria pompy | woda podnosi się na dnie, kogut |
| Niepokój na dolnych piętrach | transparent „RACJE, NIE OBIETNICE!”, górnicy siedzą, wiertło i koparka stoją |
| Jaskinia pod szybem | otwór w ścianie szybu, świecące oczy |
| Stary sprzęt | otwarta skrzynia wojskowa z częściami |
| Ktoś chce wyjść | zwiadowca w skafandrze czeka w śluzie, kogut nad drzwiami |

## 6. Nawigacja

- Pasek z prawej (⌂, −1…−12, ⛏️/⚙️) przenosi kamerę na wybrane piętro. Kolory pasują do strefy.
- Lewy górny róg pokazuje bieżącą strefę i głębokość.
- Etykiety pięter są przy krawędzi przekroju. Dotknięcie człowieka pokazuje jego imię, zajęcie i kwestię.

## 7. Wydajność (zmierzone w teście)

Wydajność zmierzyłem w Chromium z programowym WebGL. Liczby FPS z tego testu nie przekładają się na telefon.
- Sceny ma od 77 do 373 wywołań rysowania i od 59 do 156 tys. trójkątów.
- Statyczne obiekty są scalane w jedną geometrię na materiał w obrębie sektora. Schody to jedna instancja na cały szyb.
- Rysowane są tylko sektory blisko kamery. Okno renderuje się do tekstury 320×132 co 4. klatkę i tylko wtedy, gdy Kopuła jest w kadrze.
- Na prawdziwym telefonie tego nie testowałem.

## 8. Uproszczenia, o których trzeba wiedzieć

- Tuż po odkopaniu piętra czoło wykopu rysuje się co najmniej 4,5 m pod ostatnim stropem, żeby górnicy się zmieścili.
- Kopiec, maszt i wywietrzniki są wspólne dla wszystkich graczy. Nie odzwierciedlają budynków z bazy.

## 9. Propozycje rozgrywki (NIE wdrożone, bo zmieniają balans i wymagają Twojej decyzji)

1. **Okno pokazuje Twój zjazd.** Na ekranie stołówki leci powtórka najlepszego przejazdu (powtórki istnieją od v136). Zgadza się to z fabułą („bogaci oglądają zjazdy”) i daje gotowy materiał do udostępniania.
2. **Premia strefowa +10%.** Farma w Strefie Środkowej, zbrojownia i warsztat w Głębi, mieszkania w Strefie Górnej. Daje decyzję przy wyborze piętra, ale zmienia ekonomię.
3. **Pompy w Głębi.** Kopanie poniżej 200 m (warstwa kredowa) wymaga utrzymania pompowni. To nowy wydatek monet, który hamuje tempo w końcówce.
4. **Tragarze.** Codzienne mini-zadanie: metry przewyższenia z podjazdów rowerowych napędzają dostawy schodami (np. bonus do farmy).
5. **Zwiad przez śluzę jako scena.** Po decyzji „Pozwól mu wyjść” zwiadowca przechodzi przez śluzę i widać go na Oknie.

## 10. Biznes

**Fakty z kodu**: gra ma już okres próbny i kod zakupu (v189), grafikę 9:16 „Twój tydzień” (v188) i ranking okolicy (v190).

**Propozycje, z założeniami do sprawdzenia:**
- **Wideo i zrzuty 9:16 z przekroju silosu („mój silos ma −175 m”)**: to tani materiał na TikTok. Przelot kamery od Kopuły do dna ma naturalny „hak” w postaci głębokości. Koszt to tylko praca. Skuteczności nie da się przewidzieć bez testu na kilku filmach.
- **Kosmetyka silosu** (kolory stref, lampy, szablony numerów, motywy Okna): to monetyzacja bez wpływu na balans. Jej sens zależy od liczby aktywnych graczy, której nie znam.
- **Ryzyko prawne**: w reklamach nie używaj nazwy serialu, jego logo ani kadrów. Inspiracja motywem jest w porządku, sugerowanie powiązania z marką już nie.
