from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    '''Handles profile actions'''

    def get(self, request):
        '''Returns list of profiles'''
        profiles = Profile.objects.all()  # 1. returned all the profiles.
        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request}
            )
        # 2. We serialized them.
        # many=true : serializing many profile instances
        return Response(serializer.data)
        # 3. Sent serialized data in the response.


class ProfileDetail(APIView):
    '''Returns singular profile'''
    serializer_class = ProfileSerializer
    # Will render a form for us automatically
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        '''tries to find profile by primary key,
        returns error if nonexistent'''
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        '''returns profile requested above'''
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, context={'request': request}
            )  # singular profile retrieval
        return Response(serializer.data)

    def put(self, request, pk):
        '''allows profile editing'''
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
