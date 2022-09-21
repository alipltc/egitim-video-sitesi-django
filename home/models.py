from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=70)
    address = models.CharField(max_length=120)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    smtpserver = models.CharField(max_length=20)
    smtpemail = models.CharField(max_length=20)
    smtppassword = models.CharField(max_length=20)
    smtpport = models.CharField(max_length=5)
    icon = models.ImageField(blank=True,upload_to='images/')
    facebook = models.CharField(blank=True,max_length=60)
    instagram = models.CharField(blank=True,max_length=60)
    twitter = models.CharField(blank=True,max_length=60)
    aboutus = RichTextUploadingField()
    contact = RichTextUploadingField()
    referans = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('Read', 'Okundu'),
        ('Closed', 'Kapalı'),
    )
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=255)
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=120)
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Contact Form Message"
        verbose_name_plural = "Contact Form Message"

class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name','email','subject','message']
        widgets = {
            'name' :  TextInput(attrs={'id':'Name & Surname' ,'class':'form-control unicase-form-control text-input'}),
            'subject' :  TextInput(attrs={'id': 'Subject','class':'form-control unicase-form-control text-input'}),
            'email': TextInput(attrs={'id': 'Email Address','class':'form-control unicase-form-control text-input'}),
            'message': Textarea(attrs={'id': 'Your Message','class':'form-control unicase-form-control'}),

        }

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/user/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return '[' +self.user.username +'] ' +self.user.first_name + ' ' +self.user.last_name

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']

class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    siranumara = models.CharField(blank=True, max_length=20)
    question = models.CharField(blank=True, max_length=150)
    answer = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question