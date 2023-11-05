from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
import uuid



class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        username = extra_fields.pop('username', None)
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        if mobile_number:
            user.mobile_number = mobile_number
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(mobile_number, **extra_fields)


class AdnocUser(AbstractUser):
    mobile_number = models.CharField(max_length=15,unique=True)
    username = models.CharField(max_length = 100,null=True)
    withdrawable_amount = models.FloatField(default=0,null=True, blank=True)
    recharge_amount = models.FloatField(default=0,null=True, blank=True)
    referal_code = models.TextField()
    refered_by = models.ForeignKey("AdnocUser",related_name="ref_user",on_delete=models.CASCADE,null=True,blank=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    # REQUIRED_FIELDS = ['name']
    # class Meta:
    #     unique_together = ['username','mobile_number']

    def __str__(self):
        return self.mobile_number+"_"+str(self.username)

    # def save(self, *args, **kwargs):
    #     # Avoid uniqueness check for the username field
    #     self._meta.get_field('username')._unique = False
    #     super().save(*args, **kwargs)
    #     self._meta.get_field('username')._unique = True


class OTP(models.Model):
    user = models.ForeignKey('AdnocUser', on_delete=models.CASCADE,null=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.otp+"_"+str(self.user)


class userBank(models.Model):
    accname = models.TextField()
    accnum = models.TextField()
    ifsc = models.TextField()
    mobnum = models.IntegerField()
    acctype = models.TextField()
    user_id = models.OneToOneField("AdnocUser",  on_delete=models.CASCADE)

class Product(models.Model):
    prod_name = models.CharField(max_length=100)
    prod_img = models.ImageField(upload_to='products')
    prod_price = models.FloatField()
    daily_inc = models.FloatField()
    total_inc = models.IntegerField()
    validity_period = models.IntegerField()

    def __str__(self):
        return self.prod_name

class UserRecharge(models.Model):
    user_id = models.ForeignKey('AdnocUser',related_name="userPro",on_delete =models.CASCADE)
    recharge_date = models.DateTimeField(null=True)
    transaction_id = models.CharField(max_length=30,null=True)
    transaction_image = models.ImageField(upload_to='transaction',null=True)
    is_valid = models.BooleanField(default=False,null=True)
    recharge_amount = models.IntegerField()
    is_credited = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_id)+"_"+str(self.recharge_date)


class Purchase(models.Model):
    prod_id = models.ForeignKey('Product',on_delete =models.CASCADE)
    user_id = models.ForeignKey('AdnocUser',on_delete =models.CASCADE)
    purchase_date = models.DateTimeField(null=True)
    transaction_id = models.CharField(max_length=30,null=True)
    transaction_image = models.ImageField(upload_to='transaction',null=True)
    is_approved = models.BooleanField(default=False,null=True)

    def __str__(self):
        return str(self.prod_id)+"_"+str(self.user_id)

class WalletHistory(models.Model):
    user_purchase = models.ForeignKey('Purchase',on_delete=models.CASCADE,null=True)
    earning = models.FloatField()
    transaction_date = models.DateTimeField()

    def __str__(self):
        return str(self.user_purchase)+"_"+str(self.earning)

class WithdrawRequest(models.Model):
    amount = models.FloatField()
    request_date = models.DateTimeField()
    acc_name = models.CharField(max_length=60)
    acc_no = models.CharField(max_length=20)
    ifsc = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10,default="Pending")
    user_id = models.ForeignKey('AdnocUser',on_delete =models.CASCADE)

    def __str__(self):
        return str(self.user_id)


class transactions(models.Model):
    amount=models.FloatField()
    trans_date = models.DateTimeField( auto_now=False, auto_now_add=True)
    user_id = models.ForeignKey("AdnocUser", on_delete=models.CASCADE)
    credited = models.BooleanField()
    tag = models.TextField()

    def __str__(self):
        return str(self.id)