"""Open WebUI Function: operator-only Pipe to the included asynchronous core."""
import hashlib
import os
from cloud.client import ask


class Pipe:
    def __init__(self): self.name = 'Autonomous LangGraph'

    async def pipe(self, body: dict, __user__: dict = None, __metadata__: dict = None,
                   __chat_id__: str = None, __task__: str = None):
        if __task__ or (__metadata__ or {}).get('task'): return ''
        user = __user__ or {}
        if user.get('email') != os.environ.get('WEBUI_ADMIN_EMAIL'):
            return 'Esta aplicación de enseñanza tiene un único operador autorizado.'
        chat = __chat_id__ or (__metadata__ or {}).get('chat_id')
        if not isinstance(chat,str) or not chat: return 'Abra una conversación guardada.'
        text = next((m.get('content') for m in reversed(body.get('messages',[])) if m.get('role') == 'user'),None)
        if not isinstance(text,str) or not 1 <= len(text.strip()) <= 2000: return 'Escriba entre 1 y 2000 caracteres.'
        session = 'webui-'+hashlib.sha256((str(user.get('id'))+'\0'+chat).encode()).hexdigest()[:48]
        try: return (await ask(text,session))['response']
        except Exception: return 'El agente no está disponible. No se reintentó automáticamente.'
