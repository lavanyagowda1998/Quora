from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User

# Create your views here.
def HomePage(request):
    pass

def SignUpPage(request):
    if request.method == 'POST':
        username =  request.POST.get('username')
        email = request.POST.get('email')
        pass_word = request.POST.get('password1')
        confirm_pass_word =  request.POST.get('password2')
        if pass_word != confirm_pass_word:
            return HttpResponse('Your password doesnot match with confirm password ')
        
        else:
            my_user = User.objects.create_user(username,email,pass_word)
            my_user.save()
            return redirect('login')


    return render(request , 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('username')


    return render(request , 'login.html')    

