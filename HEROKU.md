# Publicar Open WebUI y Pipe propios desde cero

**Objetivo: Heroku Cedar con buildpacks clásicos y stack heroku-24. No se afirma compatibilidad Fir/CNB.** Las órdenes de esta guía son acciones futuras del propietario: no se ha creado ninguna app, add-on ni despliegue.

## 1. Preparar herramientas y cuentas

Necesita Python 3.12, Git, GitHub CLI, Heroku CLI y cuentas propias. Este proyecto es autónomo y debe publicarse en un repositorio GitHub **privado nuevo**, sin importar historial, entornos, `.env`, OAuth ni auth de ejemplos anteriores. Consulte [README](README.md) para entorno y pruebas.

## 2. Configurar el agente

Copie `.env.example` a `.env` solo localmente. Genere `AGENT_API_TOKEN` con `secrets.token_urlsafe(32)`. Elija Google Developer API con `GOOGLE_GENAI_USE_VERTEXAI=false` y una clave propia, o Vertex con proyecto/location y ADC configurado expresamente fuera de Git. No use variables/cuentas de otra aplicación. `MODELO` y `FALLBACK_MODEL` deben ser distintos. Las instrucciones y el fallback son los del agente fuente, sin un responder de demostración.

`PUBLIC_ORIGIN` debe ser la URL HTTPS exacta que obtenga para su app, sin slash final. La excepción de ejecución local es la API base en localhost; los controles de navegador seguros requieren HTTPS local con un proxy de confianza o un túnel **solo si usted lo autoriza**. No desactive la validación de Origin para probarlos.

## Preparación específica

Este repositorio ejecuta el **servidor Open WebUI real**, no solamente un Pipe. Su versión fija requiere `langchain-core==1.4.8`, incompatible con el proveedor Google actual del core. `bin/post_compile` instala en `.webui-packages` la lista slim exacta del tag oficial y luego el wheel fijado con --no-deps, sin reintroducir Torch, sentence-transformers ni ONNX. Esta combinación pip-target es una adaptación de este proyecto basada en fuentes upstream, no una instalación pip slim oficialmente documentada. No hay shebangs ni enlaces a rutas temporales; no se instala nada en otro proyecto. Consulte [procedencia, hashes y licencia](webui/UPSTREAM.md). La orden pública es `python -B -m cloud.webui_entry serve --host 0.0.0.0 --port $PORT`; el core usa 127.0.0.1:18080. Para ejecución local cree ese mismo venv e instale `webui/requirements.txt` (Windows: `.webui-venv/Scripts/python.exe -m pip install -r webui/requirements.txt`).

Defina PostgreSQL externo en `DATABASE_URL`, `WEBUI_SECRET_KEY` estable, `WEBUI_ADMIN_EMAIL` y `WEBUI_ADMIN_PASSWORD` de al menos 20 caracteres, en Config Vars. El registro público permanece desactivado. El servidor crea el administrador inicial con esas variables; use una base nueva y verifique que no contenga usuarios previos. No abra temporalmente el registro. Tras iniciar sesión, en Administración > Funciones cree una función Pipe pegando **su propio archivo** `cloud/pipe.py`, guarde y habilítela solo para el operador. El correo del usuario autenticado debe coincidir con el administrador configurado; no se acepta una identidad enviada por el navegador. La función y las cuentas se guardan en PostgreSQL. No habilite subida de archivos, RAG, conexiones externas ni registro: sus ficheros no tienen almacenamiento duradero configurado. Este tutorial cubre texto mediante Pipe, no toda la superficie multiusuario de Open WebUI. Verifique tamaño de slug, memoria y arranque con la instancia elegida antes de considerarlo apto: no se ha construido ni medido un slug Heroku aquí.

## 3. Verificar antes de publicar

```sh
python -B -m unittest discover -s tests -v
```

