#!/usr/local/bin/python3

import gmail
import sys
import httplib2

from googleapiclient import discovery

def main():
    print("Fetching API Credentials")
    credentials = gmail.GetCredentials()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # print(service.users().getProfile(userId="me").execute())

    sender = ""
    to = ""
    subject = "hello world"
    msg_txt = "Hello World"

    print("Composing email")
    msg = gmail.CreateMessage(sender, to, subject, msg_txt)
    # print(msg)
    # return
    print("Sending email")
    gmail.SendMessage(service, "me", msg)

    sys.exit()

if __name__ == "__main__":
    main()