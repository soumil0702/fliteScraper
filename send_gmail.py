# Script to send email to gmail a(cs)
def sendMail():
    import smtplib

    gmail_user = 'soumil.bharatendu@gmail.com'   #you can add more usernames by ["a.gmail.com","b.gmail.com"]
    #gmail_user = username  

    gmail_password = 'Bhole789!!'

    sent_from = gmail_user  
    to = ['soumil.bharatendu@gmail.com']  
    subject = 'OMG Super Important Message from Python'  
    body = "Hey, what's up? \n"

    message = 'subject: {}\n\n{}'.format(subject, body)

    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    #    server.sendmail(sent_from, to, email_text) # try this for sending the stuff in the email_text string
        server.sendmail(sent_from, to, message) 
        server.close()

        print ('Email sent!')
    except:  
        print ('Something went wrong...')

#sendMail()
def send_email_two(user, pwd, recipient, subject, body): #another version....works better, you can also suppply multiple recipeints in an array
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ("successfully sent the mail")
    except:
        print ("failed to send mail")

#recipient=["soumil.bharatendu@gmail.com","soumil0702@gmail.com"]
#recipient=["soumil.bharatendu@gmail.com"]

