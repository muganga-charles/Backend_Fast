# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# class Email:
#     def __init__(self, recipient_email, subject):
#         self.recipient_email = recipient_email
#         self.subject = subject
#         self.sendgrid_client = SendGridAPIClient('your-sendgrid-api-key')

#     async def send_welcome(self, full_name):
#         message = Mail(
#             from_email='your-email@example.com',
#             to_emails=self.recipient_email,
#             subject=self.subject,
#             html_content=f"<strong>Welcome {full_name}!</strong>"
#         )
#         try:
#             response = await self.sendgrid_client.send(message)
#             print(response.status_code)
#             print(response.body)
#             print(response.headers)
#         except Exception as e:
#             print(e.message)
