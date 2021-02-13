from django.core.files.storage import FileSystemStorage
from datetime import datetime

def file_upload(user_id:int, file) -> str:
  now = datetime.now()
  staticFilesUrl = f'/static/main/files/user_{user_id}/{now.strftime("%Y")}/{now.strftime("%m")}/{now.strftime("%d")}'

  location = f'main{staticFilesUrl}'
  fs = FileSystemStorage(location=location)
  fileSaveName = f'{now.strftime("%H_%M_%S")}_{file.name}'
  filename = fs.save(fileSaveName, file)
  fileUrl = f'{staticFilesUrl}{fs.url(filename)}'
  return fileUrl