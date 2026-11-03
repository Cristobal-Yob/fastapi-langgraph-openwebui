# Configuración específica

Este repositorio ejecuta el **servidor Open WebUI real**, no solamente un Pipe. Su versión fija requiere `langchain-core==1.4.8`, incompatible con el proveedor Google actual del core. `bin/post_compile` instala en `.webui-packages` la lista slim exacta del tag oficial y luego el wheel fijado con --no-deps, sin reintroducir Torch, sentence-transformers ni ONNX. Esta combinación pip-target es una adaptación de este proyecto basada en fuentes upstream, no una instalación pip slim oficialmente documentada. No hay shebangs ni enlaces a rutas temporales; no se instala nada en otro proyecto. Consulte [procedencia, hashes y licencia](webui/UPSTREAM.md). La orden pública es `python -B -m cloud.webui_entry serve --host 0.0.0.0 --port $PORT`; el core usa 127.0.0.1:18080. Para ejecución local mantenga las dependencias de la interfaz fuera del entorno del grafo. Desde esta carpeta, en PowerShell, cree el entorno separado solo si todavía no existe:

```powershell
if (Test-Path -LiteralPath .webui-venv) { throw 'Revise el entorno existente antes de modificarlo.' }
py -3.12 -m venv .webui-venv
& .\.webui-venv\Scripts\python.exe -m pip install -r webui/requirements-slim.txt
& .\.webui-venv\Scripts\python.exe -m pip install --no-deps -r webui/requirements.txt
$env:OPENWEBUI_PACKAGE_DIR = (Resolve-Path .\.webui-venv\Lib\site-packages).Path
```

Esta preparación de paquetes no levanta la interfaz ni valida su HTTPS o autenticación. [La guía de creación](CREAR_AGENTE.md) comprueba únicamente el core FastAPI; el adaptador completo se despliega después con [HEROKU.md](HEROKU.md). `cloud.webui_entry` usa `OPENWEBUI_PACKAGE_DIR` para localizar esos paquetes en su proceso separado cuando se realiza una validación completa específica de la plataforma. No instale la dependencia completa de Open WebUI dentro del entorno del grafo ni omita `--no-deps`: el orden reproduce la instalación slim de `bin/post_compile`. En Heroku ese hook crea `.webui-packages` durante el build; no suba `.webui-venv` ni configure allí una ruta local de Windows. Estos comandos no sustituyen una validación real de instalación y arranque en su plataforma.

Configure `WEBUI_SECRET_KEY`, `WEBUI_ADMIN_EMAIL` y `WEBUI_ADMIN_PASSWORD` (mínimo 20 caracteres). El registro permanece cerrado. Tras el acceso administrador, cree en Administración > Funciones un Pipe con su propio `cloud/pipe.py`, exclusivo del operador. Open WebUI usa SQLite local en `.runtime/openwebui/webui.db`, con directorio privado e ignorado por Git. El arranque genera DATA_DIR y una URL SQLite absoluta cuando DATABASE_URL falta o está vacía. No necesita configurar una URL de base de datos. Cuentas, historial y Pipe son locales; Heroku puede perderlos al reiniciar/deploy. Use una instancia/worker/dyno y conserve la clave de autenticación; no habilite registro público.

## Variables gestionadas por el arranque

Configure solo las ocho comunes más `DATABASE_URL`, `WEBUI_SECRET_KEY`, `WEBUI_ADMIN_EMAIL`
y `WEBUI_ADMIN_PASSWORD` de su `.env.example`. `cloud/run.py` fuerza autenticación,
registro cerrado, APIs externas desactivadas, cookies seguras, CORS desde `PUBLIC_ORIGIN`
y modo slim/sin descargas. No repita esos controles como variables del usuario.
`OPENWEBUI_PACKAGE_DIR` se usa únicamente como sustitución local de la ubicación de paquetes;
no es una Config Var requerida en Heroku.
