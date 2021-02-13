from django.utils.deprecation import MiddlewareMixin

class CreateSession(MiddlewareMixin):
  def process_request(self, request):
    if request.session.session_key is not None:
      return None
    
    request.session['HTTP_USER_AGENT'] = request.META['HTTP_USER_AGENT']
    return None