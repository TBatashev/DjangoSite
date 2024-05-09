from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    В общем, вышеприведенный код делает то, что после того, как метод модели пользователя save() завершил выполнение, 
    он отправляет сигнал post_save в функцию-приемник create_user_profile, затем эта функция получит сигнал для создания 
    и сохранения экземпляра профиля для этого пользователя.
    """
    if created :
        Profile.objects.create(user=instance)