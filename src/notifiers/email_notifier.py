"""
Email notification module using Gmail SMTP
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime
from ..logger import setup_logger


logger = setup_logger(__name__)


class EmailNotifier:
    """Send email notifications with AI news digest using Gmail SMTP"""

    def __init__(
        self,
        gmail_address: Optional[str] = None,
        gmail_app_password: Optional[str] = None,
        email_to: Optional[str] = None,
    ):
        self.gmail_address = gmail_address or os.getenv("GMAIL_ADDRESS")
        self.gmail_app_password = gmail_app_password or os.getenv("GMAIL_APP_PASSWORD")
        self.email_to = email_to or os.getenv("EMAIL_TO")

        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        if not all([self.gmail_address, self.gmail_app_password, self.email_to]):
            logger.warning(
                "Gmail notifier not fully configured. "
                "Required: GMAIL_ADDRESS, GMAIL_APP_PASSWORD, EMAIL_TO"
            )
        else:
            logger.info(f"EmailNotifier initialized with Gmail SMTP (from: {self.gmail_address})")

    def send(self, content: str, subject: Optional[str] = None, language: str = "en") -> bool:
        if subject is None:
            today = datetime.now().strftime("%d/%m/%Y")
            subject = f"Καθημερινό AI Briefing — {today}"

        if not all([self.gmail_address, self.gmail_app_password, self.email_to]):
            logger.error("Gmail notifier is not fully configured. Skipping email send.")
            return False

        try:
            html_content = self._create_html_email(content, subject)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.gmail_address
            msg["To"] = self.email_to

            part1 = MIMEText(content, "plain", "utf-8")
            part2 = MIMEText(html_content, "html", "utf-8")
            msg.attach(part1)
            msg.attach(part2)

            logger.info(f"Sending email via Gmail SMTP to {self.email_to}")

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_address, self.gmail_app_password)
                recipients = [e.strip() for e in self.email_to.split(",")]
                server.sendmail(self.gmail_address, recipients, msg.as_string())

            logger.info("Email sent successfully via Gmail SMTP")
            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(
                f"Gmail authentication failed: {str(e)}. "
                "Make sure you're using an App Password, not your regular Gmail password."
            )
            return False
        except Exception as e:
            logger.error(f"Failed to send email via Gmail: {str(e)}", exc_info=True)
            return False

    def _create_html_email(self, content: str, subject: str) -> str:
        try:
            import markdown
            from markdown.extensions import nl2br, tables, fenced_code

            html_content = markdown.markdown(
                content,
                extensions=['nl2br', 'tables', 'fenced_code', 'sane_lists']
            )
        except ImportError:
            logger.warning("markdown library not installed, using basic HTML formatting")
            import html
            html_content = html.escape(content).replace('\n', '<br>\n')

        current_year = datetime.now().year

        # Social media icons from Simple Icons CDN (white versions)
        icon_style = 'width="20" height="20" style="vertical-align: middle; border: 0; display: inline-block;"'
        facebook_icon = f'<img src="https://cdn.simpleicons.org/facebook/ffffff" alt="Facebook" {icon_style}>'
        instagram_icon = f'<img src="https://cdn.simpleicons.org/instagram/ffffff" alt="Instagram" {icon_style}>'
        linkedin_icon = f'<img src="https://api.iconify.design/mdi:linkedin.svg?color=%23ffffff" alt="LinkedIn" {icon_style}>'
        viber_icon = f'<img src="https://cdn.simpleicons.org/viber/ffffff" alt="Viber" {icon_style}>'

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Helvetica, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.8;
                    color: #24292e;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f6f8fa;
                }}
                .container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    padding: 40px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                .title {{
                    color: #476fff;
                    font-size: 32px;
                    font-weight: 700;
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 4px solid #476fff;
                    text-align: center;
                }}
                .content {{ margin-top: 30px; }}
                .content h1 {{
                    color: #476fff;
                    font-size: 28px;
                    font-weight: 700;
                    margin-top: 40px;
                    margin-bottom: 20px;
                    padding-bottom: 12px;
                    border-bottom: 3px solid #476fff;
                }}
                .content h2 {{
                    color: #2c3e50;
                    font-size: 22px;
                    font-weight: 600;
                    margin-top: 35px;
                    margin-bottom: 18px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #e1e4e8;
                }}
                .content h3 {{
                    color: #24292e;
                    font-size: 18px;
                    font-weight: 600;
                    margin-top: 28px;
                    margin-bottom: 15px;
                    padding-left: 12px;
                    border-left: 4px solid #476fff;
                }}
                .content p {{ margin: 15px 0; line-height: 1.8; color: #24292e; }}
                .content ul, .content ol {{ margin: 15px 0; padding-left: 30px; }}
                .content li {{ margin: 10px 0; line-height: 1.8; }}
                .content strong {{ font-weight: 700; color: #476fff; }}
                .content em {{ font-style: italic; color: #586069; }}
                .content hr {{ border: none; border-top: 2px solid #e1e4e8; margin: 30px 0; }}
                .content a {{ color: #476fff; text-decoration: none; }}
                .content a:hover {{ text-decoration: underline; }}

                /* --- MODERN FOOTER WITH HOSTED ICONS --- */
                .footer {{
                    margin-top: 50px;
                    padding: 40px 20px 30px 20px;
                    border-top: 1px solid #e1e4e8;
                    text-align: center;
                    background-color: #fafbfc;
                    border-radius: 0 0 8px 8px;
                }}
                .social-icons {{ margin-bottom: 25px; }}
                .social-icon {{
                    display: inline-block;
                    width: 42px;
                    height: 42px;
                    line-height: 42px;
                    text-align: center;
                    border-radius: 50%;
                    background-color: #476fff;
                    text-decoration: none;
                    margin: 0 5px;
                }}
                .social-icon:hover {{ background-color: #2c4dc7; }}
                .brand-name {{
                    font-size: 18px;
                    font-weight: 700;
                    color: #24292e;
                    margin: 20px 0 8px 0;
                }}
                .tagline {{
                    color: #586069;
                    font-size: 14px;
                    margin: 0 0 25px 0;
                    font-style: italic;
                }}
                .quick-links {{ margin: 15px 0; font-size: 14px; }}
                .quick-links a {{
                    color: #476fff;
                    text-decoration: none;
                    font-weight: 600;
                    margin: 0 8px;
                }}
                .quick-links a:hover {{ text-decoration: underline; }}
                .copyright {{
                    color: #999;
                    font-size: 12px;
                    margin-top: 25px;
                    padding-top: 15px;
                    border-top: 1px solid #e1e4e8;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="title">{subject}</div>
                <div class="content">
                    {html_content}
                </div>

                <!-- Modern Footer with Hosted Icons -->
                <div class="footer">
                    <div class="social-icons">
                        <a href="https://www.facebook.com/nikoslaospatsaras/" class="social-icon" title="Facebook">{facebook_icon}</a>
                        <a href="https://www.instagram.com/nikospatsaras/" class="social-icon" title="Instagram">{instagram_icon}</a>
                        <a href="https://www.linkedin.com/in/nikolaos-patsaras/" class="social-icon" title="LinkedIn">{linkedin_icon}</a>
                        <a href="https://invite.viber.com/?g2=AQAuZ8nuvPdi11XROm9N2PgkZkVBGi%2BV6LPRSYKJC%2BpR%2BhiReinEPvDP8zLI5oC%2B" class="social-icon" title="Viber Community">{viber_icon}</a>
                    </div>

                    <p class="brand-name">Νίκος Πατσάρας</p>
                    <p class="tagline">AI Briefing — Καθημερινή ενημέρωση για επαγγελματίες της αισθητικής</p>

                    <div class="quick-links">
                        <a href="https://nikospatsaras.gr">Website</a>
                        <span style="color:#ccc;">|</span>
                        <a href="https://invite.viber.com/?g2=AQAuZ8nuvPdi11XROm9N2PgkZkVBGi%2BV6LPRSYKJC%2BpR%2BhiReinEPvDP8zLI5oC%2B">Viber Community</a>
                    </div>

                    <p class="copyright">© {current_year} Νίκος Πατσάρας · All rights reserved<br>nikospatsaras.gr</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
