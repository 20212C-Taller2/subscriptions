# subscriptions

## Environment
Requiere las siguientes variables de entorno: 
```shell
export FASTAPI_POSTGRESQL=postgresql+psycopg2://user:pass@databaseurl/db
```

## Install
Necesita Python +3.7 instalado (testeado con 3.8.11 en mi maquina) para correr con `pip`. 

Ejecutar:
```shell
pip install -r requirements.txt
pre-commit install
alembic upgrade head
```

## DB migrations
Antes de iniciar el server de desarrollorealizar las migraciones pendientes con `alembic upgrade head`.

Si se quiere crear una nueva revision usar `alembic revision --autogenerate -m "some message"`. Luego validar que el 
archivo generado satisfaga correctamente los cambios realizados

## Ejecucion
Iniciar el server con:
```shell
vunicorn app.main:app

## Tip: Si se esta desarrollando utilizar para auto reload del server ante cambios
vunicorn app.main:app --reload
```

