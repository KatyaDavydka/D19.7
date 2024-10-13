# from django.conf import settings
# from django.core.mail import mail_managers, EmailMultiAlternatives
# from django.template.loader import render_to_string
# from protect.models import User
#
#
# def send_notifications(preview, pk, header):
#     users = User.objects.values_list('email', flat=True)
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}/doska_ob/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=header,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=users,
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
