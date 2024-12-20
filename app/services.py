from flask import current_app as app
from .models import CurrentStatus, db, CryptoEntries
from datetime import datetime
import requests
from sqlalchemy import func

def get_conversion_from_api(from_crypto:str, to_crypto:str):
    """Llamada a la api con la API KEY de config

    Args:
        from_crypto (str): Moneda de la cual partimos
        to_crypto (str): Moneda a la que queremos hacer el intercambio

    Returns:
        rate (float): Devuelve el ratio de moneda si se ha podido llamar a la API y todo ha salido bien
    """

    key = app.config["API_KEY_COIN"]
    url = f"https://rest.coinapi.io/v1/exchangerate/{from_crypto}/{to_crypto}?apikey={key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["rate"]
    return None

def update_current_status(from_crypto:str,to_crypto:str, amount:float, rate:float):
    """Actualizar el estado actual de tus inversiones en la base de datos

    Args:
        from_crypto (str): Moneda de la cual partimos
        to_crypto (str): Moneda a la que se ha hecho el cambio
        amount (float): Cantidad de from_crypto que se quiere cambiar
        rate (float): ratio entre monedas from y to
    """
    current_status = CurrentStatus.query.get(1)
    if from_crypto != "eur":
        from_crypto_value = getattr(current_status,from_crypto)
        setattr(current_status,from_crypto,from_crypto_value-amount)

    if to_crypto != "eur":
        to_crypto_value = getattr(current_status,to_crypto)
        setattr(current_status,to_crypto,to_crypto_value+amount*rate)

    db.session.commit()
    return

def write_entry(from_crypto:str, to_crypto:str, amount:float, rate:float):
    """Guardar el cambio de moneda en base de datos

    Args:
        from_crypto (str): Moneda de la cual partimos
        to_crypto (str): Moneda a la que se ha hecho el cambio
        amount (float): Cantidad de from_crypto que se quiere cambiar
        rate (float): ratio entre monedas from y to
    """

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S") + f".{now.microsecond // 1000:03d}"
    new_entry = CryptoEntries(date=date,
                              time=time_now,
                              from_currency=from_crypto.upper(),
                              from_quantity=amount,
                              to_currency=to_crypto.upper(),
                              to_quantity=amount*rate)
    db.session.add(new_entry)
    db.session.commit()
    return

def calculate_inversion():
    """Calcular la inversion actual que se tiene segun el documento facilitado

    Returns:
        eur_inverted (float): euros totales invertidos (suma de todas las monedas from que sean eur)
        current_value (float): valor actual de nuestras inversiones
    """
    current_status = CurrentStatus.query.get(1).to_dict()

    # get eur inverted or 0 if None
    eur_inverted = db.session.query(func.sum(CryptoEntries.from_quantity)).filter(CryptoEntries.from_currency == "EUR").scalar()
    eur_inverted = eur_inverted if eur_inverted is not None else 0.0

    # get eur returned or 0 if None
    eur_returned = db.session.query(func.sum(CryptoEntries.to_quantity)).filter(CryptoEntries.to_currency == "EUR").scalar()
    eur_returned = eur_returned if eur_returned is not None else 0.0

    eur_balance = eur_returned - eur_inverted
    
    inverted_crypto = 0
    for key,value in current_status.items():
        if value > 0:
            rate = get_conversion_from_api(key.upper(),"EUR")
            inverted_crypto += value * rate
    
    current_value = eur_inverted + eur_balance + inverted_crypto

    return eur_inverted, current_value
    
