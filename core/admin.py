from django.contrib import admin
from .models import Resume, InterviewResult, Question, Role, Skill

admin.site.register(Resume)
admin.site.register(InterviewResult)
admin.site.register(Question)
admin.site.register(Role)
admin.site.register(Skill)