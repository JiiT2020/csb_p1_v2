from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),

    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    #path('specifics/<int:question_id>/', views.detail, name='detail'),   # esimerkki polusta: specifics/-polku
    # ex: /polls/5/results/
    #path('<int:question_id>/results/', views.results, name='results'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # ex: /polls/1/comment/  # äänestysnumerokohtainen kommentin jättäminen
    path('<int:question_id>/comments/', views.leave_comment, name='leave_comment'),
    path('<int:question_id>/comment_thank_you/', views.comment_thanks, name='comment_thanks')
]