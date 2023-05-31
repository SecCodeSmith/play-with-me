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
python ./manage.py loaddata db.json 
```
windows:
```shell
docker volume create play_with_me
docker run -d --name play_with_me_db -e POSTGRES_PASSWORD='!Q2w3e4r' -e PGDATA=/var/lib/postgresql/data/pgdata -e POSTGRES_USER='play-with-me' -e POSTGRES_DB='play-with-me' -p 5432:5432 -v play_with_me:/var/lib/postgresql/data postgres
py.exe ./manage.py loaddata db.json 
```
4. Uruchomienie aplikacji `py menage.py runserver`

## Foldery
- api - folder zawierający bardziej skomplikowane usługi tzn. wymagających używietelnienia