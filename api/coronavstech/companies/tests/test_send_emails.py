from django.core import mail
from unittest.mock import patch
from django.shortcuts import reverse


def test_send_email_success(mailoutbox, settings) -> None:
    """Test sending email is successful."""

    assert len(mailoutbox) == 0

    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    mail.send_mail(
        subject="Hi there!",
        message="Test message",
        from_email="test@email.com",
        recipient_list=["testuser@email.com"],
        fail_silently=False,
    )
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Hi there!"


def test_send_email_with_no_args(client) -> None:
    """Test posting send email url with no args should send an empty email."""
    with patch("companies.views.send_mail") as mocked_sendmail:
        res = client.post(path="/send-email/")

        assert res.status_code == 200
        assert res.data["status"] == "success"
        assert res.data["info"] == "email sent successfully"
        mocked_sendmail.assert_called_with(
            subject=None,
            message=None,
            from_email="sandboxsandbox77@gmail.com",
            recipient_list=["dchestnyh21@gmail.com"],
        )


def test_send_email_get_request_not_allowed(client) -> None:
    """Test get request is not allowed for send email page."""
    url = reverse("send_email")
    res = client.get(url)

    assert res.status_code == 405
    assert res.data["detail"] == 'Method "GET" not allowed.'
