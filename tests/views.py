from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, UserResult, Question
from .forms import TestForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def test_list(request):
    tests = Test.objects.all()
    return render(request, "test_list.html", {"tests": tests})

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()

    # Инициализация переменной selected_answers
    selected_answers = []

    if request.method == "POST":
        selected_answers = request.POST.getlist("selected_answer")  # Получаем выбранные ответы
        correct_count = 0
        total_questions = questions.count()

        for question in questions:
            # Получаем правильные ответы для текущего вопроса
            correct_answers = question.answers.filter(is_correct=True)
            correct_ids = [str(answer.id) for answer in correct_answers]  # Преобразуем ID в строки

            # Проверяем, совпадает ли выбранный ответ с правильным
            if any(answer_id in selected_answers for answer_id in correct_ids):
                correct_count += 1

        score = correct_count
        percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        # Сохраняем результат пользователя  
        UserResult.objects.update_or_create(
            user=request.user,
            test=test,
            defaults={"score": score, "some_field": f"{correct_count}/{total_questions}"}
        )

        return render(request, "test_result.html", {
            "test": test,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "percentage": round(percentage, 2),
        })

    # Возвращаем страницу теста для GET-запроса
    return render(request, "test_detail.html", {
        "test": test,
        "questions": questions,
    })


def test_result(request, username):
    test_id = request.GET.get("test_id")
    test = get_object_or_404(Test, id=test_id)
    result = UserResult.objects.filter(test=test, user__username=username).first()

    if not result:
        return render(request, "test_result.html", {"test": test, "error": "Результаты не найдены."})

    percentage = (result.score / test.questions.count()) * 100 if test.questions.exists() else 0

    return render(request, "test_result.html", {
        "test": test,
        "result": result,
        "percentage": round(percentage, 2),
    })

def save_test_result(user, test, score):
    UserResult.objects.update_or_create(
        user=user,
        test=test,
        defaults={"score": score},
    )


def process_test_result(request):
    username = request.POST.get("username")
    test_id = request.POST.get("test_id")
    score = request.POST.get("score")

    test = get_object_or_404(Test, id=test_id)
    save_test_result(user=username, test=test, score=score)

    return render(request, "success.html", {"message": "Результат успешно сохранен!"})

class UserRegisterView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_register.html')

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_login')

        return render(request, 'user_register.html', {'errors': serializer.errors})

class UserLoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_login.html')

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('test_list')
            return render(request, 'user_login.html', {'error': 'Неверные учетные данные'})

        return render(request, 'user_login.html', {'errors': serializer.errors})
    