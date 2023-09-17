import os
from django.conf import settings
from django.http import JsonResponse
from .models import Pass, Photo
from .serializers import PassSerializer, PhotoSerializer
from django.db import transaction
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .models import SubmitData
from .serializers import SubmitDataSerializer

class PassListCreateView(APIView):
    def post(self, request):
        db_host = os.environ.get('FSTR_DB_HOST', 'localhost')
        db_port = os.environ.get('FSTR_DB_PORT', '5432')
        db_login = os.environ.get('FSTR_DB_LOGIN', 'myuser')
        db_password = os.environ.get('FSTR_DB_PASS', 'mypassword')

        data = request.data

        pass_obj = Pass.objects.create(name=data.get('name'), elevation=data.get('elevation'), status='new')

        with transaction.atomic():
            pass_obj.save()

        return JsonResponse({'message': 'Data submitted successfully'})

    def post(self, request):
        data = request.data

        pass_serializer = PassSerializer(data=data)
        if pass_serializer.is_valid():
            pass_obj = pass_serializer.save(status='new')
        else:
            return JsonResponse({'error': 'Invalid pass data'})

        photos_data = data.get('photos', [])
        for photo_data in photos_data:
            photo_data['pass'] = pass_obj.id
            photo_serializer = PhotoSerializer(data=photo_data)
            if photo_serializer.is_valid():
                photo_serializer.save()
            else:
                return JsonResponse({'error': 'Invalid photo data'})

        user_data = data.get('user', {})
        pass_obj.user_name = user_data.get('name')
        pass_obj.user_email = user_data.get('email')
        pass_obj.user_phone = user_data.get('phone')
        pass_obj.save()

        return JsonResponse({'message': 'Data submitted successfully'})

# Получение одной записи по ее id
def get_submit_data(request, id):
    try:
        submit_data = SubmitData.objects.get(id=id)
        serializer = SubmitDataSerializer(submit_data)
        return JsonResponse(serializer.data, status=200)
    except SubmitData.DoesNotExist:
        return JsonResponse({"message": "Запись не найдена"}, status=404)


# Редактирование существующей записи
@csrf_exempt
def edit_submit_data(request, id):
    try:
        submit_data = SubmitData.objects.get(id=id)

        # Проверка статуса модерации
        if submit_data.status != 'new':
            return JsonResponse({"message": "Запись не может быть отредактирована, так как она не в статусе 'new'"},
                                status=400)

        # Ограничение на редактирование полей
        restricted_fields = ['full_name', 'email', 'phone_number']
        for field in restricted_fields:
            if field in request.data:
                return JsonResponse({"message": f"Поле '{field}' не может быть отредактировано"}, status=400)

        serializer = SubmitDataSerializer(submit_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"state": 1}, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    except SubmitData.DoesNotExist:
        return JsonResponse({"message": "Запись не найдена"}, status=404)


# Получение списка данных по email пользователя
def get_submit_data_by_email(request):
    email = request.GET.get('user__email', None)
    if email:
        submit_data = SubmitData.objects.filter(user__email=email)
        serializer = SubmitDataSerializer(submit_data, many=True)
        return JsonResponse(serializer.data, status=200)
    else:
        return JsonResponse({"message": "Параметр 'user__email' не указан"}, status=400)

