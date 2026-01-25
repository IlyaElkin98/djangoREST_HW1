from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    preview_image = models.ImageField(upload_to='materials/preview', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='materials/preview', null=True, blank=True)
    video_url = models.URLField()

    def __str__(self):
        return self.title