from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from django.shortcuts import render, redirect
from .forms import OrderForms
from .models import Order, Payment, OrderProduct, Product
import datetime
import json
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from goldenoud.logger import logger, log_debug
from decimal import Decimal

# Create your views here.

guest_email = ''

stripe.api_key = settings.STRIPE_SECRET_KEY



def payments(request, order_number):
    log_debug("Received payment request")

    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    # Retrieve the order
    try:
        order = get_object_or_404(Order, user=request.user, is_ordered=False, order_number=order_number)
        log_debug(f"Order retrieved: {order.order_number}")
    except Exception as e:
        logger.error("Error retrieving order", exc_info=True)
        return JsonResponse({'error': 'Order not found'}, status=404)

    # Create a Stripe Checkout Session
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': f'Order {order.order_number}',
                    },
                    'unit_amount': int(order.order_total * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            client_reference_id=order.order_number,
            success_url=request.build_absolute_uri(
                reverse('stripe_return')
            ) + '?session_id={CHECKOUT_SESSION_ID}',  # Updated success URL
            cancel_url=request.build_absolute_uri('/checkout'),
        )
        logger.info(f"Stripe Checkout session created: {session.id}")
        log_debug(f"Checkout session details: {session}")
    except Exception as e:
        logger.error("Failed to create Stripe Checkout session", exc_info=True)
        return JsonResponse({'error': 'Failed to create payment session'}, status=500)

    # Save the payment information in the Payment model
    try:
        payment = Payment(
            user=request.user,
            payment_id=session.id,
            payment_method='Stripe',
            amount_paid=order.order_total,
            status='pending'
        )
        payment.save()
        log_debug(f"Payment saved with ID: {payment.payment_id}")
    except Exception as e:
        logger.error("Failed to save payment information", exc_info=True)
        return JsonResponse({'error': 'Failed to save payment information'}, status=500)

    # Link payment to order but mark order as not yet completed
    try:
        order.payment = payment
        order.save()
        log_debug(f"Order {order.order_number} updated with payment ID: {payment.payment_id}")
    except Exception as e:
        logger.error("Failed to link payment to order", exc_info=True)
        return JsonResponse({'error': 'Failed to update order with payment'}, status=500)

    log_debug("Payment process completed successfully")
    return JsonResponse({'sessionId': session.id, 'redirect_url': session.url})

def place_order(request, total=0, quantity=0, weight_total=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = Decimal('0.00')
    tax = Decimal('0.00')

    for cart_item in cart_items:
        total += Decimal(cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        weight_total += Decimal(cart_item.product.weight * cart_item.quantity)  # Calculate total weight

    # Ensure total has two decimal places
    total = round(total, 2)

    # Calculate tax and grand total with two decimal places
    tax = round(Decimal('20') * total / Decimal('100'), 2)
    grand_total = round(total + tax, 2)

    if request.method == 'POST':
        global guest_email
        form = OrderForms(request.POST)
        if form.is_valid():
            # store all data to order
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            guest_email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.post_code = form.cleaned_data['post_code']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.weight_total = weight_total  # Save the total weight
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')

def order_complete(request):
    session_id = request.GET.get('session_id')
    try:
        # Retrieve session and payment intent from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

        # Get the order and update payment status to paid
        order = Order.objects.get(order_number=session.client_reference_id, is_ordered=False)
        payment = Payment.objects.get(payment_id=session.id)
        payment.status = 'Paid'
        payment.save()

        # Mark the order as completed
        order.is_ordered = True
        order.payment = payment
        order.save()

        # Move cart items to order product table and clear the cart
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            order_product = OrderProduct.objects.create(
                order_id=order.id,
                payment=payment,
                user_id=request.user.id,
                product_id=item.product_id,
                quantity=item.quantity,
                product_price=item.product.price,
                ordered=True
            )
            order_product.variations.set(item.variations.all())
            order_product.save()

            # Reduce the stock for the purchased product
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Clear the cart
        cart_items.delete()

        # Retrieve ordered products and calculate subtotals
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        for item in ordered_products:
            item.subtotal = item.product.price * item.quantity

        # Calculate the overall subtotal
        subtotal = sum(item.subtotal for item in ordered_products)

        # Send order confirmation email with subtotal information
        mail_subject = 'Thank you for your order'
        message = render_to_string('orders/order_receive_email.html', {
            'user': request.user,
            'order': order,
            'ordered_products': ordered_products,
            'subtotal': subtotal,
        })
        to_email = order.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        email.send()

        # Render the order complete page
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)

    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')