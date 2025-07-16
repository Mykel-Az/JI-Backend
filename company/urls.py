from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from .views import CompanyProfileViewSet, CompanyReviewViewSet

router = SimpleRouter()
router.register(r'companies', CompanyProfileViewSet, basename='company')

company_router = NestedSimpleRouter(router, r'companies', lookup='company')
company_router.register(r'reviews', CompanyReviewViewSet, basename='company-reviews')

urlpatterns = router.urls + company_router.urls