En WhatsApp añada `npm test`. Los tests de PostgreSQL se habilitan únicamente contra una base **sintética aislada** con `RUN_DATABASE_TESTS=true`, `DATABASE_URL` y `STATE_ENCRYPTION_KEY` de prueba. Los tests no deben tocar la cuenta/base real. El resultado omitido no equivale a una prueba de durabilidad.

## 4. Crear repositorio privado y app, con aprobación

Revise primero el contenido: solo código, tests, manifiestos y estas guías. No publique `.env`, claves, QR, sesiones, ledgers, uploads, entornos ni node_modules. Inicialice Git **dentro de esta carpeta nueva**, añada el allowlist revisado, haga un commit convencional y cree el repositorio privado mediante `gh repo create <su-organizacion>/<nombre> --private --source=. --remote=origin`. Empuje solo ese historial limpio tras su aprobación. No copie el `.git` original.

Cree explícitamente una aplicación **Cedar** en Heroku con stack `heroku-24`, no Fir. Asigne `heroku/python` como buildpack clásico. Su `Procfile` raíz ejecuta `web: python -B -m cloud.run`; no es un comando de desarrollo ni usa reload. `$PORT` lo lee el supervisor y el proceso público escucha en `0.0.0.0:$PORT`.

Complete las Config Vars desde un canal privado seguro, no desde un archivo versionado ni comandos que queden en capturas. Obtenga la URL real con `heroku apps:info --app <su-app>` y copie el campo Web URL (o web_url de la respuesta JSON), sin slash final, en PUBLIC_ORIGIN. No suponga que coincide con <nombre>.herokuapp.com: Heroku puede añadir un sufijo. Las dependencias están fijadas en los manifiestos. No hay add-ons automáticos: use únicamente un PostgreSQL externo previamente autorizado cuando corresponda. Verifique TLS y acceso restringido de esa base con su proveedor.

Solo después de revisar configuración, alcance y coste, conecte la app al repositorio privado y despliegue la rama elegida, o añada el remoto Heroku y haga el push manual aprobado. Escale a **un solo dyno web** y un solo proceso del core. No habilite autoscaling, workers extra ni despliegues automáticos antes de validar seguridad y presupuesto. El filesystem del dyno es efímero; no use SQLite para estado de seguridad.

## 5. Aceptación y operación

1. Consulte `/health`: debe responder sin datos privados. Verifique que una solicitud de chat/control sin autenticación sea rechazada.
2. Pruebe primero una consulta inocua con su propio operador. El cliente debe recibir 202 y consultar estado; no mantenga una petición bloqueada más de 30 segundos.
3. Solo si está autorizado, habilite por separado correo, pairing o sesión pagada y pruebe con destinatario/cuenta propios. Registre aceptación del proveedor separada de recepción humana o reproducción audiovisual.
4. Compruebe reinicio, reservas inciertas y limpieza con datos sintéticos antes de usar un proveedor real. Un restart borra memoria conversacional; **no** borra PostgreSQL.
5. Si hay incertidumbre, detenga operaciones y concilie. No reintente envíos ni creaciones ciegamente. Copias de seguridad y rotación de claves requieren preservar la capacidad de descifrar estado existente.

## Fuentes oficiales

- [Procfile](https://devcenter.heroku.com/articles/procfile), [Python y .python-version](https://devcenter.heroku.com/articles/python-runtimes).
- [Disco efímero y SQLite](https://devcenter.heroku.com/articles/sqlite3), [timeout HTTP](https://devcenter.heroku.com/articles/request-timeout), [apagado](https://devcenter.heroku.com/articles/dyno-shutdown-behavior).
- [Chainlit archivado](https://docs.chainlit.io/get-started/project-status), [Open WebUI](https://docs.openwebui.com/getting-started/quick-start/).

La entrega de estas fuentes no demuestra build Linux, tamaño de slug, rendimiento cloud ni integración con cuentas. Esas comprobaciones requieren un despliegue y autorización separados.
