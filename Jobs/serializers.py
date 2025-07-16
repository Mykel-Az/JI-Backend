# from rest_framework import serializers
# from .models import (
#     Location, JobIndustry, JobCategory, SubCategory, EmploymentType,
#     Payment, JobTags, JobPost
# )
# from cities_light.models import Country, City
# from accounts.serializers import CustomUserSerializer  # adjust if needed


# # ----------------------------
# # Basic Serializers
# # ----------------------------

# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = ['id', 'name', 'code2']


# class CitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = City
#         fields = ['id', 'name']


# class LocationSerializer(serializers.ModelSerializer):
#     country = CountrySerializer()
#     city = CitySerializer()

#     class Meta:
#         model = Location
#         fields = ['id', 'country', 'city', 'address']

#     def create(self, validated_data):
#         country_data = validated_data.pop('country')
#         city_data = validated_data.pop('city')
#         country = Country.objects.get(id=country_data['id'])
#         city = City.objects.get(id=city_data['id'])
#         return Location.objects.create(country=country, city=city, **validated_data)

#     def update(self, instance, validated_data):
#         country_data = validated_data.pop('country', None)
#         city_data = validated_data.pop('city', None)

#         if country_data:
#             instance.country = Country.objects.get(id=country_data['id'])
#         if city_data:
#             instance.city = City.objects.get(id=city_data['id'])

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()
#         return instance



# class JobIndustrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobIndustry
#         fields = ['id', 'name', 'description']


# class JobCategoriesSerializer(serializers.ModelSerializer):
#     industry = serializers.PrimaryKeyRelatedField(queryset=JobIndustry.objects.all(), many=True)

#     class Meta:
#         model = JobCategory
#         fields = ['id', 'name', 'industry']


# class SubCategorySerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(queryset=JobCategory.objects.all(), many=True)

#     class Meta:
#         model = SubCategory
#         fields = ['id', 'name', 'category']


# class EmploymentTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmploymentType
#         fields = ['id', 'name', 'duration', 'description', 'is_flexible']


# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = ['id', 'currency', 'budget', 'description', 'is_flexible']


# class JobTagsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobTags
#         fields = ['id', 'name', 'description', 'is_active']


# # ----------------------------
# # JobPost Serializer (Main One)
# # ----------------------------

# class JobPostSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer(read_only=True)
#     industry = JobIndustrySerializer()
#     location = LocationSerializer()
#     employment_type = EmploymentTypeSerializer()
#     categories = JobCategoriesSerializer(many=True)
#     payment = PaymentSerializer()

#     class Meta:
#         model = JobPost
#         fields = [
#             'job_id', 'title', 'user', 'industry', 'description',
#             'location', 'job_type', 'employment_type', 'categories',
#             'payment', 'full_details', 'is_active', 'created_at', 'updated_at'
#         ]

#     def create(self, validated_data):
#         industry_data = validated_data.pop('industry')
#         location_data = validated_data.pop('location')
#         employment_data = validated_data.pop('employment_type')
#         categories_data = validated_data.pop('categories')
#         payment_data = validated_data.pop('payment')

#         industry = JobIndustry.objects.get_or_create(**industry_data)[0]
#         employment_type = EmploymentType.objects.get_or_create(**employment_data)[0]
#         payment = Payment.objects.get_or_create(**payment_data)[0]

#         # Handle nested city and country for location
#         country_data = location_data.pop('country')
#         city_data = location_data.pop('city')
#         country = Country.objects.get(id=country_data['id'])
#         city = City.objects.get(id=city_data['id'])
#         location = Location.objects.create(country=country, city=city, **location_data)

#         job = JobPost.objects.create(
#             user=self.context['request'].user,
#             industry=industry,
#             location=location,
#             employment_type=employment_type,
#             payment=payment,
#             **validated_data
#         )

#         for category_data in categories_data:
#             category = JobCategory.objects.get(id=category_data['id'])
#             job.categories.add(category)

#         return job


# from django.core.exceptions import ValidationError

# class ProfessionalJobPost(TimeModel):
#     ...
#     def clean(self):
#         if self.job_type != 'remote' and not self.location:
#             raise ValidationError("Location is required for onsite or hybrid jobs.")
