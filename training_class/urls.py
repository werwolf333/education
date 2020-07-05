from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'training_class'

urlpatterns = [
    path('', views.TrainingClass.as_view(), name='Post_List'),

    path('<str:group>/task', views.TeacherTask.as_view(), name='TeacherTask'),
    path('<str:group>/task/add', views.TeacherTaskAdd.as_view(), name='TeacherTaskAdd'),
    path('<str:group>/task/<int:id>/edit', views.TeacherTaskEdit.as_view(), name='TeacherTaskEdit'),
    path('<str:group>/task/<int:id>/delete', views.TeacherTaskDelete.as_view(), name='TeacherTaskDelete'),
    path('<str:group>/task/<int:id>/decision', views.TeacherTaskDecision.as_view(), name='TeacherTaskDecision'),
    path('<str:group>/task/<int:id>/decision/<int:id_dec>/edit', views.TeacherTaskDecisionEdit.as_view(), name='TeacherTaskDecision'),

    path('<str:group>/decision', views.Decision.as_view(), name='Decision'),
    path('<str:group>/decision/<int:id>/add', views.DecisionAdd.as_view(), name='DecisionAdd'),
    path('<str:group>/decision/<int:id>', views.DecisionList.as_view(), name='DecisionList'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

