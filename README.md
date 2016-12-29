# pyladies.cz

Website of the Czech PyLadies chapter / Web českých PyLadies.

[![Travis CI kontrolka](https://travis-ci.org/PyLadiesCZ/pyladies.cz.svg?branch=master)](https://travis-ci.org/PyLadiesCZ/pyladies.cz)

*Pokud je kontrolka zelená, povedlo se dostat poslední změny z větve `master` do ostrého provozu. Má-li jinou barvu, stala se [někde po cestě](https://travis-ci.org/PyLadiesCZ/pyladies.cz) chyba.*


## Licence

* Kód: [MIT](LICENSE)
* Materiály: [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

## Jak to funguje

Stránky jsou generované ze šablon Jinja2 v adresáři `templates`.
Zatím je to hlavně na hlavičky a patičky, časem můžeme použít víc
šablonových vychytávek (dědičnost, makra), ať je v tom trochu pořádek.

Soubory jako obrázky, fonty, CSS, JS jsou v `static`.

Původní stránky jsou v  `original`; podadresář `v1` obsahuje kurz a musí
být zveřejněn na setjných URL jako předtím.

V `course` snad časem bude kurz převedený do ReST dokumentace.

V `plans` jsou data pro seznamy lekcí. Mění se tu datumy, probrané/neprobrané lekce, přesun témat.

Celé dohromady to spojuje `pyladies_cz.py`; tady se např. přidávají nové
podstránky.

## Jak vytvořit stránky

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

## Základní informace o kurzech, které se často mění - editace HTML

### Nastavení aktuálních kurzů na úvodní stránce <br /><br />
**Nezapomeň vždy změnit {{ pathto('mesto') }} pro dané město!**

<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/icon/pylady.png" width=100 height=55 /><br /> - kurz, který právě běží. Ikonka - obrázek pylady.png. Kód:
```
<div class="col-xs-12 col-sm-12 col-md-4 col-lg-4 course-i">
  <div class="py-icon">
    <img src="{{ pathto('_static/img/icon/pylady.png', 1) }}" class="py-icon-i" />
  </div>
  <div class="py-block pull-left">
    <a href="{{ pathto('praha') }}"><h4 class="city-heading">Praha - začátečnický kurz</h4>
    <p class="city-info">01.01. - 31.04. 2016</p>
    <p class="city-address">
      <a href="https://www.google.cz/maps/place/Florentinum/@50.0888957,14.4353417,15z/data=!4m2!3m1!1s0x0:0x90e42b8069106734" target="new">Na Florenci 2116/15, 110 00</a>
    </p>
  </div>
</div>
```

<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/icon/pylady-grey.png" width=100 height=55 /><br /> - kurz, který právě nebeží a není spuštěná registrace. Ikonka - obrázek pylady-grey.png. Kód:
```
<div class="col-xs-12 col-sm-12 col-md-4 col-lg-4 course-i">
    <div class="py-icon">
      <img src="{{ pathto('_static/img/icon/pylady-grey.png', 1) }}" class="py-icon-i" />
    </div>
    <div class="py-block pull-left">
      <a href="{{ pathto('brno') }}"><h4 class="city-heading">Brno - začátečnický kurz</h4>
      <p class="city-info">Kurz právě neprobíhá.</p>
      <p class="city-address">
        <a href="mailto: a@a.com">Napiš nám.</a>
      </p>
    </div>
</div>
```

<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/icon/pylady-blue.png" width=100 height=55 /><br /> - kurz, který právě nebeží, ale je spuštěná registrace. Ikonka - obrázek pylady-blue.png. Kód:
```
<div class="col-xs-12 col-sm-12 col-md-4 col-lg-4 course-i">
  <div class="py-icon">
    <img src="{{ pathto('_static/img/icon/pylady-blue.png', 1) }}" class="py-icon-i" />
  </div>
  <div class="py-block pull-left">
    <a href="{{ pathto('ostrava') }}"><h4 class="city-heading">Ostrava - začátečnický kurz</h4>
    <p class="city-info">Proběhne od 01.01. - 31.04. 2016</p>
    <p class="city-address">
      <a href="#">Registrační formulář</a>
    </p>
  </div>
</div>
```
### Nastavení obrázků

* Banner na úvodní stránce - 1500px × 655px
* Banner v detailu měst - 1850px × 400px
* Fotky - detail města - 1920px × 1278px

### Změna obrázků podle měst v banerech

Obrázky jsou definované v CSS. Pro každé město je společná třída intro=city, s tím, že obrázek pro každé město se změní v třídě **intro-city-{city-name}**. (Příklad třídy: intro-city-praha).

### Nastavení informací o aktuálním kurzu na stránce materiálů

* Aktivní kurz (př. v sekci ```Started course Prague``` v souboru `templates/praha.html`)
* Neaktivní kurz (př. v sekci ```Started course Brno``` v souboru `templates/brno.html`)

### Stav kurzu - probrané a neprobrané lekce (stránka materiálů kurzu v souboru `plans/praha.yml`)

* Probraná lekce ```done: true```
* Neprobraná lekce ```done: false```

***Ukázka pro probranou a neprobranou lekci na webu:***
<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/readme-course-plan-1.png" /><br /> 

### Stav kurzu - vytvoření plánu kurzu či přesun lekcí v kurzu (stránka materiálů kurzu v souboru `plans/praha.yml`)
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
    
    

