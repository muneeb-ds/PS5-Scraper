import smtplib

from email.message import EmailMessage


class EmailUpdate:

    def __init__(self, content, email, password):
        self.content = content
        self.email = email
        self.password = password

    def mail_msg(self):
        msg = EmailMessage()
        msg['Subject'] = "PS5 in STOCK!"
        msg['From'] = "syedmuneeb54@gmail.com"
        msg['To'] = self.email

        msg.set_content("You scrapped stock info for BestBuy Canada")

        msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
            {0}
        </body>
        </html>
        """.format(self.content.to_html()),subtype = 'html')

        # content = MIMEText(html, 'html')
        # msg.attach(content)

        
        return msg

    def connect(self, smtp):
        smtp.login(self.email, self.password)

    def send(self):
        msg = self.mail_msg()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            self.connect(smtp)
            smtp.send_message(msg)
