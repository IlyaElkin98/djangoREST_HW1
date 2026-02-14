import stripe
from django.core.mail import send_mail
from django.http import JsonResponse

from config.settings import STRIPE_API_KEY, EMAIL_HOST_USER

stripe.api_key = STRIPE_API_KEY

def create_price(amount):
    """Создание цены для объекта"""
    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "tuition fees"},
    )
    return price


def create_session(price):
    """Создание сессии оплаты"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def test_session(request, session_id):
    """Просмотр сессии оплаты через идентификатор сессии"""
    session = stripe.checkout.Session.retrieve(session_id)
    return JsonResponse({"session": session})


def send_mailing(address, subject, body):
    """Функция отправки письма"""

    response = send_mail(
        subject=subject,
        message=body,
        from_email=EMAIL_HOST_USER,
        recipient_list=address,
        fail_silently=False,
    )
    return response