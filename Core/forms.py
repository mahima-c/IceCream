from django import forms

from .models import ContactUs, Registration, Branch, Year, Gender, Event

from django.forms import ValidationError

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
import datetime
import re

class ContactUsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())

    class Meta:
        model = ContactUs
        fields = ['name', 'contact', 'email', 'subject', 'message','captcha']

    name = forms.CharField(
        max_length=225, required=True,
        widget=forms.TextInput(
            attrs={'type': 'text',
                   'name': 'name',
                   'class': 'form-control',
                   'id': 'exampleInputName1',
                   'placeholder': 'Enter Name'
                   }
        )
    )
    contact = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={'type': 'number',
                   'name': 'contact',
                   'class': 'form-control',
                   'id': 'exampleInputcontact1',
                   'placeholder': 'Enter Contact No'
                   }
        )
    )
    email = forms.EmailField(
        max_length=50, required=True,
        widget=forms.EmailInput(
            attrs={'type': 'email',
                   'name': 'email',
                   'class': 'form-control',
                   'id': 'exampleInputEmail1',
                   'placeholder': 'Enter Email'}
        )
    )
    subject = forms.CharField(
        225, required=True,
        widget=forms.TextInput(
            attrs={'type': 'text',
                   'name': 'subject',
                   'class': 'form-control',
                   'id': 'exampleInputsub1',
                   'placeholder': 'Enter Subject'}
        )
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'name': 'message',
                   'id': 'message',
                   'rows': '5'
                   }
        ),
    )


class RegistrationForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    
    class Meta:
        model = Registration
        fields = ['name', 'contact', 'email', 'student_number', 'branch','year','gender','hosteler','captcha']
        # exclude = ['event', 'fee_paid']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(
            max_length=225, required=True,
            widget=forms.TextInput(
                attrs={'type': 'text',
                       'name': 'name',
                       'class': 'form-control',
                       'id': 'Name',
                       'placeholder': 'Enter Name',
                       'onblur': ''}
            )
        )

        self.fields['email'] = forms.EmailField(
            max_length=50, required=True,
            widget=forms.EmailInput(
                attrs={'type': 'email',
                       'name': 'email',
                       'class': 'form-control',
                       'id': 'Email',
                       'placeholder': 'Enter Email'}
            )
        )

        self.fields['contact'] = forms.CharField(
            required=True,
            widget=forms.TextInput(
                attrs={'type': 'text',
                       'name': 'contact',
                       'class': 'form-control',
                       'id': 'Contact',
                       'placeholder': 'Enter Contact No.',
                       'onblur': ''
                       }
            )
        )
        self.fields['student_number'] = forms.CharField(
            required=True,
            widget=forms.TextInput(
                attrs={'type': 'text',
                       'class': 'form-control',
                       'id': 'Student',
                       'placeholder': 'Enter Student Number',
                       'onblur': ''}
            )
        )

        self.fields['branch'] = forms.ModelChoiceField(
            queryset=Branch.objects.filter(active=True),
            required=True,
            widget=forms.Select(
                # choices=BRANCH_CHOICES,
                attrs={'class': 'form-control',
                       'data-val': 'true',
                       'data-val-required': '*',
                       'id': 'Branch',
                       'name': 'Branch',
                       'onchange': 'validateBranch()'}
            )
        )

        self.fields['year'] = forms.ModelChoiceField(
            queryset=Year.objects.filter(active=True),
            required=True,
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'data-val': 'true',
                       'data-val-required': '*',
                       'id': 'Year',
                       'name': 'Year'},
            ),
        )

        self.fields['gender'] = forms.ModelChoiceField(
            queryset=Gender.objects.all(),
            required=True,
            widget=forms.Select(
                attrs={'class': 'form-control',
                       'data-val': 'true',
                       'data-val-required': '*',
                       'id': 'Gender',
                       'name': 'Gender',
                       'type': 'radio'})
        )

        self.fields['hosteler'] = forms.BooleanField(
            required=False,
            widget=forms.CheckboxInput(
            attrs={
                'data-val': 'true',
                'data-val-required': 'the hosteler field is required',
                'id': 'IsHosteler',
                'name': 'IsHosteler',
                'type': 'checkbox'}
            )
        )

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        try:
            student_number = cleaned_data['student_number']
        except KeyError:
            raise ValidationError("")
        
        year = datetime.date.today().year
        end = ''
        start = ''

        for i in range(year, year-4, -1):
            end += str(i % 10)
            i = int(i/10)
            start += str(i % 10)

        regex = "^["+start+"]["+end+"](12|14|10|13|00|31|21|32|40)[0-1][0-9][0-9][-]?[mdlMDL]?$"
        pattern = re.compile(regex)

        if student_number:
            if not pattern.match(str(student_number)):
                raise ValidationError("Invalid Student Number")

        try:
            email = cleaned_data['email']
        except KeyError:
            raise ValidationError("")

        event = Event.objects.filter(active=True).first()

        if Registration.objects.filter(email=email, event=event, student_number=student_number).exists():
            raise ValidationError('Registration with this student number and email already exist.')
        elif Registration.objects.filter(student_number=student_number, event=event).exists():
            raise ValidationError('Registration with this student number already exist.')
        elif Registration.objects.filter(email=email, event=event).exists():
            raise ValidationError('Registration with this email already exist.')

        return cleaned_data

