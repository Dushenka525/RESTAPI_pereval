from rest_framework import serializers
from .models import Tourist, Coords, Image, PerevalAdded, PerevalImage
from django.utils import timezone


class TouristSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tourist
        fields = ['email', 'phone', 'fam', 'name', 'otc']
        # email будем использовать как уникальный идентификатор

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']

class ImageSerializer(serializers.ModelSerializer):
    # Поле image будет обрабатывать загрузку файла (если нужно)
    # Для простоты предположим, что изображения уже загружены и мы получаем только их id
    class Meta:
        model = Image
        fields = ['id', 'title', 'image']
        read_only_fields = ['id', 'date_added']  # дату добавляет сервер автоматически


class PerevalAddedSerializer(serializers.ModelSerializer):
    # user = TouristSerializer()
    user = serializers.DictField(write_only=True)  # теперь просто словарь

    coords = CoordsSerializer()
    images = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Image.objects.all(),
        write_only=True  # в ответе не выводим, или можно добавить в read_only
    )

    class Meta:
        model = PerevalAdded
        fields = [
            'id',
            'beautyTitle',
            'title',
            'other_titles', 
            'connect',
            'add_time',
            'user',
            'coords',
            'winter_level',
            'summer_level',
            'autumn_level',
            'spring_level',
            'status',
            'images',
        ]
        read_only_fields = ['id', 'status', 'add_time']  # статус и дату ставим автоматически

    def create(self, validated_data):
        # Извлекаем вложенные данные
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_ids = validated_data.pop('images')  # список id изображений

        # Получаем или создаём пользователя по email
        user, created = Tourist.objects.get_or_create(
            email=user_data['email'],
            defaults=user_data
        )
        # Если пользователь уже существовал, но данные изменились? 
        # Можно обновить, если нужно, но пока оставим как есть.

        # Создаём координаты
        coords = Coords.objects.create(**coords_data)
        validated_data['add_time'] = timezone.now()

        # Создаём перевал
        pereval = PerevalAdded.objects.create(
            user=user,
            coords=coords,
            **validated_data
        )

        # Связываем изображения через промежуточную модель
        # for img_id in images_ids:
        #     PerevalImage.objects.create(pereval=pereval, image_id=img_id)
        for img in images_ids:
            PerevalImage.objects.create(pereval=pereval, image=img)
        return pereval