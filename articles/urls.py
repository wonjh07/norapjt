from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),

    path('create/', views.create, name='create'),

    path('<int:pk>/', views.detail, name='detail'),

    path('<int:pk>/update/', views.update, name='update'),

    path('<int:pk>/delete/', views.delete, name='delete'),

    path('<int:pk>/comments/', views.comments_create, name='comments_create'),

    path(
        '<int:article_pk>/comments/<int:comment_pk>/delete/',
        views.comments_delete,
        name='comments_delete',
    ),
    path('<int:pk>/likes/', views.likes, name='likes'),

    # 경로 수정 (내 일정, 모든 일정)
    path('ajax/mine/', views.ajax_mine),
    path('ajax/total/', views.ajax_total),
    path('ajax/calendar/', views.ajax_calendar),

    # 디테일 => 멤버 관리 페이지로 렌더링
    path('<int:pk>/member/', views.member, name='member'),
    # 참가 신청 버튼 클릭 시
    path('<int:pk>/apply/', views.apply, name='apply'),

    # 수락 거절 / 삭제
    path('<int:article_pk>/member/accept/', views.accept, name='accept'),
    path('<int:pk>/delete_member/', views.delete_member, name="delete_member"),
]
