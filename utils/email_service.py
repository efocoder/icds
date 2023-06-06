from django.core.mail import send_mail


def send_email(receiver, status='success', codes=None, error=None):
    subject = 'Uploaded successfully'

    if status == 'failed':
        subject = "Failed to upload"

    msg = f'Your icd codes have been added successfully. Total codes is {len(codes)}'

    if status == 'failed':
        msg = f'Sorry we could not add your icd codes.\nError{error}'

    sender = 'dev@test.com'

    send_mail(subject, msg, sender, [receiver])
