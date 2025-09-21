# Juomamme
Tietokannat ja web-ohjelmointi kurssin harjoitustyö

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

* Käyttäjä pystyy lisäämään sovellukseen juoma-arvosteluja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään juoma-arvosteluja.

* Käyttäjä näkee sovellukseen lisätyt juomat. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät juoma-arvostelut.

* Käyttäjä pystyy etsimään kellotuksia hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä tietokohteita.

* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja (arvostelujen määrä ja jotain muuta hauskaa nippelitietoa)

* Käyttäjä pystyy valitsemaan juoma-arvostelulle yhden tai useamman luokittelun. (juoman tyyppi, juoman alkoholipitoisuus, arvosana)

* Käyttäjät pystyvät vertailemaan arvosteluja toisten käyttäjien arvosteluihin taulukon (esim. annettujen arvosanojen perusteella.)

* Käyttäjä pystyy lisämään kuvan juomasta

* Käyttäjä voi saada erilaisia saavutuksia ja "arvonimiä", joita voi esitellä profiilissa

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

## Miksi?
Pidän asioiden varsinkin juomien arvostelusta
  
