import argparse
import os
import smtplib
from email.mime.text import MIMEText
from time import sleep

def main():
    parser = argparse.ArgumentParser(prog='auto send mail script', description='Send mail to receivers with same content.')

    parser.add_argument('-s', '--subject', help='mail subject', required=True)
    parser.add_argument('-c', '--content', help='mail content, must be in html format. You can add image but only with image tag, view the same in sample.html', required=True)
    parser.add_argument('-r', '--receiver', help='mail receiver, txt file. Separate with end line.', required=True)
    parser.add_argument('-a', '--account', help='sender account. Beware if you want to send mail to education organization, you must use an email inside that organization.', required=True)
    parser.add_argument('-p', '--password', help='sender password. This password can be retrieve by follow this instruction: https://support.google.com/mail/answer/185833?hl=en', required=True)
    parser.add_argument('-t', '--time', help='time between 2 mail sending, default is 2 sec', default=2, type=int)
    args = parser.parse_args()


    # check file exist
    _check_file_exist(args.content)
    _check_file_exist(args.receiver)

    # read content
    content = open(args.content, encoding='utf-8').read()
    receiver = open(args.receiver, encoding='utf-8').read().splitlines()

    # sender
    sender = args.account

    # time
    time = args.time

    # login
    server = _login(args.account, args.password)
    
    # send mail
    for i, receiver in enumerate(receiver):
        print(i, receiver)
        _send_mail(server, sender, receiver, args.subject, content, time)

def _check_file_exist(file_path):
    if not os.path.isfile(file_path):
        print(f'File {file_path} not exist')
        exit(1)

def _send_mail(server, sender, receiver, subject, content, time):
    msg = MIMEText(content, "html")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    try:
        server.sendmail(sender, receiver, msg.as_string())
    except Exception as e:
        print(e)
        sleep(180)
        server = login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
    sleep(time)

def _login(username, password):
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com")
        server.login(username, password)
    except:
        print('Login failed. Check your username and password')
        exit(1)
    return server

if __name__ == '__main__':
    main()

