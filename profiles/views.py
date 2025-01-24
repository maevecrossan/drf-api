from django.db.models import Count
from rest_framework import generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.annotate
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True), # no direct link between models, so '__' needed.
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer

    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__followed__created_at',
        'owner__following__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
