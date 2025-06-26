# app/services/email_service.py

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config import settings
from app.schemas import User, Capsule

def send_email(to_email: str, subject: str, html_content: str):
    """
    Основная функция для отправки email через SendGrid.

    :param to_email: Email получателя.
    :param subject: Тема письма.
    :param html_content: HTML-содержимое письма.
    """
    if not settings.SENDGRID_API_KEY:
        print("SENDGRID_API_KEY не настроен. Пропуск отправки email.")
        return

    message = Mail(
        from_email=settings.EMAILS_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email отправлен на {to_email}. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при отправке email на {to_email}: {e}")

def send_capsule_reminder(user: User, capsule: Capsule):
    """
    Отправляет email-напоминание о капсуле знаний.
    """
    subject = f"🧠 Ваше напоминание: {capsule.title or 'Ваша капсула знаний'}"
    
    # Формируем красивое HTML-письмо
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; color: #333; }}
            .container {{ background-color: #ffffff; border: 1px solid #ddd; border-radius: 8px; padding: 30px; max-width: 600px; margin: auto; }}
            .header {{ font-size: 24px; font-weight: bold; color: #0d9488; margin-bottom: 20px; }}
            .content {{ font-size: 16px; line-height: 1.6; }}
            .footer {{ font-size: 12px; color: #777; margin-top: 30px; text-align: center; }}
            a {{ color: #0d9488; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Привет, это ваши "Капсулы Знаний"!</div>
            <div class="content">
                <p>Вы просили напомнить вам об этой идее:</p>
                <blockquote style="border-left: 4px solid #0d9488; padding-left: 15px; margin-left: 0; font-style: italic;">
                    {capsule.content}
                </blockquote>
                <p><strong>Источник:</strong> <a href="{capsule.source_url}">{capsule.source_url}</a></p>
                <p>Подумайте, как эта мысль актуальна для вас сегодня.</p>
            </div>
            <div class="footer">
                <p>Вы получили это письмо, потому что запланировали напоминание в сервисе "Капсулы Знаний".</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    send_email(to_email=user.email, subject=subject, html_content=html_content)

