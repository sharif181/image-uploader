from rest_framework import serializers
from .models import FileUpload, GenerateLink
from django.contrib.sites.shortcuts import get_current_site
from PIL import Image
from pathlib import Path
from datetime import datetime
BASE = Path(__file__).resolve().parent.parent.parent



class FileUploadSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.username')
    creator_id = serializers.ReadOnlyField(source='creator.id')
    image_url = serializers.ImageField(required=True, write_only=True)

    class Meta:
        model = FileUpload
        fields = ['id', 'creator', 'creator_id', 'title', 'description', 'image_url']


class FileListSerializer(serializers.ModelSerializer):
    original_image_url = serializers.SerializerMethodField(required=False, read_only=True)
    thumbnail_url_200px = serializers.SerializerMethodField(read_only=True)
    thumbnail_url_400px = serializers.SerializerMethodField(read_only=True)
    arbitary_thumbnail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FileUpload
        fields = ['id', 'creator', 'original_image_url', 'thumbnail_url_200px', 'thumbnail_url_400px', 'arbitary_thumbnail']

    def get_original_image_url(self, obj):
        user = self.context['request'].user
        domain = get_current_site(self.context['request']).domain
        build_in_tier = user.build_in_tier
        arbitary_tier = user.arbitary_tier

        if build_in_tier in ['premium', 'enterprise'] or (arbitary_tier is not None and arbitary_tier.is_original_link):
            return f'http://{domain}/media/{str(obj.image_url)}'
        else:
            return None

    def get_thumbnail_url_200px(self, obj):
        user = self.context['request'].user
        domain = get_current_site(self.context['request']).domain
        build_in_tier = user.build_in_tier
        # arbitary_tier = user.arbitary_tier
        if build_in_tier in ['basic', 'premium', 'enterprise']:
            size = (200, 200)
            im = Image.open(obj.image_url) 
            im = im.resize(size)
            file_name = str(obj.image_url).split("/")[-1]
            name = file_name.split(".")[0]
            exten = file_name.split(".")[-1]
            file_name = f"{name}_200px.{exten}"
            im.save(f'{BASE}/mediafiles/images/{file_name}')
            return f'http://{domain}/media/images/{file_name}'
        else:
            return None
        
    
    def get_thumbnail_url_400px(self, obj):
        user = self.context['request'].user
        domain = get_current_site(self.context['request']).domain
        build_in_tier = user.build_in_tier
        # arbitary_tier = user.arbitary_tier
        if build_in_tier in ['premium', 'enterprise']:
            size = (400, 400)
            im = Image.open(obj.image_url) 
            im = im.resize(size)
            file_name = str(obj.image_url).split("/")[-1]
            name = file_name.split(".")[0]
            exten = file_name.split(".")[-1]
            file_name = f"{name}_400px.{exten}"
            im.save(f'{BASE}/mediafiles/images/{file_name}')
            return f'http://{domain}/media/images/{file_name}'
        else:
            return None

    def get_arbitary_thumbnail(self, obj):
        user = self.context['request'].user
        domain = get_current_site(self.context['request']).domain
        arbitary_tier = user.arbitary_tier
        if arbitary_tier is not None:
            size_ = user.arbitary_tier.thumbnail_size
            size = (size_, size_)
            im = Image.open(obj.image_url) 
            im = im.resize(size)
            file_name = str(obj.image_url).split("/")[-1]
            name = file_name.split(".")[0]
            exten = file_name.split(".")[-1]
            file_name = f"{name}_{size_}px.{exten}"
            im.save(f'{BASE}/mediafiles/images/{file_name}')
            return f'http://{domain}/media/images/{file_name}'
        else:
            return None
# http://127.0.0.1:8000/media/images/images.jpg

class FileUploadPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context.get("request").user
        return FileUpload.objects.filter(
            creator = user
         )

class GenerateLinkSeiralizer(serializers.ModelSerializer):

    link = serializers.SerializerMethodField(read_only=True)
    image = FileUploadPrimaryKeyRelatedField(write_only=True)
    
    class Meta:
        model = GenerateLink
        fields = ['id', 'link', 'link_duration', 'image']
    
    def get_link(self, obj):
        create_date = obj.create_at.date()
        now_date = datetime.now().date()
        if create_date == now_date:
            create_at = obj.create_at.timestamp()
            now = datetime.now().timestamp()
            if round(now - create_at) < obj.link_duration:
                domain = get_current_site(self.context['request']).domain
                return f'http://{domain}/media/{obj.image.image_url}'
        return 'Time expired'
    

    # def create(self, validated_data):
    #     validated_data['creator'] = self.context['request'].user
    #     # obj = GenerateLink.objects.create(**validated_data)
    #     # obj.save()
    #     return super().create(validated_data)