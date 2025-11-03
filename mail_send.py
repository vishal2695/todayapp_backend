import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# # Your Gmail credentials
# GMAIL_USER = 'honeybeeofficial2020@gmail.com'
# GMAIL_APP_PASSWORD = 'scrn idqr phta dybg'  # 16-character app password (no spaces)
# Your Gmail credentials
GMAIL_USER = 'regotpastoneaone@gmail.com'
GMAIL_APP_PASSWORD = 'wqmj cuji elct obgc'  # 16-character app password (no spaces)

# Email details
# to_email = 'rahul.akarniya@cinntra.com'
to_email = 'vishal.dubey@cinntra.com'
# to_email = 'honeybeeofficial2020@gmail.com'
subject = 'hello subject'
body = f'Your testing messages..!!'

# Create the email message
message = MIMEMultipart()
message['From'] = GMAIL_USER
message['To'] = to_email
message['Subject'] = subject

# Add plain text body
message.attach(MIMEText(body, 'plain'))

try:
    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.sendmail(GMAIL_USER, to_email, message.as_string())
    server.quit()
    # user.save()

    print("✅ Email sent successfully.")
except Exception as e:
    print("❌ Failed to send email:", str(e))