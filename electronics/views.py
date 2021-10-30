from django.shortcuts import render, get_object_or_404, redirect
from .models import  Payment
from django.conf import settings
from .forms import PaymentForm
from django.conf import settings


def initiate_payment(request):
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'make_payment.html', {'payment': payment,
                                                  'public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form = PaymentForm()
    return render(request, 'initiate_payment.html', {'payment_form': payment_form})


def verify_payment(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    verified = payment.verify_payment()
    return redirect('initiate-payment')
