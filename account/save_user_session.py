from .models import User_sessions, User
from django.contrib.sessions.models import Session
from datetime import datetime

def SaveUserSession(sessionKey, userId):
  session = Session.objects.get(session_key=sessionKey)
  user = User.objects.get(pk=userId)
  if session is None or user is None: return

  userSession = User_sessions.objects.create(
    user=user,
    session=session
  )
  User_sessions.objects \
    .filter(user_id=userId) \
    .filter(active=True) \
    .exclude(pk=userSession.id) \
    .update(active=False, closed_at=datetime.now())
  return