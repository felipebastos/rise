import os
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.core.mail import send_mail

from djoser.signals import user_activated


@receiver(user_activated)
def handle_user_activated(sender, user, request, **kwargs):
    usuarios_comuns = Group.objects.get(name="common_users")

    user.groups.add(usuarios_comuns)

    send_mail(
        "Um usuário foi ativado",
        f"O usuário {user.username} foi ativado com sucesso e adicionado ao grupo de usuários comuns",
        from_email=os.getenv("DEFAULT_FROM_EMAIL"),
        recipient_list=[os.getenv("ADMIN_MAIL")],
        fail_silently=True,
    )
