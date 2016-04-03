.. highlight:: none

Úvod do příkazové řádky
=======================

Než začneme programovat, bude dobré se seznámit s *příkazovou řádkou* – tím
černým okýnkem, které programátoři používají na zadávání příkazů.
Na první pohled může vypadat nepřirozeně, ale dá se na ni zvyknout :)

Příkazová řádka
(respektive program, kterému se říká i *konzole* či *terminál*;
anglicky *command line*, *console*, *terminal*)
se na různých systémech otevírá různě:

* **Windows** (české): Start → Všechny programy → Příslušenství → Příkazový řádek
* **Windows** (anglické): Start → All Programs → Accessories → Command Prompt
* **Mac OS X** (anglické): Applications → Utilities → Terminal
* **Linux** (KDE): Hlavní Menu → hledat Konsole
* **Linux** (Gnome): Super → hledat Terminál

Nevíš-li si rady, zkus buď googlit, nebo se jednoduše zeptat
(na sraze kouče, jinak e-mailem).

Po otevření konzole tě uvítá řádek,
kterým počítač vybízí k zadání příkazu.
Podle systému bude končit buď znakem ``$`` nebo ``>``,
před nímž můžou být ještě další informace:

.. container:: col-md-6 os-unix

    **Unix (Linux, OS X)**::

    $

.. container:: col-md-6 os-windows


    **Windows**::

    >

První příkaz
------------

Začneme jednoduchým příkazem.
Napiš ``whoami`` (z angl. *who am I?* – kdo jsem?)
a stiskni Enter.
Objeví se přihlašovací jméno. U mě to vypadá takhle:

.. container:: col-md-6 os-unix

    **Unix**::

        $ whoami
        helena

.. container:: col-md-6 os-windows

    **Windows**::

        > whoami
        pocitac\helena

.. todo::

    Zvýraznit zadávaný příklad

.. note::

    Znak ``$`` nebo ``>`` je v ukázce jen proto, aby bylo jasné že zadáváme
    příkaz do příkazové řádky.
    Vypíše ho sám počítač (většinou ještě s něčím před ním),
    takže ho nepiš sama! Zadej jen ``whoami`` a Enter.

    Stejně tak počítač sám vypíše přihlašovací jméno.


Aktuální adresář
----------------

Příkazová řádka pracuje vždy v nějakém *adresáři* neboli složce
(angl. *directory*, *folder*).
Ve kterém adresáři zrovna je, to nám poví příkaz ``pwd`` nebo ``cd``
(z angl. *print working directory* – vypiš pracovní adresář,
resp. *current directory* – aktuální adresář).

.. container:: col-md-6 os-unix

    **Unix**::

        $ pwd
        /home/helena/

.. container:: col-md-6 os-windows

    **Windows**::

        > cd
        C:\Users\helena

.. note::

    Aktuální adresář se většinou ukazuje i přímo před znakem ``$`` nebo ``>``,
    ale je dobré ``pwd``/``cd`` znát,
    kdyby ses náhodou ztratila.

Co v tom adresáři je?
---------------------

Příkaz ``ls`` nebo ``dir`` (z angl. *list* – vyjmenovat; *directory* – adresář)
nám vypíše, co aktuální adresář obsahuje – všechny soubory,
včetně podadresářů, které se v aktuálním adresáři nacházejí.

.. container:: col-md-6 os-unix

    **Unix**::

        $ ls
        Applications
        Desktop
        Downloads
        Music
        ...

.. container:: col-md-6 os-windows

    **Windows**::

        > dir
        Directory of C:\Users\helena
        05/08/2014 07:28 PM <DIR>      Applications
        05/08/2014 07:28 PM <DIR>      Desktop
        05/08/2014 07:28 PM <DIR>      Downloads
        05/08/2014 07:28 PM <DIR>      Music
        ...


Změna aktuálního adresáře
-------------------------

Aktuální adresář se dá změnit pomocí příkazu ``cd``
(z angl. *change directory* – změnit adresář).
Za ``cd`` se píše jméno adresáře, kam chceme přejít – pokud máš
adresář *Desktop* nebo *Plocha*, přejdi tam.
Pak nezapomeň  ověřit, že jsi na správném místě.

.. container:: col-md-6 os-unix

    **Unix**:

    .. note::

        Unix rozeznává u adresářů a souborů velikost písmen:
        ``Desktop`` a ``desktop`` není to samé.

    ::

        $ cd Desktop
        $ pwd
        /home/helena/Desktop

