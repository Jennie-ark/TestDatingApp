from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password):
        if email is None:
            raise TypeError('Введите email адрес')
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Введите пароль')
        user = self.create_user(email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class GenderChoices(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'

    avatar = models.ImageField(upload_to='media/')
    gender = models.CharField(max_length=6, choices=GenderChoices.choices)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    lat = models.FloatField(default=59.7914)
    lon = models.FloatField(default=30.1650)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Match(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='liked_to')
    user_like = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  related_name='was_liked')

    class Meta:
        verbose_name = "Совпадение"
        verbose_name_plural = "Совпадения"

        constraints = [models.UniqueConstraint(fields=['user', 'user_like'],
                                               name='unique_match')]
