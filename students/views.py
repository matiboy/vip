# Create your views here.
from django.utils.translation import ugettext as _
import string
import cms.models
import students.models
import django.shortcuts
import django.template
import django.templatetags
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
import django.contrib
import django.views.decorators.http
import django.contrib.humanize
import django.core.paginator
import django.views.generic
import django.contrib.auth.decorators
import django.utils.decorators
import cms.forms
import vip.extras
import json
from django.core.urlresolvers import reverse_lazy, reverse
import vip.settings
import os
import logging
import django.http
import datetime
import django.template.loader
import django_tables2
from vip.extras import get_image_url

# Create your views here.
def redirect(request,path):
    return django.shortcuts.redirect(maxman.settings.STATIC_URL + path)

def index(request):
    return django.shortcuts.render_to_response("index.html")

class ProtectedView(django.views.generic.View):
    @django.utils.decorators.method_decorator(django.contrib.auth.decorators.login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)

class StaffOnlyView(ProtectedView):
    def dispatch(self,*args,**kwargs):
        if args[0].user.is_staff:
            return super(ProtectedView, self).dispatch(*args, **kwargs)
        else:
            return django.shortcuts.redirect(reverse("frontend.index"))

class HomeView(ProtectedView):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff == False:
            return django.shortcuts.redirect(reverse("frontent.index"))
        get_token(request)
        c = {}
        # See if we can find a set of preferences
        c.update({"is_logged":request.user.is_authenticated()})
        return django.shortcuts.render_to_response("cms/home.html",c,context_instance=django.template.RequestContext(request))

#from django.utils.decorators import method_decorator
class ProtectedTemplateView(StaffOnlyView, django.views.generic.TemplateView):
    template_name = 'secret.html'

class ProtectedListView(StaffOnlyView,django.views.generic.ListView):
    template_name = 'secret.html'

class ProtectedCreateView(StaffOnlyView,django.views.generic.CreateView):
    template_name = 'secret.html'

class ProtectedUpdateView(StaffOnlyView,django.views.generic.UpdateView):
    template_name = 'secret.html'

class ProtectedDeleteView(StaffOnlyView, django.views.generic.DeleteView):
    template_name = 'secret.html'

'''
Utility class that redefines get_success_url to handle redirecting according to which submit button was clicked
if self.submit_back is found as a key in POST, redirects to success_view_back (using a reverse url)
otherwise, redirects to success_view (using a reverse url) with pk as argument
'''
class UpdateCreateWithRedirectView():
    # Names of the POST attributes
    submit = "submit-continue"
    submit_back = "submit-back"
    def get_success_url(self,pk=None):
        # See if we are submitting or submitting and expecting to go back
        try:
            key = self.request.POST["button-pressed"]
        except:
            # Going back
            return reverse( self.success_view_back )
        else:
            if key == self.submit_back:
                return reverse( self.success_view_back )
        if self.request.POST.get("button-pressed","") == self.submit_back:

            # Going back
            return reverse( self.success_view_back )
        else:
            if pk is None:
                pk = self.object.pk
            return reverse( self.success_view, kwargs={"pk":pk} )

class MediaImageIframe(ProtectedCreateView):
    template_name = "cms/media_iframe.html"
    form_class = cms.forms.ImageForm
    #model = daemon.models.Image

    def get_context_data(self, **kwargs):
        context = super(MediaImageIframe, self).get_context_data(**kwargs)
        context["action"] = reverse_lazy( "cms.media.images.iframe", kwargs={"pk":self.kwargs["pk"]} ) + "/"
        return context

    def form_valid(self,form):
        self.object = form.save(commit=False)
        # Add the media id
        self.object.media_id = self.kwargs["pk"]
        return super(MediaImageIframe, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy( "cms.media.images.iframe", kwargs={"pk":self.kwargs["pk"]} )

class StudentList(ProtectedListView):
    template_name = "cms/students/student_list.html"
    context_object_name = 'student_list'

    def get_queryset(self):
        return students.models.Student.objects.all()

'''class RecommendedDelete(StaffOnlyView,maxman.extras.JsonView):
    def post( self, request, *args, **kwargs):
        id = kwargs["pk"]
        # Find corresponding media
        try:
            cms.models.Recommended.objects.get(media_id=id).delete()
        except:
            return self._response.error_and_respond(_("Unable to delete"))

        return self._response.respond()'''
