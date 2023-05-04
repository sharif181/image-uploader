from .models import FileUpload, GenerateLink
from .serializers import FileUploadSerializer, FileListSerializer, GenerateLinkSeiralizer
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework import generics

class FileUploadViewSet(generics.CreateAPIView):
    queryset = FileUpload.objects.order_by('id')
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ImageListView(generics.ListAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileListSerializer


    permission_classes = [
        permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = FileUpload.objects.all()
        qs = qs.filter(creator=self.request.user)
        return qs


class ImageDetailsView(generics.RetrieveAPIView):
    queryset = FileUpload.objects.all()
    lookup_field = 'pk'
    serializer_class = FileListSerializer

    permission_classes = [
        permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = FileUpload.objects.all()
        qs = qs.filter(creator=self.request.user)
        return qs


class GenerateLinkListView(generics.ListAPIView):
    queryset = GenerateLink.objects.all()
    serializer_class = GenerateLinkSeiralizer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        qs = GenerateLink.objects.all()
        qs = qs.filter(creator=self.request.user)
        return qs


class GenerateLinkDetailView(generics.RetrieveAPIView):
    queryset = GenerateLink.objects.all()
    serializer_class = GenerateLinkSeiralizer
    lookup_field = 'pk'

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        qs = GenerateLink.objects.all()
        qs = qs.filter(creator=self.request.user)
        return qs
    
class GenerateLinkCreateView(generics.CreateAPIView):
    serializer_class = GenerateLinkSeiralizer
    queryset = GenerateLink.objects.all()
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        qs = FileUpload.objects.all()
        qs = qs.filter(creator=self.request.user)
        return qs


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)