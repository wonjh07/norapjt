from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import date
from .models import Article, Comment, Photo
from .forms import ArticleForm, CommentForm
from .serializers import ArticleListSerializer, CalendarSerializer


# Create your views here.
@require_safe
def index(request):
    if request.user.is_authenticated:
        return render(request, 'articles/index.html')
    return redirect('accounts:login')


# get 요청을 두 번 보낼 경우
# 내 일정
@api_view(['GET'])
def ajax_mine(request):
    ttoday = request.GET.get('ttoday')
    articles = Article.objects.filter(meeting_date=ttoday, member=request.user)
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)


# 전체 일정
@api_view(['GET'])
def ajax_total(request):
    ttoday = request.GET.get('ttoday')
    articles = Article.objects.filter(meeting_date=ttoday).exclude(member=request.user) # 조금 더 깔끔하게 바꿈
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ajax_calendar(request):
    month = request.GET.get('month')
    articles = Article.objects.filter(member=request.user, meeting_date__startswith=month)
    myplan = {}
    for i in range(1, 32):
        myplan[i] = 0
    serializer = CalendarSerializer(articles, many=True)
    for article in serializer.data:
        myplan[article['meeting_date'][8:]] = 1
    return Response(myplan)


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            photos = request.FILES.getlist('photos')
            user = request.user
            if form.is_valid():
                article = form.save(commit=False)
                article.thumbnail = form.cleaned_data['thumbnail']
                article.user = user
                article.save()
                article.member.add(user)
                for photo in photos:
                    Photo.objects.create(article=article, photo=photo)
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(initial={'meeting_date':date.today,})
        context = {
            'form': form,
        }
        return render(request, 'articles/create.html', context)
    return redirect('accounts:login')


@require_safe
def detail(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        photos = article.photos.all()
        comment_form = CommentForm()
        comments = article.comments.all()

        # 참가 여부 버튼
        isApplicant = False
        if article.applicants.filter(pk=request.user.pk).exists():
            isApplicant = True

        isMember = False
        if article.member.filter(pk=request.user.pk).exists():
            isMember = True

        isFullMember = False
        if article.member_limit == article.member.count():
            isFullMember = True
        member_count = article.member.count()
        print('isApplicant',isApplicant, 'isMember',isMember,'isFullMember',isFullMember)
        context = {
            'article': article,
            'comment_form': comment_form,
            'comments': comments,
            'photos':photos,
            'isApplicant': isApplicant,
            'isMember': isMember,
            'isFullMember':isFullMember,
            'member_count':member_count,
        }
        return render(request, 'articles/detail.html', context)
    return redirect('accounts:login')


@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        if request.user == article.user:
            article.delete()
            return redirect('articles:index') 
        return redirect('articles:detail', article.pk)
    return redirect('accounts:login')


@require_http_methods(['GET', 'POST'])
def update(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        if request.user == article.user:
            if request.method == 'POST':
                form = ArticleForm(request.POST, request.FILES, instance=article)
                photolist = request.FILES.getlist('photos')
                if form.is_valid():
                    form.save()
                    rm_photos = article.photos.all()
                    for rm_photo in rm_photos:
                        rm_photo.delete()
                    for photo in photolist:
                        Photo.objects.create(article=article, photo=photo)
                    return redirect('articles:detail', article.pk)
            else:
                form = ArticleForm(instance=article)
        else:
            return redirect('articles:detail', article.pk)
        context = {
            'article': article,
            'form': form,
        }
        return render(request, 'articles/update.html', context)
    return redirect('accounts:login')


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
        return redirect('articles:detail', article.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
        return redirect('articles:detail', article_pk)
    return redirect('accounts:login')


@api_view(['POST'])
def likes(request, pk):
    article = get_object_or_404(Article,pk=pk)
    user = request.user

    response = {
        'liked':False,
        'count':0,
    }

    if article.like_users.filter(pk=user.pk).exists():
        article.like_users.remove(user)
    else:
        article.like_users.add(user)
        response['liked'] = True
    response['count'] = article.like_users.count()

    return JsonResponse(response)


# 디테일 => 멤버 관리 페이지 렌더링
@require_safe
def member(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        members = article.member.all()
        applicants = article.applicants.all()
        member_count = article.member.count()
        context = {
            'article': article,
            'members': members,
            'applicants': applicants,
            'member_count': member_count,
        }
        return render(request, 'articles/member.html', context)
    return redirect('accounts:login')



# 신청 버튼 클릭 시 신청 테이블에 신청자와 게시글 저장 후 상태 반환(신청버튼 => 수락대기)
@api_view(['PATCH'])
def apply(request, pk):
    user = request.user
    article = get_object_or_404(Article, pk=pk)

    response = {
        'state': False,
    }

    # 이미 신청자라면 삭제
    if article.applicants.filter(pk=user.pk).exists():
        article.applicants.remove(user)
    # 아니라면 신청
    else:
        article.applicants.add(user)
        response['state'] = True

    # state에 따라서 버튼 정보 출력
    return JsonResponse(response)


# 수락or거절 버튼 클릭 시
@api_view(['POST'])
def accept(request, article_pk):
    action = request.POST.get('action')
    article = get_object_or_404(Article, pk=article_pk)
    applicant_pk = request.POST.get('applicantId')
    user = get_object_or_404(get_user_model(), pk=applicant_pk)

    if action == 'delete':
        user = get_object_or_404(get_user_model(), pk=applicant_pk)
        article.member.remove(user)
        response = {
            'state': 'delete',
            'memberCount': 0,
        }
        response['memberCount'] = article.member.count()
        return JsonResponse(response)

    else:
        article.applicants.remove(user)
        response = {
            'state': False,
            'memberCount': 0,
            'applicantName': user.nickname
        }

        if action == 'accept':
            article.member.add(user)
            response['state'] = True

        response['memberCount'] = article.member.count()
        return JsonResponse(response)


@require_POST
def delete_member(request,pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        if article.member.filter(pk=request.user.pk).exists():
            article.member.remove(request.user)
        return redirect('articles:detail', article.pk)
    return redirect('accounts:login')