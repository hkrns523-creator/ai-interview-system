from django.contrib import admin
from .models import Role, Skill
from .models import (
    Resume,
    InterviewResult,
    Question
)

admin.site.register(Resume)
admin.site.register(InterviewResult)
admin.site.register(Question)
admin.site.register(Role)
admin.site.register(Skill)