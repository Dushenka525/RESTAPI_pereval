from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PerevalAddedSerializer, ImageSerializer



from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # поддержка загрузки файлов

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()  # сохраняет файл и запись в БД
            # Формируем ответ с ID и ссылкой на изображение
            return Response({
                'id': image.id,
                'title': image.title,
                'url': image.image.url  # требует настройки MEDIA_URL
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def submit_data(request):
    serializer = PerevalAddedSerializer(data=request.data)
    if serializer.is_valid():
        pereval = serializer.save()
        return Response({
            'status': 200,
            'message': 'Отправлено успешно',
            'id': pereval.id
        })
    print(serializer.errors)  # добавить эту строку

    return Response({
        'status': 400,
        'message': 'Ошибка валидации',
        'errors': serializer.errors
    }, status=400)