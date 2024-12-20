from flask import Blueprint, render_template, request, jsonify
from .models import CryptoEntries, CryptoCoin, CurrentStatus
from .services import get_conversion_from_api, update_current_status, write_entry, calculate_inversion

bp = Blueprint('main', __name__)

@bp.route('/')
def movements():
    """Funcion para devolver el html con los movimientos que se hayan hecho hasta la fecha actual

    Returns:
        template: template de movements
    """
    crypto_entries = CryptoEntries.query.all()
    return render_template('movements.html', crypto_entries=crypto_entries)

@bp.route('/purchase', methods=['GET', 'POST'])
def purchase():
    """Funcion para comprar, intercambiar o vender cryptos, tendra diferentes funcionalidades segun sea:
    - GET: Mostrar el formulario para comprar, intercambiar o vender
    - POST: Realizar la compra, intercambio o venta

    Returns:
        template: template de purchase
    """
    available_coins = CryptoCoin.query.all()
    current_status_entries = CurrentStatus.query.all()
    current_status = current_status_entries[0].to_dict()
    if request.method == 'GET':
        return render_template('purchase.html', available_coins=available_coins, current_status = current_status)
    
    elif request.method == 'POST':
        form_values = dict(request.form)
        rate = get_conversion_from_api(request.form.get("from_crypto"),request.form.get("to_crypto"))
        if rate:
            real_quantity = rate * float(request.form.get("quantity"))
            return render_template('purchase.html', available_coins=available_coins, rate=rate, real_quantity=real_quantity, form_previous_values = form_values, current_status = current_status)
        else:
            return render_template('purchase.html', available_coins=available_coins, form_previous_values = form_values, current_status = current_status)

@bp.route("/api/validate_purchase", methods =['POST'])
def validate_purchase():
    """API para realizar la validacion de la compra

    Returns:
        json: json indicando que se ha hecho la validacion correctamente
    """

    data = request.json
    amount = float(data.get("amount"))
    rate = float(data.get("rate"))
    from_crypto = data.get("from_crypto").lower()
    to_crypto = data.get("to_crypto").lower()

    update_current_status(from_crypto,to_crypto,amount,rate)
    write_entry(from_crypto, to_crypto, amount, rate)
    return jsonify({"message": "ok"})

@bp.route("/status", methods =['GET'])
def status():
    inverted, current_value = calculate_inversion()
    return render_template("status.html", inverted=inverted, current_value=current_value)