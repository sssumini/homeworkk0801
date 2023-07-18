from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)
    
    comments = serializers.SerializerMethodField(read_only=True)
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_field = ['id', 'comments', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post']