function check_form() {
    var from_crypto = document.getElementById("from_crypto").value;
    var to_crypto = document.getElementById("to_crypto").value;
    var amount = document.getElementById("amount").value;

    if (from_crypto==to_crypto){
        alert("No puedes comprar la misma moneda");
        return false;
    }
    if (amount==0){
        alert("No puedes comprar 0");
        return false;
    }
    return true;
}

function hide_validate(){
    if(rate){
        document.getElementById("validate_button").style.display = "none";
    }
}
async function validate_crypto_change() {
    var from_crypto = document.getElementById("from_crypto").value.toLowerCase();
    const amount = document.getElementById("amount").value
    
    if(from_crypto!="eur"){
        if (current_status[from_crypto]<amount){
            alert("No tienes suficiente "+from_crypto+" para realizar la transacción");
        }
    }
    const form = document.getElementById('form_crypto');
    const formData = new FormData(form);
    const data = {
        from_crypto: formData.get('from_crypto'),
        to_crypto: formData.get('to_crypto'),
        amount: formData.get('quantity'),
        rate: rate
    };

    try {
        // Hacer la solicitud POST a la API
        const response = await fetch('/api/validate_purchase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        // Manejar la respuesta
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        window.location.href = window.location.pathname;

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').textContent = `Error: ${error.message}`;
    }
};