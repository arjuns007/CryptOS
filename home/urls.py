from django.urls import path
from . import views
urlpatterns = [
    path('about',views.about, name='about'),
    path('',views.cal_con, name='cal_con'),
    path('guide',views.guide, name='guide'),
    path('faq',views.faq, name='faq'),
    path('blog',views.blog, name='blog'),
   
]
