from .           import views
from django.urls import path

urlpatterns = [
    path('', views.SympyCharFieldTestList.as_view(), name='formulas'),
    path('<pk>/', views.SympyCharFieldTest.as_view(), name='formulas'),
]
# from .                import views
# from django.conf.urls import url
#
# urlpatterns = [
#     url(r'^$', views.SympyCharFieldTestList.as_view(), name='formulas'),
#     url(r'^(?P<pk>[A-Z0-9-]+)/$', views.SympyCharFieldTest.as_view(), name='formulas'),
# ]