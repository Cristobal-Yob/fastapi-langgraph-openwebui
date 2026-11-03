# Persistencia opcional: fuera del recorrido básico

Open WebUI usa SQLite local en `.runtime/openwebui/webui.db`, con directorio privado e ignorado por Git. El arranque genera DATA_DIR y una URL SQLite absoluta cuando DATABASE_URL falta o está vacía. No necesita configurar una URL de base de datos. Cuentas, historial y Pipe son locales; Heroku puede perderlos al reiniciar/deploy. Use una instancia/worker/dyno y conserve la clave de autenticación; no habilite registro público.

## Antes de ampliar

1. Mantenga el ejemplo básico en una sola instancia. No añada PostgreSQL para probar el agente.
2. Si necesita sobrevivir reinicios, diseñe y pruebe una ampliación con almacenamiento externo y permisos propios.
3. Para efectos externos, la reserva debe ser atómica antes del efecto; un resultado incierto nunca autoriza reenvío automático.
4. Pruebe caídas, concurrencia, recuperación y eliminación de datos con información sintética antes de usar cuentas reales.

Esta carpeta no incluye un backend PostgreSQL activo ni promete coordinación distribuida.
La implementación anterior se conserva en el archivo de fuentes del mantenedor, no en el paquete básico.
No copiar una URL de base de datos crea ese backend ni migra registros. No se contratan servicios desde app.json.
Nunca publique credenciales, bases SQLite, archivos Signal o registros de acciones.

Open WebUI admite bases externas como ampliación upstream; requieren instalar y revisar sus dependencias opcionales, migración y permisos por separado. Cambiar DATABASE_URL no migra datos.

[Volver a la configuración del canal](CONFIGURACION.md).

[SQLite y opciones de escalado upstream](https://docs.openwebui.com/getting-started/advanced-topics/scaling/). No modifique DATA_DIR a una carpeta pública.
