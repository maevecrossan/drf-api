from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    '''Displays list of Posts & Posts creation form'''

    # create post form
    serializer_class = PostSerializer

    # only shows above form if validated user
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        '''Retreive Posts'''
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        '''Create a Post'''
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class PostDetail(APIView):
    '''Returns singular post'''
    serializer_class = PostSerializer
    # Will render a form for us automatically
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        '''tries to find post by primary key,
        returns error if nonexistent'''
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''returns profile requested above'''
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request}
            )  # singular post retrieval
        return Response(serializer.data)

    def put(self, request, pk):
        '''allows post editing'''
        post = self.get_object(pk)

        serializer = PostSerializer(
            post, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
