import datetime

date = str(datetime.datetime.now().date())
app = 'outlook.application'
mail_to = 'shadab.shaikh@calibehr.com;vibhuti.kumar@calibehr.com'
mail_subject = 'Face-Recognition Logs'
mail_body = f'Please find attached logs for date: {date}.'
mail_attach = 'E:/MachineLearning/face-recognition/CGI/logs/mainlogs/mail.log'