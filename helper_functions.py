
import win32com.client as win32
def CreateDraftEmail(send_to, send_cc, subject, email_body):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = send_to
    mail.Cc = send_cc
    mail.Subject = subject
    textt=r"Need to enter the Wis here"
    image_cid = "image_cid"  # Content ID for the embedded image
    Stream_name="Amon_MosNA_Win10_PreInt"
    mail.HTMLBody = f"""<html><head><title>Delivery Report</title></head>
    <body><p>Dear All,</p><p>I have delivered the following items to the {Stream_name}:</p>
    {textt}
    <p>Regards,</p>
    </body>
    </html>"""
    mail.save()

