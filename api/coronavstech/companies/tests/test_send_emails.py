from django.core import mail
from django.test import TestCase, override_settings, Client
from unittest.mock import patch
from django.shortcuts import reverse



class EmailUnitTest(TestCase):
    """Test class for testing sending emails."""

    # @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email_success(self) -> None:
        """Test sending email is successful."""

        self.assertEqual(len(mail.outbox), 0)

        with self.settings(
                EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
        ):
            mail.send_mail(
                subject='Hi there!',
                message='Test message',
                from_email='test@email.com',
                recipient_list=['testuser@email.com'],
                fail_silently=False
            )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Hi there!')
        self.assertEqual(mail.outbox[0].body, 'Test message')
        self.assertEqual(mail.outbox[0].from_email, 'test@email.com')
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], 'testuser@email.com')

    def test_send_email_with_no_args(self) -> None:
        """Test posting send email url with no args should send an empty email."""
        client = Client()
        with patch("companies.views.send_mail") as mocked_sendmail:

            payload = {"subject": "Hi",
                       "message": "Hey"}
            res = client.post(path='/send-email/', payload=payload)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data['status'], 'success')
            self.assertEqual(res.data['info'], 'email sent successfully')

            mocked_sendmail.assert_called_with(
                subject=None,
                message=None,
                from_email='sandboxsandbox77@gmail.com',
                recipient_list=['dchestnyh21@gmail.com'],
            )

    def test_send_email_get_request_not_allowed(self) -> None:
        """Test get request is not allowed for send email page."""
        client = Client()
        url = reverse('send_email')
        res = client.get(url)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.data['detail'], "Method \"GET\" not allowed.")

