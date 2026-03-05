from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PerevalAddedSerializer, ImageSerializer, PerevalAddedDetailSerializer, PerevalAddedUpdateSerializer, PerevalAdded
from .models import Tourist


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

# @api_view([ 'POST'])
# def submit_data(request):
#     serializer = PerevalAddedSerializer(data=request.data)
#     if serializer.is_valid():
#         pereval = serializer.save()
#         return Response({
#             'status': 200,
#             'message': 'Отправлено успешно',
#             'id': pereval.id
#         })
#     print(serializer.errors)  # добавить эту строку

#     return Response({
#         'status': 400,
#         'message': 'Ошибка валидации',
#         'errors': serializer.errors
#     }, status=400)


@api_view(['GET', 'POST'])
def submit_data(request):
    """
    Обрабатывает GET (список перевалов пользователя по email) и POST (создание нового перевала)
    """
    if request.method == 'GET':
        # Получение списка перевалов по email пользователя
        email = request.query_params.get('user__email')
        if not email:
            return Response(
                {'state': 0, 'message': 'Не указан параметр user__email'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = Tourist.objects.get(email=email)
        except Tourist.DoesNotExist:
            # Если пользователь не найден, возвращаем пустой список
            return Response([])

        perevals = PerevalAdded.objects.filter(user=user).order_by('-add_time')
        serializer = PerevalAddedDetailSerializer(perevals, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Создание нового перевала (существующий код)
        serializer = PerevalAddedSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pereval = serializer.save()
            return Response({
                'status': 200,
                'message': 'Отправлено успешно',
                'id': pereval.id
            })
        return Response({
            'status': 400,
            'message': 'Ошибка валидации',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PATCH'])
def pereval_detail(request, pk):
    """
    GET: получение информации о конкретном перевале
    PATCH: редактирование перевала, если он в статусе 'new'
    """
    try:
        pereval = PerevalAdded.objects.get(pk=pk)
    except PerevalAdded.DoesNotExist:
        return Response(
            {'state': 0, 'message': 'Объект не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = PerevalAddedDetailSerializer(pereval)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        # Проверяем статус
        if pereval.status != 'new':
            return Response(
                {'state': 0, 'message': 'Редактирование запрещено, статус не "new"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PerevalAddedUpdateSerializer(
            pereval,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'state': 1, 'message': 'Запись успешно обновлена'})
        return Response(
            {'state': 0, 'message': 'Ошибка валидации', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )