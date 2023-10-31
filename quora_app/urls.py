from django.urls import path
from . import views  # Import your app's views

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('question_and_answer/', views.QuestionAndAnswerPage, name='question_and_answer'),
    path('login/', views.LoginPage, name='login'),
    path('signup/', views.SignUpPage, name='signup'),
    path('logout/', views.LogoutPage, name='logout'),
    path('post_question/', views.post_question, name='post_question'),
    path('post_answer/<int:question_id>/', views.post_answer, name='post_answer'),
    path('like_answer/<int:answer_id>/', views.like_answer, name='like_answer'),
    # Define other app-level URL patterns if needed
]
