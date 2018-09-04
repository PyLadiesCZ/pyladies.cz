# pyladies.cz

Web českých PyLadies / Website of the Czech PyLadies chapter.

[![Travis CI kontrolka](https://travis-ci.org/PyLadiesCZ/pyladies.cz.svg?branch=master)](https://travis-ci.org/PyLadiesCZ/pyladies.cz)

*Pokud je kontrolka zelená, povedlo se dostat poslední změny z větve `master` do ostrého provozu. Má-li jinou barvu, stala se [někde po cestě](https://travis-ci.org/PyLadiesCZ/pyladies.cz) chyba.*


### Licence

* Kód: [MIT](LICENSE)
* Materiály: [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## Obsah

[Co je kde](#jak-to-funguje)

[Jak vytvořit stránky](#jak-vytvorit-stranky)

[Aktuální a proběhlé kurzy](#kurzy-mesta)


<a name="jak-to-funguje"></a>
## Co je kde

Stránky jsou generované ze šablon Jinja2 v adresáři `templates`.

Soubory jako obrázky, fonty, CSS, Javascript jsou v `static`.

Původní stránky jsou v  `original`; podadresář `v1` obsahuje kurz a musí
být zveřejněn na stejných URL jako předtím.

V `meetups` jsou data pro seznamy kurzů srazů. Mění se tu datumy, časy, odkazy na materiály.
Více viz [sekce o kurzech](#kurzy-mesta).

V `teams` jsou data pro seznamy lidí – organizátorů a koučů.

V `cities.yml` jsou data o městech, ve kterých PyLadies fungují, včetně kontaktů na PyLadies v konkrétních městech.

V `news.yml` jsou novinky pro hlavní stránku.

Celé dohromady to spojuje `pyladies_cz.py`; tady se např. přidávají nové
podstránky.

<a name="jak-vytvorit-stranky"></a>
## Jak vytvořit stránky

### Instalace

Ve virtuálním prostředí s Pythhonem 3.6 (nebo vyšším) spusť:

    $ python -m pip install -r requirements.txt

### Spuštění webu lokálně v PC

Ve stejném virtuálním prostředí spusť na Linuxu/macOS:

    $ export PYTHONPATH=.

nebo na Windows:

    > set PYTHONPATH=.

a pak (na všech systémech):

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

<a name="kurzy-mesta"></a>
## Aktuální a proběhlé kurzy

Každé město má vlastní stránku s aktuálními a proběhlými kurzy.
Je z toho taková kronika.

Nové kurzy se přidávají na konec `.yml` souboru v adresáři `meetups`.

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
  (Informace o paralelních kurzech se občas zobrazovaly společně.)


### Ukázky variant kurzu (dají se kombinovat)

#### Kurz má jasný start a konec, místo, čas registraci

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

#### Kurz je jednodenní a má například téma

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

#### Jsou to pravidelné srazy

```
- name: Advanced PyLadies & PyWorking Praha <br> pokročilé a doučovací srazy
  time: pondělky ve 14 denních intervalech, 18:00 - 20:00
  registration:
    url: <tady_bude_adresa>
```

