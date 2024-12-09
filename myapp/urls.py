from django.urls import path
from .views import *
urlpatterns = [

    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('setting/', setting, name='setting'),
    path('profile/', profile, name='profile'),
    path('change-password/', change_password, name='change-password'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('new-password/', new_password, name='new-password'),
    path('my-all-exams/', my_all_exams, name='my-all-exams'),
    path('create-exam/', create_exam, name='create-exam'),
    path('create-questions/<int:id>/', create_questions, name='create-questions'),
    path('publish-exam/<int:id>/', publish_exam, name='publish-exam'),
    path('private-exam/<int:id>/', private_exam, name='private-exam'),
    path('delete-exam/<int:id>/', delete_exam, name='delete-exam'),
    path('all-exams/', all_exams, name='all-exams'),
    path('view-exam/<int:id>/', view_exam, name='view-exam'),
    path('exam/<int:id>/', enroll_exam, name='enroll-exam'),
    path('quiz/get_question/<int:exam_id>/<int:index>/', get_question, name='get_question'),
    path('quiz/submit/<int:exam_id>/', submit_answers, name='submit_answers'),
    path('quiz/results/<int:result_id>/', results_view, name='results_view'),
    path('enrolled-exams/', enrolled_exams, name='enrolled-exams'),
]