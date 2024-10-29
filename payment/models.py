import secrets

from django.db import models
from django.utils import timezone
from django.db import models

from users.models import User
from .paystack  import  Paystack


# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payment')
    amount = models.PositiveIntegerField()
    email = models.EmailField()
    access_code = models.CharField()
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"User: {self.user} - Payment: {self.amount}"

    # def save(self, *args, **kwargs):
    #     while not self.ref:
    #         ref = secrets.token_urlsafe(50)
    #         object_with_similar_ref = Payment.objects.filter(ref=ref)
    #         if not object_with_similar_ref:
    #             self.ref = ref

    #     super().save(*args, **kwargs)
        
    def amount_value(self):
        return int(self.amount) * 100
    
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
