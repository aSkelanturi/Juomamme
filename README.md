# Juomamme
Tietokannat ja web-ohjelmointi kurssin harjoitustyö

## Sovelluksen toiminnot

* Käyttäjä pystyy poistamaan lisäämiään juoma-arvosteluja.

* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja (arvostelujen määrä ja jotain muuta hauskaa nippelitietoa)

* Käyttäjät pystyvät vertailemaan arvosteluja toisten käyttäjien arvosteluihin taulukon (esim. annettujen arvosanojen perusteella.)

* Käyttäjä pystyy lisämään kuvan juomasta

* Käyttäjä voi saada erilaisia saavutuksia ja "arvonimiä", joita voi esitellä profiilissa

## Sovelluksessa toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

* Käyttäjä pystyy lisäämään sovellukseen juoma-arvosteluja. Lisäksi käyttäjä pystyy muokkaamaan lisäämiään juoma-arvosteluja.

* Käyttäjä näkee sovellukseen lisätyt juomat. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät juoma-arvostelut.

* Käyttäjä pystyy etsimään Arvosteluita hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä tietokohteita.

* Käyttäjä pystyy valitsemaan juoma-arvostelulle yhden tai useamman luokittelun. (juoman nimi, arvosana, arvostelu)

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
  
