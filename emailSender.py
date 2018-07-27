"""
    Sends email using Gmail API
"""

from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import urllib.error as error
import base64

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
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: {}'.format(message['id']))
        return message
    except error.HTTPError as err:
        print('An error occurred: ',err.reason)


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
    return {'raw': (base64.urlsafe_b64encode(message.as_bytes()).decode())}


def StartMessage():
    # Setup the Gmail API
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            'PATH\\TO\\client_secret.json', SCOPES)
        # flow = client.flow_from_clientsecrets(secret_file, SCOPES)
        creds = tools.run_flow(flow, store)
    service = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    try:
        service = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
        SendMessage(service, "me", CreateMessage("SOURCE-EMAIL-ADDRESS", "DEST-EMAIL-ADDRESS",
                                                 "Check myUMBC", "New updates on classifieds section"))

    except Exception as e:
        print(e)
        raise


# if __name__ == '__main__':
#     StartMessage()