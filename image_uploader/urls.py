from django.urls import path, include
from .views import (
    FileUploadViewSet, ImageListView, 
    ImageDetailsView, GenerateLinkListView, 
    GenerateLinkDetailView, GenerateLinkCreateView
)

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'file-upload', FileUploadViewSet)

urlpatterns = [
    path('file-upload/', FileUploadViewSet.as_view()),
    path('file-list/', ImageListView.as_view()),
    path('file-details/<int:pk>', ImageDetailsView.as_view()),
    path('generate-links/', GenerateLinkListView.as_view()),
    path('generate-link-details/<int:pk>', GenerateLinkDetailView.as_view()),
    path('generate-link/', GenerateLinkCreateView.as_view())
]
