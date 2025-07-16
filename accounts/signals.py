from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, AccountType
from professionals.models import ProfessionalUserProfile
from trades_services.models import TradeServiceProfile
from company.models import CompanyProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if not CustomUser.is_staff:
        if instance.account_type == AccountType.PROFESSIONAL and created:
            profile, _ = ProfessionalUserProfile.objects.get_or_create(user=instance)
        elif instance.account_type == AccountType.TRADE_BUSINESS and created:
            profile, _ = TradeServiceProfile.objects.get_or_create(user=instance)
        elif instance.account_type == AccountType.COMPANY and created:
            profile, _ = CompanyProfile.objects.get_or_create(user=instance)

        if not created:
            profile.save()  # Ensure the profile is saved if it already exists


# extend this to trigger email verification or setup default values in each profile too.


# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.account_type == AccountType.PROFESSIONAL and hasattr(instance, 'professionaluserprofile'):
#         instance.userprofile.save()
#     elif instance.account_type == AccountType.TRADE_BUSINESS and hasattr(instance, 'tradeserviceprofile'):
#         instance.tradeserviceprofile.save()
#     elif instance.account_type == AccountType.COMPANY and hasattr(instance, 'companyprofile'):
#         instance.companyprofile.save()