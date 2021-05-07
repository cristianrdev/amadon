from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    # si no existe la sesion, primera vez ingresando
    if 'quantity_total' not in request.session:
        request.session['quantity_total'] = 0
    if 'price_total' not in request.session:
        request.session['price_total'] = 0
    # solo el valor de esta orden (no acumulada)
    request.session['total_this_order'] = 0


    # obtiene la cantidad y la ID del producto desde el form
    quantity_from_form = int(request.POST["quantity"])
    product_ID_from_form = request.POST["id_product"]
    # obtiene el valor del producto segun la id en la BD
    selected_product = Product.objects.get(id=product_ID_from_form)

    # calcula el total de esta orden
    total_charge = quantity_from_form * float(selected_product.price)

    # total $ acumulado de ordenes pasadas + la actual
    request.session['total_this_order'] = total_charge

    # suma el numero total de ordenes pasadas + actual
    request.session['quantity_total'] = request.session['quantity_total'] + quantity_from_form
    # suma el  total $ de ordenes pasadas + actual
    request.session['price_total'] = round(request.session['price_total'] + total_charge,2)


    print(request.session)

    print("Charging credit card...")
    order = Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)

    return redirect('/refresh_checkout')

def refresh_checkout(request):
    return render(request, "store/checkout.html")