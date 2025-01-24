from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializer import CommentSerializer, CommentDetailSerializer


class CommentList(generics.ListCreateAPIView):  
    '''
    Creates a generic view to avoid code repetition.
    - 'list' = GET method
    - 'Create' = POST method
    https://www.django-rest-framework.org/api-guide/generic-views/#attributes/
    '''
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    # https://www.django-rest-framework.org/api-guide/filtering/

    filter_backends = [
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'post'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
