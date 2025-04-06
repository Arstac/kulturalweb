{% extends 'base.html' %}
{% block content %}

<div class="container mt-5 text-center">
    <h1 class="mb-4">¡Pago completado con éxito! 🎉</h1>
    <div class="alert alert-success" role="alert">
        <h4 class="alert-heading">Gracias por tu compra</h4>
        <p>Tu pedido ha sido procesado correctamente. En breve recibirás un email de confirmación.</p>
        <hr>
        <p class="mb-0">Número de transacción: <strong>{{ order.paypal_transaction_id }}</strong></p>
    </div>
    <a href="{% url 'tienda:tienda' %}" class="btn btn-primary">Volver a la tienda</a>
</div>

{% endblock %}