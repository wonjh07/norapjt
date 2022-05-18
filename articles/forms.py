from turtle import width
from django import forms
from .models import Article, Comment
from .widgets import DatePickerInput, TimePickerInput

# 수정 필요


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    REGION_CHOICES = [
        ("", '모임 지역을 선택해주세요.'),
        ('seoul', '서울특별시'),
        ('gyeonggi', '경기도'),
        ('gangwon', '강원도'),
        ('chungcheong', '충청도'),
        ('jeolla', '전라도'),
        ('jeju', '제주도'),
    ]

    region = forms.ChoiceField(
        label="지역",
        choices=REGION_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "form-select"
            }
        )
    )

    location = forms.CharField(
        label="모임 장소",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    member_limit = forms.IntegerField(
        label="인원 제한",
        widget=forms.NumberInput(
            attrs={
                'placeholder': '인원',
                "class": "form-control",
                'min': 1,
                'max': 20,
            }
        )
    )

    title = forms.CharField(
        label="제목",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    meeting_date = forms.DateField(
        label="모임 일자",
        widget=DatePickerInput(
            attrs={
                'class': 'form-control'
            }
        ))
    meeting_time = forms.TimeField(
        label="모임 시간",
        widget=TimePickerInput(
            attrs={
                'class': 'form-control'
            }
        ))

    content = forms.CharField(
        label="상세 일정",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Article
        fields = ('region', 'member_limit', 'meeting_date',
                  'meeting_time', 'location', 'title', 'content', 'thumbnail')


class CommentForm(forms.ModelForm):

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'textarea',
                'placeholder': '댓글을 입력하세요.',
                'rows': 3
            }
        )
    )

    class Meta:
        model = Comment
        fields = ('content',)