.. container:: col-md-6 os-windows

    **Windows**:

    .. note::

        (``cd`` jsme už viděly; ale předtím jsme nepsaly nic za něj)

    ::

        > cd Desktop

        > cd
        C:\Users\helena\Desktop

    .. note::

        Pokud přecházíš do adresáře na jiném disku,
        například D: místo C:, je potřeba *před* ``cd``
        zadat jméno disku jako zvláštní příkaz::

            > cd D:\blabla
            > D:
            > cd
            D:\blabla

Vytvoření adresáře
------------------

Co takhle si vytvořit adresář na PyLadies?
To se dělá příkazem ``mkdir``
(z angl. *make directory* – vytvořit adresář).

.. container:: col-md-6 os-unix

    **Unix**::

        $ mkdir pyladies

.. container:: col-md-6 os-windows

    **Windows**::

        > mkdir pyladies

Potom, co adresář vytvoříš, se zkus zkontrolovat, že tam opravdu je.
Můžeš to udělat buď příkazem ``dir``/``pwd``, nebo i z grafického programu,
kterým normálně hledáš na počítači soubory!

Úkol
----

Zkus v nově vytvořeném adresáři `pyladies` vytvořit adresář `test`,
a zkontrolovat že se opravdu vytvořil.

Budou se hodit příkazy `cd`, `mkdir`, `ls` či `dir`.

Řešení
------

.. todo::

    Nastylovat Řešení

.. container:: col-md-6 os-unix

    **Unix**::

        $ cd pyladies
        $ mkdir test
        $ ls
        test

.. container:: col-md-6 os-windows

    **Windows**::

        > cd pyladies
        > mkdir test
        > dir
        05/08/2014 07:28 PM <DIR>      test

Úklid
-----

Teď vytvořené adresáře zase smažeme. Nemůžeme ale smazat adresář, ve kterém
jsme, takže se vrátíme na `Desktop`.
Nadřazený adresář (ten, který obsahuje ten aktuální), se značí dvěma tečkami:

.. container:: col-md-6 os-unix

    **Unix**::

        $ cd ..
        $ pwd
        /home/helena/Desktop

.. container:: col-md-6 os-windows

    **Windows**::

        > cd ..
        > cd
        /home/helena/Desktop

A nakonec smažeme vytvořený adresář `pyladies`.
K tomu použijeme příkaz `rm` nebo `rmdir`
(z *remove* – odstraň, resp. *remove directory* – odstraň adresář).

.. warning::
    Pozor, příkazová řádka nepoužívá odpadkový koš!
    Všechno se nadobro smaže, takže si dobře překontroluj, že mažeš správný
    adresář.

.. container:: col-md-6 os-unix

    **Unix**::

        $ pwd
        /home/helena/Desktop
        $ rm -rv pyladies
        removed directory: ‘pyladies’

.. container:: col-md-6 os-windows

    **Windows**::

        > cd
        /home/helena/Desktop
        > rmdir /S pyladies
        pyladies, Are you sure <Y/N>? Y

Konec
-----

A to je vše! Můžeš příkazovou řádku zavřít.
To se dělá příkazem `exit`.

.. container:: col-md-6 os-unix

    **Unix**::

        $ exit

.. container:: col-md-6 os-windows

    **Windows**::

        > exit

Malý seznam příkazů
-------------------

Tady je tabulka základních příkazů.

.. table::
    :class: table table-striped

    ==============  ==================  ==================================  ==================================================================
    Příkaz (Unix)   Příkaz (Windows)    Popis                               Příklad použití
    ==============  ==================  ==================================  ==================================================================
    exit            exit                ukončení                            ``exit``
    cd              cd                  změna adresáře                      ``cd test``
    ls              dir                 výpis adresáře                      ``ls``
    cp              copy                kopírování souboru                  ``cp /home/helena/test/test.txt /home/helena/test/kopie_test.txt``
    mv              move                přesun (nebo přejmenování) souboru  ``mv /home/helena/test/a.txt /home/helena/test/b.txt``
    mkdir           mkdir               vytvoření adresáře                  ``mkdir test``
    rm              del                 smazání souboru                     ``rm test.txt``
    ==============  ==================  ==================================  ==================================================================

Příkazů existuje jich samozřejmě daleko víc,
pro dnešek nám ale budou stačit tyhle.
Jen jeden ještě přidáme – příkaz ``python``.

Nejdřív ho ale musíme :doc:`nainstalovat <install-python>`.

.. todo::

    Nastylovat patičku

------

Přeloženo z `tutoriálu Django Girls`_.

Licence: `Creative Commons Attribution-ShareAlike 4.0 International`__

Pro PyLadies Brno napsal Petr Viktorin.

__ cc-by-sa_
.. _cc-by-sa: http://creativecommons.org/licenses/by-sa/4.0/
.. _tutoriálu Django Girls: http://tutorial.djangogirls.org/intro_to_command_line/README.html

