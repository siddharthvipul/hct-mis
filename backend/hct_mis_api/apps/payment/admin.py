from django.contrib import admin

from hct_mis_api.apps.payment.models import PaymentRecord, CashPlanPaymentVerification, PaymentVerification


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(CashPlanPaymentVerification)
class CashPlanPaymentVerificationAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentVerification)
class PaymentVerificationAdmin(admin.ModelAdmin):
    pass
