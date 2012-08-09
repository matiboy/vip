import json
import django.http
import django.forms.util
from django.contrib.gis.geoip import GeoIP
import django.db
import VIP.settings
import django.views.generic
from django.core.urlresolvers import reverse_lazy, reverse

def get_image_url( image, request ):
    return request.build_absolute_uri( reverse("cms.media",kwargs={"path":image.replace( VIP.settings.MEDIA_URL, "" )}))

class RawErrorList(django.forms.util.ErrorList):
    def __unicode__(self):
        return self.raw()
    
    def raw(self):
        if not self:
            return u''
        return ','.join([u'%s' % e for e in self])

class JsonView(django.views.generic.View):
    def __init__(self, **kwargs):
        super(JsonView, self).__init__(**kwargs)
        self._response = VIP.extras.JsonResponse()

class JsonMessage(object):
    def __init__( self, msg, t="info" ):
        self.type = t
        self.msg = msg
        
    def toDict(self):
        return {"type":self.type,"message":self.msg }
        
    def toJson(self):
        return json.dumps( self.toDict() )

class JsonSuccess(JsonMessage):
    def __init__( self, msg ):
        super( JsonSuccess, self ).__init__( msg, "success" )
        
class JsonError(JsonMessage):
    def __init__( self, msg ):
        super( JsonError, self ).__init__( msg, "error" )
        
class JsonAlert( JsonMessage ):
    def __init__( self, msg ):
        super( JsonAlert, self ).__init__( msg, "alert" )
        
class JsonDebug( JsonMessage ):
    def __init__( self, msg ):
        super( JsonDebug, self ).__init__( msg, "debug" )
        
def json_handler(obj):
    if hasattr( obj, "toJson"):
        return obj.toDict()
    
class JsonResponse(object):
    def __init__(self):
        self._success = True
        self._messages = []
        self._html = ""
        self._data = {}
        
    def toDict(self):
        return {"success":self._success,"messages":self._messages,"html":self._html,"data":self._data}
        
    def toJson(self):
        return json.dumps(self.toDict())
    
    def respond(self):
        if VIP.settings.DEBUG_JSON_QUERIES:
            self.data(key="queries",value=django.db.connection.queries)
        return django.http.HttpResponse(json.dumps(self,default=json_handler),mimetype="application/json")
    
    def success(self,direction=None):
        if direction is None:
            return self._success
        self._success = direction
        
    def html(self,html=None):
        if html is None:
            return self._html
        self._html = html
        
    def error(self,message,modify_success=True):
        self._messages.append(JsonError(message))
        if modify_success:
            self.success(False)
        return self
    
    def error_and_respond(self,message,modify_success=True):
        self.error(message,modify_success)
        return self.respond()
    
    def message(self,message):
        self._messages.append(JsonSuccess(message))
        return self
    
    def alert(self,message):
        self._messages.append(JsonAlert(message))
        return self
    
    def debug(self,message):
        if VIP.settings.DEBUG:
            self._messages.append(JsonDebug(message))
        return self
        
    def data(self,*args,**kwargs):
        if args.__len__() == 0:
            key = kwargs["key"]
            value = kwargs.get( "value", None )
            if value is None:
                try:
                    return self._data[key]
                except:
                    raise
            else:
                self._data[key] = value
        else:
            for couple in args:
                self.data(key=couple[0], value=couple[1])
        return self