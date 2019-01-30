import win32com.client as win32
import config


outlook = win32.Dispatch('output.application')
mail = outlook.CreateItem(0)
mail.To = config.mail_to
mail.Subject = config.mail_subject
mail.Body = config.mail_body
# mail.HTMLBody = '<h2>Testing Python Code</h2>' #this field is optional

# To attach a file to the email 
attachment  = config.mail_attach
mail.Attachments.Add(attachment)

mail.Send()