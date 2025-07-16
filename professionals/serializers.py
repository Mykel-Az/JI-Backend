from rest_framework import serializers
from .models import ProfessionalUserProfile

class MinimalProfessionalSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    profile_picture = serializers.ImageField(read_only=True)

    class Meta:
        model = ProfessionalUserProfile
        fields = ['id', 'full_name', 'email', 'profile_picture', 'profession']


class ProfessionalUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    skills = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = ProfessionalUserProfile
        fields = '__all__'


# Filtering professionals by skill or location