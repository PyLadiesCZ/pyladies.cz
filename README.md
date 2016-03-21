# PyLadies.cz

Stránky jsou generované ze šablon Jinja2 v adresáři `templates`.
Zatím je to hlavně na hlavičky a patičky, časem můžeme použít víc
šablonových vychytávek (dědičnost, makra), ať je v tom trochu pořádek.

Soubory jako obrázky, fonty, CSS, JS jsou v `static`.

Původní stránky jsou v  `original`; podadresář `v1` obsahuje kurz a musí
být zveřejněn na setjných URL jako předtím.

V `course` snad časem bude kurz převedený do ReST dokumentace.

V `plans` jsou data pro seznamy lekcí (zatím pro Brno).

Celé dohromady to spojuje `conf.py`; tady se např. přidávají nové podstránky.

## Jak vytvořit stránky

### Instalace

    $ python -m pip install -r requirements.txt

### Vytvoření stránek

    $ sphinx-build -b html . _build/html

(na Linuxu postačí zadat `make`)

Stránky se vytvoří v adresáři `_build/html`.

### Nasazení

Spuštěním `make dirhtml` vzniknou v adresáři `_build/dirhtml`
statické stránky k nasazení na webový server.


## Základné informácie - editace HTML

**Správa kurzov na úvodnej stránke** <br /><br />
<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/icon/pylady.png" width=100 height=55 /><br /> - kurz, ktorý práve beží. Ikonka - obrázok pylady.png. V kóde označený takto:
```
<div class="col-xs-12 col-sm-12 col-md-4 col-lg-4 course-i">
  <div class="py-icon">
    <img src="{{ pathto('_static/img/icon/pylady.png', 1) }}" class="py-icon-i" />
  </div>
  <div class="py-block pull-left">
    <h4 class="city-heading">Praha</h4>
    <p class="city-info">01.01. - 31.04. 2016</p>
    <p class="city-address">
      <a href="https://www.google.cz/maps/place/Florentinum/@50.0888957,14.4353417,15z/data=!4m2!3m1!1s0x0:0x90e42b8069106734" target="new">Na Florenci 2116/15, 110 00</a>
    </p>
  </div>
</div>
```

<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/icon/pylady-grey.png" width=100 height=55 /><br /> - kurz, ktorý práve nebeží a nie je spustená registrácia. Ikonka - obrázok pylady-grey.png. V kóde označený takto:
```
<div class="col-xs-12 col-sm-12 col-md-4 col-lg-4 course-i">
    <div class="py-icon">
      <img src="{{ pathto('_static/img/icon/pylady-grey.png', 1) }}" class="py-icon-i" />
    </div>
    <div class="py-block pull-left">
      <h4 class="city-heading">Brno</h4>
      <p class="city-info">Kurz práve neprebieha.</p>
      <p class="city-address">
        <a href="mailto: a@a.com">Napíš nám</a>
      </p>
    </div>
</div>
```

<img src="https://github.com/PyLadiesCZ/pyladies.cz/blob/master/static/img/icon/pylady-blue.png" width=100 height=55 /><br /> - kurz, ktorý práve nebeží, ale je spustená registrácia. Ikonka - obrázok pylady-blue.png. V kóde označený takto:
```
<div class="col-xs-12 col-sm-12 col-md-4 col-lg-4 course-i">
  <div class="py-icon">
    <img src="{{ pathto('_static/img/icon/pylady-blue.png', 1) }}" class="py-icon-i" />
  </div>
  <div class="py-block pull-left">
    <h4 class="city-heading">Praha</h4>
    <p class="city-info">Nový štart od 01.01. - 31.04. 2016</p>
    <p class="city-address">
      <a href="#">Registračný formulár</a>
    </p>
  </div>
</div>
```
**Správa obrázkov**<br />
<ul>
  <li>Banner na úvodnej stránke - 1500px x 655px</li>
  <li>Banner v detailoch miest - 1850px x 400px</li>
  <li>Fotky - detail mesta - 1920px x 1278px</li>
</ul>

**Zmena obrázkov podľa miest v banneroch**
Obrázky sú definované v CSSku. Pre každé mesto je spoločná trieda intro-city, s tým, že obrázok pre každé mesto sa zmení v triede **intro-city-{city-name}**. (Príklad triedy: intro-city-praha).

**Správa kurzov na stránke materiálov**
<ul>
  <li>Aktívny kurz (sekcia Intro header v súbore praha.html)</li>
  <li>Neaktívny kurz (sekcia Intro header v súbore brno.html)</li>
</ul>

**Stavu kurzu - stránka kurzu (Praha)**
<ul>
  <li>Prejdená hodina - zmena ikonky na <strong>glyphicon-ok</strong></li>
  <li>Ešte neprejdená hodina - ikonka <strong>glyphicon-remove</strong></li>
  <li>Vyznačenie aktívnej aktuálnej hodiny - trieda <strong>section-active</strong></li>
</ul>
