from rest_framework import serializers
from .models import Profile

# serializers allow you to convert data from Python objects into a
# format that can be easily rendered into JSON or parsed from
# incoming JSON requests

class ProfileSerializer(serializers.ModelSerializer):
    '''  '''
    owner = serializers.ReadOnlyField(source='ownder.username')

    # id field is created automatically with (model.Model).

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'content', 'image'
        ]
