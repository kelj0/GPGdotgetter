import random
import string
import smtplib

def generate_random_string(N):
    '''Returns random string of N chars long'''
    return ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits
            ) for _ in range(N)
        )

def sendConfirmationEmail(email,token):
    '''Sends email to validate email'''
    s = 'Please confirm your email by clicking on link: https://gpgdotgetter.com/api/emailValidator?token=%s' % token
    m = smtplib.SMTP_SSL('smtp.gmail.com',465)
    m.ehlo()
    m.login('email','password')
    m.sendmail('email', email, s)
    if m:
        print("Problems while sending email to %s!" % email)
    m.quit()

def allowed_file(filename,extensions):
    '''Returns true if file is valid to be uploaded'''
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in extensions

