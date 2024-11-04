import smtplib
from email.message import EmailMessage


def main():
    from_addr = "hao-se@outlook.com"
    to_addrs = ["xhrtxh@gmail.com"]
    access_token = ""

    msg = EmailMessage()
    msg.set_content("测试发送")
    msg['Subject'] = '测试发送'
    msg['From'] = from_addr
    msg['To'] = to_addrs[0]

    server = smtplib.SMTP(host="smtp-mail.outlook.com", port=587)
    server.set_debuglevel(1)
    server.starttls()
    server.docmd('AUTH', f'XOAUTH2 {access_token}')

    server.quit()


if __name__ == '__main__':
    main()
