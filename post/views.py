from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

from django.shortcuts import get_object_or_404

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        post = serializer.instance
        self.handle_tags(post)

        return Response(serializer.data)
    
    def perform_update(self, serializer):
        post = serializer.save()
        post.tag.clear()
        self.handle_tags(post)

    def handle_tags(self, post):
        words = post.content.split(' ')
        tag_list = []
        for w in words:
            if w[0] == '#':
                tag_list.append(w[1:])
        
        for t in tag_list:
            tag, created = Tag.objects.get_or_create(name=t)
            post.tag.add(tag)
        
        post.save()

    
class CommentViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
class PostCommentViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        queryset = self.filter_queryset(self.get_queryset().filter(post=post))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self,request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)