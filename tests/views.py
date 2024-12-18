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

@login_required
def test_detail(request, pk):
    user = request.user
    test = get_object_or_404(Test, id=pk)
    
    try:
        result, created = UserResult.objects.get_or_create(user=user, test=test, defaults={'some_field': 'new_value'})
        questions = test.questions.all()
        
        if not questions.exists():
            return render(request, "error.html", {"error": "Тест не содержит вопросов."})

        if request.method == "POST":
            selected_answers = request.POST.getlist("selected_answer")
            correct_count = 0 
            total_questions = questions.count()

            for question, selected_answer in zip(questions, selected_answers):
                if question.correct_answer == selected_answer:
                    correct_count += 1

            score = f"{correct_count}/{total_questions}"
            result.some_field = score
            result.save()

            return render(request, "test_result.html", {
                "test": test,
                "correct_count": correct_count,
                "total_questions": total_questions
            })

        return render(request, "test_detail.html", {"test": test, "questions": questions, "result": result})

    except IntegrityError:
        return render(request, "error.html", {"error": "Ошибка при обработке данных."})

def test_result(request, username):
    test_id = request.GET.get("test_id")
    test = get_object_or_404(Test, id=test_id)

    results = UserResult.objects.filter(test=test, user__username=username)

    if not results.exists():
        return render(request, "test_result.html", {"test": test, "error": "Результаты не найдены."})

    result = results.first()

    return render(request, "test_result.html", {"test": test, "result": result})

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
    