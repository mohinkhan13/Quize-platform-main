from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Exam)
admin.site.register(MCQQuestion)
admin.site.register(ShortAnswerQuestion)
admin.site.register(TrueFalseQuestion)
admin.site.register(Enrollment)
admin.site.register(ExamResult)

