from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseCountSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.course.count()

    class Meta:
        model = Course
        fields = ('name', 'description',)