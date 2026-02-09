from rest_framework import serializers


def valid_yt(value):
    if value.find('youtube.com'):
        raise serializers.ValidationError('Вы не можете использовать ссылки на сторонние ресурсы, кроме youtube.com.')
