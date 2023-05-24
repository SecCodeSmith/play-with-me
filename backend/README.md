# Play with me

## Trello 
https://trello.com/invite/b/jNGcHCua/ATTI896a98d50ab8278855fee3de7f11177bD2253329/projekt-informacyjny-1

## Zaproszenie na dsc

https://discord.gg/fUWj3AujwB

## Uruchomienie projektu

1. Instalacja python w wersji 3.1+
2. Instalacja django `py -m pip install django`
3. Uruchomienie bazy danych w docker
linux:
```bash
docker volume create play_with_me
docker run -d \
	--name play_with_me_db \
	-e POSTGRES_PASSWORD='!Q2w3e4r' \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-e POSTGRES_USER='play-with-me' \
	-e POSTGRES_DB='play-with-me' \
	-p 5432:5432 \
	-v play_with_me:/var/lib/postgresql/data \
	postgres
```
windows:
```shell
docker volume create play_with_me
docker run -d --name play_with_me_db -e POSTGRES_PASSWORD='!Q2w3e4r' -e PGDATA=/var/lib/postgresql/data/pgdata -e POSTGRES_USER='play-with-me' -e POSTGRES_DB='play-with-me' -p 5432:5432 -v play_with_me:/var/lib/postgresql/data postgres
docker exec -it psql play_with_me_db < play_with_me_db_24_05_2023.sql
```
4. Uruchomienie aplikacji `py menage.py runserver`

## Foldery

- singlepage - folder zawierający obsługę wyświetlania informacji oraz działań nie wymagających logowania
- static/css - folder zawierający pliki css (formatowanie strony dla niewtajemniczonych) -- Dla apki testowej (bez znaczenia dla projektu)
- static/img - folder zawierający pliki zdjęć np favicon, ikona itd. -- Dla apki testowej (bez znaczenia dla projektu)
- static/js - folder zawierający pliki skrypty javaScript używane globalnie.-- Dla apki testowej (bez znaczenia dla projektu)
- template - miejsce na pliki html strony -- Dla apki testowej (bez znaczenia dla projektu)
- api - folder zawierający bardziej skomplikowane usługi tzn. wymagających używietelnienia