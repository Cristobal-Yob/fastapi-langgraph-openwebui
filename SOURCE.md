# Procedencia

La base procede del starter local FastAPI/LangGraph revisado el 27 de octubre de 2026. Se copian únicamente fuentes allowlisted; no historial Git, configuración privada, entornos ni estado de cuentas.

Open WebUI usa SQLite local en `.runtime/openwebui/webui.db`, con directorio privado e ignorado por Git. El arranque genera DATA_DIR y una URL SQLite absoluta cuando DATABASE_URL falta o está vacía. No necesita configurar una URL de base de datos. Cuentas, historial y Pipe son locales; Heroku puede perderlos al reiniciar/deploy. Use una instancia/worker/dyno y conserve la clave de autenticación; no habilite registro público.

Hashes SHA-256 de la base:

```json
{
  "graph.py": "aaa18441525fd8d9c4ed8ad43c2551e5349f9756ad449bbc52ec80341e979b8a",
  "prompts.py": "67806e3ff5656a3933c22c9d556fdafa0e1dd511f6a60d26e700ba23a3cff783",
  "provider.py": "0b4a2851c9ffaf6968868920f04258e45f90ced8dceda4d6b5d082dfa0fffb9e",
  "memory.py": "002ce0bbe03f18d1e38c14dea7205f6b78aa3397de885d33da8c8bddc14819bf"
}
```

El origen queda intacto y no es una dependencia runtime. No se han copiado credenciales, contenido del usuario, audios, registros ni carpetas privadas. Esta preparación no prueba entrega real.

La instalación pip-target del host es una adaptación basada en la lista slim exacta del tag oficial, no una ruta pip slim oficialmente documentada. Véanse [procedencia y licencia](webui/UPSTREAM.md).
