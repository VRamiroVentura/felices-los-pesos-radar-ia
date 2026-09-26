# Felices los Pesos - Radar Autónomo de Contenido con IA

Proyecto final del curso AI Automation. El sistema releva noticias financieras argentinas, elimina duplicados, utiliza IA para seleccionar y redactar contenido, registra memoria en Airtable y solicita aprobación humana por Gmail antes de cerrar la ejecución.

## Arquitectura

- Orquestador: n8n.
- Base de datos y memoria: Airtable.
- Procesamiento IA: OpenAI GPT-4o-mini.
- Canal de salida y Human-in-the-loop: Gmail Send and Wait.
- Fuentes: RSS de Google News configuradas dinámicamente desde Airtable.
- Resiliencia: filtros, validación JSON, control de duplicados, umbrales editoriales y workflow independiente de errores.

## Archivos

- `documentacion/Entrega_Final_Felices_los_Pesos.pdf`: arquitectura, modelo de datos, JSON, costos, seguridad, resiliencia, pruebas y evidencias.
- `workflows/FDP_01_Radar_de_Contenido.json`: flujo principal de n8n.
- `workflows/FDP_01_Error_Handler.json`: workflow de errores.
- `evidencias/`: capturas del flujo, IA, HITL, error handler, contenidos y dashboard.

## Enlaces públicos

- Dashboard KPI: https://airtable.com/appxI2IKCoBWmPZQp/shrCmCXdf2JFA3CHq
- Contenidos: https://airtable.com/appxI2IKCoBWmPZQp/shre0HzEuc4gNljXr
- VIDEO YT: https://youtu.be/1sAPLxe6gLM

## Ejecución resumida

1. El trigger manual o diario inicia la ejecución.
2. n8n registra el inicio y consulta la fuente activa en Airtable.
3. Lee el RSS, limita volumen y consulta el historial.
4. Elimina URLs y acontecimientos duplicados.
5. GPT-4o-mini puntúa candidatos y redacta el contenido.
6. Los nodos de código validan JSON y recalculan el score ponderado.
7. Si supera los umbrales, se guarda como contenido en revisión.
8. Gmail detiene el flujo hasta que una persona aprueba o rechaza.
9. Airtable actualiza estado, ejecución y KPIs.
10. Un workflow independiente registra fallos de producción.

## Seguridad

El repositorio no incluye API keys, contraseñas ni tokens OAuth. El JSON exportado contiene solamente referencias internas a credenciales de n8n; quien importe el flujo debe conectar sus propias credenciales.

