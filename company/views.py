from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import mixins
from .models import *
from .serializers import *
# Create your views here.


class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['company_name', 'tagline', 'industry__name']
    ordering_fields = ['created_at', 'average_rating', 'company_name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return CompanyCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CompanyUpdateSerializer
        elif self.action == 'list':
            return MinimialCompanySerializer
        return CompanyProfileSerializer
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
    


class CompanyReviewViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CompanyReviewSerializer

    def get_queryset(self):
        slug = self.kwargs.get('company_slug')
        try:
            company = CompanyProfile.objects.get(slug=slug)
        except CompanyProfile.DoesNotExist:
            raise ValidationError("Company not found.")
        return Review.objects.filter(reviewed_user=company.user)

    def create(self, request, *args, **kwargs):
        slug = self.kwargs.get('company_slug')
        try:
            company = CompanyProfile.objects.get(slug=slug)
        except CompanyProfile.DoesNotExist:
            return Response({"detail": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == company.user:
            raise ValidationError("You cannot review your own company.")

        if Review.objects.filter(reviewer=request.user, reviewed_user=company.user).exists():
            raise ValidationError("You have already reviewed this company.")

        serializer = ReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save(reviewer=request.user, reviewed_user=company.user)

        return Response(CompanyReviewSerializer(review).data, status=status.HTTP_201_CREATED)
    
    

# class findtalent:
#     def get(self, request):
#         return render(request, 'company/find_talent.html')
    


