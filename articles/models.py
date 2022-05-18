from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Article(models.Model):
    REGION_CHOICES = [
      ('seoul','서울특별시'),
      ('gyeonggi', '경기도'),
      ('gangwon', '강원도'),
      ('chungcheong', '충청도'),
      ('jeolla', '전라도'),
      ('jeju','제주도'),
    ]

    region = models.CharField(max_length=11, choices=REGION_CHOICES)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    member = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='members')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    applicants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='applicants')            # 지원자 관련 테이블

    member_limit = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(20)], help_text='최대 20명까지 가능합니다.') # 최대 인원 수 조정 필요
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)

    location = models.TextField() # API활용? 적절한 방식 찾기
    meeting_date = models.DateField()
    meeting_time = models.TimeField() 
    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Photo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(null=True, blank=True)