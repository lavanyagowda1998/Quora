from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def HomePage(request):
    # Display the home page
    return render(request, 'home.html')

def SignUpPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        # Check if the passwords match
        if password != confirm_password:
            return HttpResponse('Your password does not match with the confirm password.')

        try:
            # Attempt to create the user
            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect('login')
        except IntegrityError:
            return HttpResponse('Username already exists. Please choose a different username.')
        
    return render(request, 'signup.html')    

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('question_and_answer')  # Redirect to the "Question and Answer" page
        else:
            return HttpResponse("Username or Password is incorrect!!!")
        
    return render(request, 'login.html')   

@login_required(login_url='login')
def QuestionAndAnswerPage(request):
    # Load questions and answers
    questions = Question.objects.all()
    answers = Answer.objects.all()

    context = {
        'questions': questions,
        'answers': answers,
    }

    return render(request, 'question_and_answer.html', context)

def LogoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question_and_answer')

    form = QuestionForm()
    return render(request, 'post_question.html', {'form': form})


@login_required(login_url='login')
def post_answer(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = Question.objects.get(pk=question_id)
            answer.save()
            return redirect('question_and_answer')

    form = AnswerForm()
    return render(request, 'post_answer.html', {'form': form})



# Create a dictionary to track liked answers
liked_answers = {}

@login_required(login_url='login')
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if answer.id not in liked_answers:
        # If the answer ID is not in the liked_answers dictionary, the user hasn't liked it yet
        liked_answers[answer.id] = True  # Mark the answer as liked
        answer.like_count += 1
        answer.save()
        return redirect('question_and_answer')
    else:
        return HttpResponse("You have already liked this answer.")