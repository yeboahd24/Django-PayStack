from django.db import models
import secrets
from .paystack import Paystack

class Product(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='product_images')
    price = models.FloatField()
    slug = models.SlugField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class Payment(models.Model):
    amount = models.PositiveIntegerField()
    reference = models.CharField(max_length=100)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)


    def __str__(self):
        return f"Payment {self.amount} made by {self.email}"


    def save(self, *args, **kwargs):
        while not self.reference:
            ref = secrets.token_urlsafe(50)
            similar_reference = Payment.objects.filter(reference=ref)
            if not similar_reference:
                self.reference = ref
        super().save(*args, **kwargs)


    def amount_value(self):
        return self.amount*100


    def verify_payment(self):
        paystack = Paystack()
        status,result = paystack.verify_payment(self.reference, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
