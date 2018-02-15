#!/usr/local/bin/python3

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import mimetypes
import os

from apiclient import errors

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from gmail import secrets

secrets = secrets.Definitions()
 
 
def GetCredentials():
    """Gets valid user credentials from storage.
 
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
 
    Returns:
      Credentials, the obtained credential.
    """

    store = Storage(secrets.CREDENTIAL_PATH)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(secrets.CLIENT_SECRET_FILE, secrets.SCOPES)
        flow.user_agent = secrets.APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + secrets.CREDENTIAL_PATH)

    return credentials

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: ' + message['id'])
    
    return message
  except errors.HttpError as err:
    print('An error occurred: ', err)



def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  # encoders.encode_base64(message)
  # print(message)
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  
  return {'raw': raw}