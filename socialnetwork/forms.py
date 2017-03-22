from django import forms
from django.core.validators import validate_email, RegexValidator
from django.contrib.auth.models import User
from models import *

MAX_UPLOAD_SIZE = 2500000

class PostsForm(forms.Form): #implement model forms for creating posts
    
    post = forms.CharField(max_length=160)

    def clean_post(self):
        post_data = self.cleaned_data.get('post')
        if len(post_data) > 160:
            raise forms.ValidationError(" Posts should be less than or equal to 160 characters")
        return post_data

class CommentForm(forms.Form): #implement model forms for creating posts
    
    comment = forms.CharField(max_length=160)

    def clean_post(self):
        comment_data = self.cleaned_data.get('comment')
        if len(post_data) > 160:
            raise forms.ValidationError(" Comments should be less than or equal to 160 characters")
        return comment_data


class RegistrationForm(forms.Form):
    
    username   = forms.CharField(max_length = 20,
                                 validators = [RegexValidator(r'^[0-9a-zA-Z]*$',
                                                              message='Enter only letters and numbers')])
    firstname = forms.CharField(max_length = 20)
    lastname = forms.CharField(max_length = 20)
    email      = forms.CharField(max_length = 40,label='E Mail',
                                 validators = [validate_email])
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                label='Confirm password',  
                                widget = forms.PasswordInput())
    age = forms.CharField(max_length = 2,required=False)
    bio = forms.CharField(max_length = 430,
                                label='Short Bio',
                                required=False, 
                                widget = forms.Textarea(attrs={'cols': 70, 'rows': 6}))
    pic = forms.ImageField(required=False, 
                            label='Profile Picture',
                            widget = forms.FileInput())
    #pic = forms.

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if(not age.isdigit() or int(age) < 1):
            raise forms.ValidationError("Age should be a number and greater than zero")
        
        return age

    def clean_pic(self):
        print 'clean_picture:'
        picture = self.cleaned_data['pic']
        print 'clean_picture:', picture
        if not picture:
            return None
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture

class EditForm(RegistrationForm):
    class Meta:
        fields = (
            'username',
            'password1',
            'password2',
            'pic',
        )