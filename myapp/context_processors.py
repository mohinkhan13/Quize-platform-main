# your_app/context_processors.py

from .models import CustomUser, Exam

def custom_context(request):
    context = {}
    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = CustomUser.objects.get(id=user_id)
            context['user'] = user
            context['exams_count'] = Exam.objects.filter(user=user).count()
        except CustomUser.DoesNotExist:
            pass

    # Add other context variables as needed
    # context['site_name'] = "Your Site Name"
    # Add more variables here

    return context
