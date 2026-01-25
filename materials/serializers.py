from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import Payment
from .models import Course, Lesson



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('course', 'title', 'description', 'preview_image', 'video_url',)


class CourseCountSerializer(serializers.ModelSerializer):
    # Сериализатор выводящий количество уроков.
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count']

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'