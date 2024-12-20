# flask-crypto

## Instalar
Para instalar esta aplicación tendremos que instalar el requirements.txt creando un entorno virtual preferiblemente

```sh
python -m venv flask_env_crypto
python -m pip install -r requirements.txt 
```

## Configuración
Asegurese de que la base de datos ha sido creada en el directorio instance/crypto.db, en caso de no estar creada o querer crear una nueva:

```sh 
flask db init
flask db migrate -m "Init db"
flask db upgrade
```
## Correr la aplicación
Para correr la aplicación, ejecuta el siguiente comando en la terminal:

```sh
flask run
```