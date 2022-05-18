from rest_framework import serializers
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(source='member.count', read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'user', 'member_count', 'title', 'content', 'member_limit', 'region', 'location', 'thumbnail', 'meeting_date', 'meeting_time')

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('meeting_date',)