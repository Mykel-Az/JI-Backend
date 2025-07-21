from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from core.common.models import Location, Review
from .models import *
from accounts.serializers import MinimalUserSerializer
from professionals.serializers import MinimalProfessionalSerializer


class CompanyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class MinimialCompanySerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    # avaliable_jobs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CompanyProfile
        fields = ['id', 'company_name', 'location', 'logo', 'average_rating', 
                  'total_jobs_open', 'is_remote_friendly', 'is_verified', 'is_active']
        
    

class CompanyReviewSerializer(serializers.ModelSerializer):
    reviewer = MinimalUserSerializer(read_only=True)
    reviewed_user = MinimialCompanySerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'reviewed_user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'reviewer', 'reviewed_user', 'created_at']



class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['reviewed_user', 'rating', 'comment']


class CompanyFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFAQ
        fields = ['id', 'question', 'answer']


class CompanyTeamMemberSerializer(serializers.ModelSerializer):
    name = MinimalProfessionalSerializer(read_only=True)

    class Meta:
        model = CompanyTeamMember
        fields = ['id', 'name', 'postion']



class CompanyProfileSerializer(serializers.ModelSerializer):

    Alumini = CompanyTeamMemberSerializer(many=True, read_only=True)
    faqs = CompanyFAQSerializer(many=True, read_only=True)
    location = serializers.StringRelatedField()
    followers = MinimalUserSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    

    class Meta:
        model = CompanyProfile
        fields = '__all__'
        read_only_fields = ['is_verified', 'is_active', 'total_jobs_posted', 'total_jobs_open', 'total_followers', 'average_rating']

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_reviews(self, obj):
        return CompanyReviewSerializer(Review.objects.filter(reviewed_user=obj.user), many=True).data


class CompanyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = ['id', 'company_name', 'industry', 'category', 'company_size', 'founded_year', 'location', 'is_remote_friendly',
                  'tagline', 'description', 'mission_statement',
                  'logo', 'cover_image', 'website', 'linkedin_url', 'twitter_url',
                  'Alumini', 'faqs',
                  'contact_email', 'contact_phone',
                  'followers', 'reviews',
                  'is_verified', 'is_active']

    def create(self, validate_data):
        company = CompanyProfile(**validate_data)
        company.save()
        return company
    

class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['category', 'company_size', 'location', 'is_remote_friendly',
                  'tagline', 'description', 'mission_statement',
                  'logo', 'cover_image', 'website', 'linkedin_url', 'twitter_url',
                  'Alumini', 'faqs',
                  'contact_email', 'contact_phone',
                  ]
        


