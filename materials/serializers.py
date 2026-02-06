from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import Payment
from .models import Course, Lesson, Subscription
from materials.validators import valid_yt


class CourseSerializer(serializers.ModelSerializer):

    video_url = serializers.CharField(validators=[valid_yt])
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    video_url = serializers.CharField(validators=[valid_yt])

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