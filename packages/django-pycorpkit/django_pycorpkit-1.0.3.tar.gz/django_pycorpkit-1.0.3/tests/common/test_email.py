from unittest.mock import patch

from django.conf import settings

from pycorpkit.common.utils.email import send_email_asynchronously


@patch("pycorpkit.common.utils.email.EmailMultiAlternatives")
def test_send_email(mock_email_multi_alternatives):
    subject = "Test Subject"
    plain_text = "Test Plain Text"
    html_message = "<p>Test HTML Message</p>"
    recipients = ["recipient@example.com"]
    attachments = [("test.txt", "Test content", "text/plain")]
    bcc = ["bcc@example.com"]
    cc = ["cc@example.com"]

    send_email_asynchronously(
        subject=subject,
        plain_text=plain_text,
        html_message=html_message,
        recipients=recipients,
        attachments=attachments,
        bcc=bcc,
        cc=cc,
    )

    mock_email_multi_alternatives.assert_called_once_with(
        subject=subject,
        body=plain_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
        bcc=bcc,
        cc=cc,
        alternatives=[(html_message, "text/html")],
    )
    mock_email_instance = mock_email_multi_alternatives.return_value
    mock_email_instance.attach.assert_called_once_with(
        "test.txt", "Test content", "text/plain"
    )
    mock_email_instance.send.assert_called_once()


@patch("pycorpkit.common.utils.email.EmailMultiAlternatives")
def test_send_email_no_html(mock_email_multi_alternatives):
    subject = "Test Subject"
    plain_text = "Test Plain Text"
    recipients = ["recipient@example.com"]

    send_email_asynchronously(
        subject=subject,
        plain_text=plain_text,
        recipients=recipients,
    )

    mock_email_multi_alternatives.assert_called_once_with(
        subject=subject,
        body=plain_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
        bcc=None,
        cc=None,
        alternatives=None,
    )
    mock_email_instance = mock_email_multi_alternatives.return_value
    mock_email_instance.send.assert_called_once()
