# core/emails.py
from django.core.mail import send_mail

def send_order_email(to_email, order_id, total):
    subject = f"Order #{order_id} confirmed"
    body = f"Thank you! Your order #{order_id} is confirmed.\nTotal: {total}"
    send_mail(subject, body, "no-reply@groceryshop.local", [to_email], fail_silently=True)
