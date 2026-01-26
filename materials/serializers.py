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
    # Сериализатор курса выводящий количество уроков и информацию о них.
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count', 'lessons']

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'