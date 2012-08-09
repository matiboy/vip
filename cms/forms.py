import cms.models
import django.forms
import daemon.models
import django.contrib.auth
import maxman.extras
import logging
import datetime

class AdvertForm(django.forms.ModelForm):
    url = django.forms.CharField( max_length=255, label="Destination URL", help_text="When clicking on the ad, the user will be redirected to this url" )
    class Meta:
        model = cms.models.Advert

class FrontSliderForm(django.forms.ModelForm):
    class Meta:
        model = cms.models.FrontSliderEntry

class MediaForm(django.forms.ModelForm):
    class Meta:
        model = daemon.models.Media
        fields = ('rating', 'highlighted','free',"price","is_trailer")

class UserForm(django.forms.ModelForm):
    class Meta:
        model = django.contrib.auth.models.User
        fields = ('username','first_name', 'last_name', 'email')

class UserProfileForm(django.forms.ModelForm):
    first_name = django.forms.CharField(max_length=255)
    last_name = django.forms.CharField(max_length=255)
    email = django.forms.EmailField()
    password1 = django.forms.CharField(max_length=255, widget=django.forms.PasswordInput, label="Password", initial="", required=False)
    password2 = django.forms.CharField(max_length=255, widget=django.forms.PasswordInput, label="Repeat password", initial="",required=False)
    date_of_birth = django.forms.DateField( widget=django.forms.DateInput( format="%Y-%m-%d" ) )
    view_only_password = django.forms.CharField( max_length=255, widget=django.forms.PasswordInput, required=False )

    class Meta:
        model = cms.models.UserProfile
        exclude = ('user','activation_key',)

        # Can't set this here, must set at run time
        #error_class= maxman.extras.RawErrorList

    def clean(self):
        return super(UserProfileForm,self).clean()

    def clean_email(self):

        return self.data["email"]

    def clean_password2(self):
        data = self.cleaned_data
        try:
            logging.debug("Clean password2: Instance")
            # If we have an instance, we can have blank password.
            # But if password is there, it must match
            if data["password1"] != "" and data["password2"] != data["password1"]:
                msg = "Passwords do not match"
                self._errors["password2"] = self.error_class([msg])
        except:
            # New because no instance
            if data["password1"] == "" or data["password2"] != data["password1"]:
                msg = "Password empty or passwords do not match"
                self._errors["password2"] = self.error_class([msg])
            logging.debug( "Clean password2: No instance" )
        return data["password2"]

class ChannelForm(django.forms.ModelForm):
    maxman_published = django.forms.DateTimeField(label="Published", initial=datetime.datetime.now)
    class Meta:
        model = daemon.models.Channel
        fields = ("price","genre","director","length","country","language","maxman_published","show_on_frontend","coming_soon","latest_show")

class ImageForm(django.forms.ModelForm):
    class Meta:
        model = daemon.models.Image
        exclude = ("media",)

class ChannelImageForm(django.forms.ModelForm):
    class Meta:
        model = daemon.models.ChannelImage
        exclude = ("channel",)

class FrontSliderEntryForm(django.forms.ModelForm):
    media = django.forms.ModelChoiceField(queryset=daemon.models.Media.objects.all().order_by("title"), required=False)
    channel = django.forms.ModelChoiceField(queryset=daemon.models.Channel.objects.all().order_by("title"),required=False)
    caption = django.forms.CharField(widget=maxman.fields.RedactorWidget)
    class Meta:
        model = cms.models.FrontSliderEntry
        exclude = ("order",)
