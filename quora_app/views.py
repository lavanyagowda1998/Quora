from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from .models import Question
from .forms import QuestionForm



@login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')

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
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")
        
    return render(request , 'login.html')   



def view_questions(request):
    questions = Question.objects.all()
    return render(request, 'qa/view_questions.html', {'questions': questions})

def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_questions')
    else:
        form = QuestionForm()
    return render(request, 'qa/post_question.html', {'form': form})

def LogoutPage(request):
    logout(request)
    return redirect('login')

