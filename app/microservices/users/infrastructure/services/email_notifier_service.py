from __future__ import annotations
from typing import Iterable, List, Optional, Union, Tuple
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.microservices.users.domain.interfaces.services.i_email_notifier_service import IEmailNotifierService


conf = ConnectionConfig(
)


def _as_list(value: Optional[Union[str, Iterable[str]]]) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


class EmailNotifierService(IEmailNotifierService):
    """
    Servicio de envío de correos basado en FastAPI-Mail (sin adjuntos).
    Requisitos:
      - ConnectionConfig con TEMPLATE_FOLDER apuntando a su carpeta de plantillas Jinja2.
      - MAIL_FROM, servidor SMTP y credenciales configurados.
    """

    def __init__(self):
        self.mailer = FastMail(conf)

    async def prepared_email(
        self,
        title: str,
        content: Union[str, dict],
        to: list,
        cc: Optional[Iterable[str]] = None,
        template: Optional[str] = None,
    ) -> Tuple[MessageSchema, Optional[str]]:
        """
        Si 'template' es None => 'content' debe ser str (HTML directo).
        Si 'template' tiene valor => 'content' debe ser dict (contexto Jinja2).
        Retorna (message, template_name).
        """
        recipients = _as_list(to)
        cc_list = _as_list(cc)

        if template:
            if not isinstance(content, dict):
                raise TypeError("Con 'template', 'content' debe ser dict (contexto Jinja2).")
            message = MessageSchema(
                subject=title,
                recipients=recipients,
                template_body=content,
                subtype="html",
            )
            return message, template

        if not isinstance(content, str):
            raise TypeError("Sin 'template', 'content' debe ser str (HTML).")
        message = MessageSchema(
            subject=title,
            recipients=recipients,
            cc=cc_list or None,
            body=content,
            subtype="html",
        )
        return message, None

    async def send_email(
        self,
        template: Optional[str],
        title: str,
        to: list,
        content: Union[dict, str],
        send: bool = True,
        cc: Optional[Iterable[str]] = None,
    ):
        """
        Construye el mensaje mediante 'prepared_email' y luego envía.
        - Con 'template' => render Jinja2 (content: dict)
        - Sin 'template' => HTML directo (content: str)
        """
        message, tpl = await self.prepared_email(
            title=title,
            content=content,
            to=to,
            cc=cc,
            template=template,
        )

        if not send:
            return message  # útil para pruebas

        if tpl:
            await self.mailer.send_message(message, template_name=tpl)
        else:
            await self.mailer.send_message(message)

        return {"status": "sent", "recipients": _as_list(to), "cc": _as_list(cc)}
