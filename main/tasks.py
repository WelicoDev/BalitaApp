from celery import shared_task
import requests
from decouple import config
from main.models import Contact

@shared_task
def send_contact_message(contact_id):
    contact = Contact.objects.get(id=contact_id)

    message = (f"Project : Balita.uz\nID : {contact.id}\nUser : {contact.name}\nEmail : {contact.email}\nPhone : "
               f"{contact.phone}\nMessage : {contact.message}\nTime : {contact.created_at.date()}  // "
               f"{contact.created_at.hour}:{contact.created_at.minute}:{contact.created_at.second}")

    BOT_TOKEN = config("BOT_TOKEN")
    CHAT_ID = config("CHAT_ID")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"

    response = requests.get(url)
    return response.text
