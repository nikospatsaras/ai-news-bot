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

        # SVG icons (official brand logos)
        facebook_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#ffffff" xmlns="http://www.w3.org/2000/svg"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>'

        instagram_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#ffffff" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>'

        linkedin_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#ffffff" xmlns="http://www.w3.org/2000/svg"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'

        viber_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#ffffff" xmlns="http://www.w3.org/2000/svg"><path d="M11.4 0C9.473.028 5.333.344 3.02 2.467 1.302 4.187.696 6.7.633 9.817c-.063 3.117-.138 8.962 5.497 10.547v2.42s-.038.972.602 1.17c.78.241 1.227-.5 1.97-1.299L9.94 21.05c3.86.323 6.823-.42 7.16-.527.781-.252 5.196-.818 5.913-6.677.74-6.042-.36-9.853-2.34-11.583l-.011-.005C20.067.752 17.077.121 14.166.082c0 0-.215-.014-.733-.018C13.07.06 12.738.054 12.391.05 12.044.045 11.733.038 11.43.034c-.01-.001-.02-.001-.031-.001zm.027 1.685c.276.003.546.009.798.013.479.007.728.018.728.018 2.587.035 5.245.598 6.49 1.756 1.756 1.523 2.628 5.04 2.025 10.196-.601 5.135-4.34 5.557-4.997 5.762-.293.092-2.882.74-6.135.516 0 0-2.43 2.93-3.19 3.692-.117.117-.255.165-.346.144-.13-.032-.165-.184-.165-.4l.024-4.005C.97 17.62 1.275 12.683 1.328 10.099c.063-2.604.561-4.738 1.93-6.084 1.95-1.832 5.42-2.097 7.045-2.18 0 0 .206-.151 1.105-.151h.019zm6.005 2.815c-.244 0-.443.198-.443.443 0 .245.199.443.443.443.245 0 .443-.198.443-.443 0-.245-.198-.443-.443-.443zm-2.92.207c-.295 0-.534.239-.534.534 0 .294.239.533.534.533 1.957.029 3.476.667 4.514 1.838 1.06 1.193 1.596 2.835 1.49 4.793-.014.295.213.546.508.56h.025c.288 0 .526-.225.54-.514.122-2.281-.555-4.288-1.876-5.78-1.32-1.495-3.273-2.376-5.193-2.483zm-1.45 1.788c-.342-.007-.341.514-.004.522 2.451.019 4.471 1.69 4.493 4.755.003.344.527.34.524-.004h-.001c-.025-3.327-2.293-5.235-5.012-5.273zm-3.78.392a.898.898 0 00-.622.27h-.001c-.567.574-.728 1.395-.444 2.31C7.62 9.342 9.83 11.86 12.555 13.4c1.94 1.099 3.084 1.34 3.776 1.012.626-.296.978-.952.984-1.518a.583.583 0 00-.27-.503c-.397-.275-1.011-.66-1.435-.886-.385-.207-.69-.064-.866.18l-.371.467c-.19.232-.539.2-.555.2-1.27-.329-2.448-.984-3.385-1.913-.965-.958-1.541-1.985-1.748-2.625-.054-.169-.045-.385.142-.575l.46-.473c.205-.207.31-.493.115-.876-.286-.564-.665-1.222-.948-1.602a.605.605 0 00-.487-.232z"/></svg>'

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

                /* --- MODERN FOOTER WITH SVG ICONS --- */
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
                .social-icon svg {{ vertical-align: middle; }}
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

                <!-- Modern Footer with SVG icons -->
                <div class="footer">
                    <div class="social-icons">
                        <a href="https://www.facebook.com/nikoslaospatsaras/" class="social-icon" title="Facebook">{facebook_svg}</a>
                        <a href="https://www.instagram.com/nikospatsaras/" class="social-icon" title="Instagram">{instagram_svg}</a>
                        <a href="https://www.linkedin.com/in/nikolaos-patsaras/" class="social-icon" title="LinkedIn">{linkedin_svg}</a>
                        <a href="https://invite.viber.com/?g2=AQAuZ8nuvPdi11XROm9N2PgkZkVBGi%2BV6LPRSYKJC%2BpR%2BhiReinEPvDP8zLI5oC%2B" class="social-icon" title="Viber Community">{viber_svg}</a>
                    </div>

                    <p class="brand-name">Νίκος Πατσαράς</p>
                    <p class="tagline">AI Briefing — Καθημερινή ενημέρωση για επαγγελματίες της αισθητικής</p>

                    <div class="quick-links">
                        <a href="https://nikospatsaras.gr">Website</a>
                        <span style="color:#ccc;">|</span>
                        <a href="https://invite.viber.com/?g2=AQAuZ8nuvPdi11XROm9N2PgkZkVBGi%2BV6LPRSYKJC%2BpR%2BhiReinEPvDP8zLI5oC%2B">Viber Community</a>
                    </div>

                    <p class="copyright">© {current_year} Νίκος Πατσαράς · All rights reserved<br>nikospatsaras.gr</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
