"""
Defining URLs for learning_logs app.
"""

from django.urls import path
from django.views.generic import TemplateView


from . import views
from .views import EntryListView 

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    
    path(
        "topics/<int:topic_id>/entries/", EntryListView.as_view(),
        name="entry-list"
    ),
    path("topicsview/", TemplateView.as_view(template_name="learning_logs/topics_view.html"), name="topics-view"),
    
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),


]