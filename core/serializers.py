from rest_framework import serializers
from .models import Resume, InterviewResult, Question, Role, Skill


class ResumeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Resume
        fields = ['id', 'username', 'score', 'skills', 'role']


class InterviewResultSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = InterviewResult
        fields = ['id', 'username', 'role', 'question',
                  'answer', 'score', 'feedback', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'role', 'difficulty', 'question', 'answer']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class RoleSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'skills']