# pyladies.cz

Website of the Czech PyLadies chapter / Web českých PyLadies.

[![Travis CI kontrolka](https://travis-ci.org/PyLadiesCZ/pyladies.cz.svg?branch=master)](https://travis-ci.org/PyLadiesCZ/pyladies.cz)

*Pokud je kontrolka zelená, povedlo se dostat poslední změny z větve `master` do ostrého provozu. Má-li jinou barvu, stala se [někde po cestě](https://travis-ci.org/PyLadiesCZ/pyladies.cz) chyba.*


### Licence

* Kód: [MIT](LICENSE)
* Materiály: [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## Obsah README
**Obecně**

[Jak to funguje](#jak-to-funguje)

[Jak vytvořit stránky](#jak-vytvorit-stranky)

**Editace HTML**

[Nastavení aktuálních kurzů na úvodní stránce](#uvodni-stranka)

[Nastavení obrázků](#nastaveni-obrazku)

[Nastavení informací o aktuálním kurzu na stránce materiálů](#nastaveni-informaci-o-aktualnim-kurzu)

[Stav kurzu - probrané a neprobrané lekce](#probrane-neprobrane)

[Stav kurzu - vytvoření plánu kurzu či přesun lekcí v kurzu](#presun-lekci)

[Aktuální a proběhlé kurzy](#kurzy-mesta)

## <a name="jak-to-funguje">Jak to funguje

Stránky jsou generované ze šablon Jinja2 v adresáři `templates`.
Zatím je to hlavně na hlavičky a patičky, časem můžeme použít víc
šablonových vychytávek (dědičnost, makra), ať je v tom trochu pořádek.

Soubory jako obrázky, fonty, CSS, JS jsou v `static`.

Původní stránky jsou v  `original`; podadresář `v1` obsahuje kurz a musí
být zveřejněn na stejných URL jako předtím.

V `course` snad časem bude kurz převedený do ReST dokumentace.

V `plans` jsou data pro seznamy lekcí. Mění se tu datumy, probrané/neprobrané lekce, přesun témat.

Celé dohromady to spojuje `pyladies_cz.py`; tady se např. přidávají nové
podstránky.

## <a name="jak-vytvorit-stranky">Jak vytvořit stránky

### Instalace

    $ python -m pip install -r requirements.txt

### Spuštění webu lokálně v PC

    $ python pyladies_cz.py serve

Stránky se zpřístupní na adrese `http://127.0.0.1:8003/`.
Změny v kódu se projeví po obnovení stránky v prohlížeči.

### Úprava souborů

* Soubory html jsou ve složce ``templates``
* Úprava hlavičky webu, hlavního menu a patičky stránky v souboru `templates/layout.html`
* CSS soubory sa nacházejí v `static/css`
* Obrázky se nacházejí v `static/img`
* Přiřazování obrázků `src="{{ pathto('_static/img/{subfolder}/{image}', 1) }}"`

### Nasazení

(Tohle je pro spuštění „ostré” verze webu; většinou to nebudeš potřebovat)

Tento příkaz vytvoří v adresáři `_build`
statické stránky k nasazení na webový server.:

    $ python pyladies_cz.py freeze

### <a name="kurzy-mesta">Aktuální a proběhlé kurzy (stránka kurzů se upravuje v souboru `meetups/brno.yml`)
Každé město má vlastní stránku s aktuálními a proběhlými kurzy. Dříve či později se z toho stane taková kronika.

První kurz v seznamu se ukáže na hlavní stránce.

***V meetupech lze nastavit:***

* `name`: jméno akce

* `topic`: téma akce

* `start` a `end`: datum ve formátu `2017-02-13`, pokud má akce pevný termín od do

* `date`: datum jednodenní akce (`start` a `end` by byly stejné)

* `time`: čas od do, případně i den v týdnu

* `place`: místo, kde sraz probíhá (pokud je víc srazů v jednom místě, dá se v YAMLu místo nasdílet dalším srazům, viz ukázky v těch YAML souborech)

    * `name`: jméno místa
    * `address`: adresa
    * `latitude`, `longitude`: mapové souřadnice
    * `url`: odkaz (chybí-li, ukáže se odkaz na mapu podle latitude/longitude)

* `registration`: informace o registraci

    * `url`: odkaz na registrační formulář
    * `end`: konec registrace (dá se vynechat, pokud je registrace aktuální až do konce kurzu – třeba u opakujících se srazů)
    * `text`: text, který se objeví v odkazu (místo "Registrace právě probíhá!")

* `parallel-with-previous`: `true` pokud je kurz paralelní s předchozím.
  (Informace o paralelních kurzech se občas zobrazují společně.)


***Ukázky variant kurzu (dají se kombinovat):***

** Kurz má jasný start a konec, místo, čas registraci**

```
- name: Začátečnický kurz <br> Jarní pondělí 2017
  start: 2017-02-27
  end: 2017-05-29
  time: pondělky 18:00 – 20:00
  place:
    name: Odbor školství
    address: Cejl 73, Brno
    latitude: '49.1992294'
    longitude: '16.6235206'
  registration:
    url: <tady_bude_adresa>
    end: 2017-02-19
```

** Kurz je jednodenní a má například téma**

```
- name: Lednový PyWorking <br> meetup pro pokročilé začátečníky
  topic: Django Polls
  date: 2017-01-28
  time: 9:00 - 17:30
  place:
    name: MSD IT (Riverview)
    address: Svornosti 3321/2, Praha 5
    latitude: '50.0670442'
```

** Jsou to pravidelné srazy**

```
- name: Advanced PyLadies & PyWorking Praha <br> pokročilé a doučovací srazy
  time: pondělky ve 14 denních intervalech, 18:00 - 20:00
  registration:
    url: <tady_bude_adresa>
```
    


### <a name="nastaveni-obrazku">Nastavení obrázků

* Banner na úvodní stránce - 1500px × 655px
* Banner v detailu měst - 1850px × 400px
* Fotky - detail města - 1920px × 1278px

**Změna obrázků podle měst v banerech**

Obrázky jsou definované v CSS. Pro každé město je společná třída intro=city, s tím, že obrázek pro každé město se změní v třídě **intro-city-{city-name}**. (Příklad třídy: intro-city-praha).

### <a name="nastaveni-informaci-o-aktualnim-kurzu">Nastavení informací o aktuálním kurzu na stránce materiálů

* Aktivní kurz (př. v sekci ```Started course Prague``` v souboru `templates/praha.html`)
* Neaktivní kurz (př. v sekci ```Started course Brno``` v souboru `templates/brno.html`)

### <a name="probrane-neprobrane">Stav kurzu - probrané a neprobrané lekce (stránka materiálů kurzu v souboru `plans/praha.yml`)

* Probraná lekce ```done: true```
* Neprobraná lekce ```done: false```

***Ukázka pro probranou a neprobranou lekci na webu:***
<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/readme-course-plan-1.png" /><br /> 

### <a name="presun-lekci">Stav kurzu - vytvoření plánu kurzu či přesun lekcí v kurzu (stránka materiálů kurzu v souboru `plans/praha.yml`)
Každé město může mít vlastní plán kurzu. Případně navíc speciální lekce.

***Ukázka pro běžnou lekci:***
<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/readme-course-plan-2.png" /><br /> 

```
- name: Seznamy
  date: 2016-11-14
  done: true
  materials:
  - name: Turnaj v piškvorkách
    type: special
  - name: Seznamy
    type: lesson
    link: v1/s006-lists/lists2.html
  - name: N-tice
    type: lesson
    link: v1/s006-lists/tuples.html
  - name: Tahák na seznamy
    type: handout
    link: https://github.com/pyvec/cheatsheets/raw/master/lists/lists-cs.pdf
  - name: Domácí projekty (PDF)
    type: homework
    link: v1/s006-lists/handout/handout6.pdf
  - name: Celý kód na hru z lekce o seznamech
    type: link
    link: v1/cele-kody/seznamy.py
```



***Ukázka pro domluvené speciální lekce nad rámec běžného výkladu (např. z odboček)- probrané a neprobrané:***
<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/readme-course-plan-3.png" /><br /> 

```
- name: Vánoční speciál
  date: 2016-12-19
  done: true
  materials:
  - name: MicroPython a světýlka
    type: special-lesson
- name: Relační databáze (SQLite a SQLAlchemy)
  date: 2016-01-02
  done: false
  materials:
  - name: Relační databáze
    type: special-lesson
```
