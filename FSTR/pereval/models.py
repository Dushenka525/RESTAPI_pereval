from django.db import models
from django.contrib.postgres.fields import JSONField  # для PostgreSQL, или используйте models.JSONField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Tourist(models.Model):
    # Используем email как уникальный идентификатор (можно оставить и автоинкрементное поле, но тогда email должен быть уникальным)
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    fam = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    otc = models.CharField(max_length=100, verbose_name='Отчество', blank=True)

    def __str__(self):
        return f"{self.fam} {self.name} {self.otc}".strip()

    class Meta:
        verbose_name = 'Турист'
        verbose_name_plural = 'Туристы'


# Модель координат
class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Широта', validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(verbose_name='Долгота', validators=[MinValueValidator(-180), MaxValueValidator(180)])
    height = models.IntegerField(verbose_name='Высота (м)')

    def __str__(self):
        return f"{self.latitude}, {self.longitude} (высота {self.height})"

    class Meta:
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'


# Модель изображения (файл)
class Image(models.Model):
    # Если хранить файлы, нужно настроить MEDIA_ROOT и MEDIA_URL
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    title = models.CharField(max_length=255, verbose_name='Название', blank=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.title or f"Image {self.id}"

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


# Модель перевала
class PerevalAdded(models.Model):
    STATUS_CHOICES = [
        ('new', 'новый'),
        ('pending', 'на модерации'),
        ('accepted', 'принят'),
        ('rejected', 'отклонён'),
    ]

    beautyTitle = models.CharField(max_length=255, verbose_name='Красивое название', blank=True)
    title = models.CharField(max_length=255, verbose_name='Название')
    other_titles = models.CharField(max_length=255, verbose_name='Другие названия', blank=True)
    connect = models.CharField(max_length=255, verbose_name='Связь', blank=True)  # что соединяет

    add_time = models.DateTimeField(verbose_name='Время добавления')

    # Связи
    user = models.ForeignKey(Tourist, on_delete=models.CASCADE, related_name='pereval_added', verbose_name='Пользователь')
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE, verbose_name='Координаты')

    # Уровни сложности для каждого времени года
    winter_level = models.CharField(max_length=10, verbose_name='Уровень сложности (зима)', blank=True)
    summer_level = models.CharField(max_length=10, verbose_name='Уровень сложности (лето)', blank=True)
    autumn_level = models.CharField(max_length=10, verbose_name='Уровень сложности (осень)', blank=True)
    spring_level = models.CharField(max_length=10, verbose_name='Уровень сложности (весна)', blank=True)

    # Статус модерации
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name='Статус')

    # Связь с изображениями (многие-ко-многим через промежуточную модель)
    images = models.ManyToManyField(Image, through='PerevalImage', related_name='pereval_added', verbose_name='Изображения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'


# Промежуточная модель для связи перевала и изображения
class PerevalImage(models.Model):
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE, verbose_name='Перевал')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name='Изображение')
    # Можно добавить порядковый номер, если нужно
    # order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.pereval.title} - {self.image.title}"

    class Meta:
        verbose_name = 'Связь перевала и изображения'
        verbose_name_plural = 'Связи перевалов и изображений'
        # Уникальность пары (pereval, image) – чтобы одно и то же изображение не привязывалось дважды к одному перевалу
        unique_together = ('pereval', 'image')