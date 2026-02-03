from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=200)
    preview_image = models.ImageField(upload_to='materials/preview', null=True, blank=True)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name='course', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='materials/preview', null=True, blank=True)
    video_url = models.URLField()
    owner = models.ForeignKey(User, related_name='lesson', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title