from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "documentacion", "Entrega_Final_Felices_los_Pesos.pdf")
EV = os.path.join(ROOT, "evidencias")

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DV", FONT))
pdfmetrics.registerFont(TTFont("DVB", FONT_B))

NAVY = colors.HexColor("#17243A")
BLUE = colors.HexColor("#3266D5")
CYAN = colors.HexColor("#24B5A5")
ORANGE = colors.HexColor("#F59E42")
LIGHT = colors.HexColor("#F3F6FA")
MID = colors.HexColor("#D8E1EC")
TEXT = colors.HexColor("#273444")
GREEN = colors.HexColor("#2E9D67")
RED = colors.HexColor("#C94A4A")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleDV", fontName="DVB", fontSize=25, leading=31, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle(name="SubDV", fontName="DV", fontSize=12, leading=17, textColor=TEXT, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="H1DV", fontName="DVB", fontSize=18, leading=23, textColor=NAVY, spaceAfter=9))
styles.add(ParagraphStyle(name="H2DV", fontName="DVB", fontSize=12, leading=16, textColor=BLUE, spaceBefore=7, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyDV", fontName="DV", fontSize=8.8, leading=13, textColor=TEXT, spaceAfter=5))
styles.add(ParagraphStyle(name="SmallDV", fontName="DV", fontSize=7.1, leading=10, textColor=TEXT))
styles.add(ParagraphStyle(name="WhiteDV", fontName="DVB", fontSize=9, leading=12, textColor=colors.white, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="BoxDV", fontName="DV", fontSize=7.4, leading=10, textColor=TEXT, alignment=TA_CENTER))

def P(text, style="BodyDV"):
    return Paragraph(text, styles[style])

def bullets(items):
    return [P("• " + x) for x in items]

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(MID)
    canvas.line(18*mm, 13*mm, 192*mm, 13*mm)
    canvas.setFont("DV", 7)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(18*mm, 8*mm, "Felices los Pesos - Ecosistema de Automatización IA")
    canvas.drawRightString(192*mm, 8*mm, f"Página {doc.page}")
    canvas.restoreState()

def table(data, widths, header=True, font=7.2):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmd = [
        ("FONTNAME", (0,0), (-1,-1), "DV"),
        ("FONTSIZE", (0,0), (-1,-1), font),
        ("LEADING", (0,0), (-1,-1), font+3),
        ("GRID", (0,0), (-1,-1), 0.35, MID),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]
    if header:
        cmd += [("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("FONTNAME", (0,0), (-1,0), "DVB")]
    for r in range(1 if header else 0, len(data)):
        if r % 2 == 0:
            cmd.append(("BACKGROUND", (0,r), (-1,r), LIGHT))
    t.setStyle(TableStyle(cmd))
    return t

def screenshot(filename, max_w=174*mm, max_h=125*mm):
    path = os.path.join(EV, filename)
    im = PILImage.open(path)
    w, h = im.size
    scale = min(max_w/w, max_h/h)
    return Image(path, width=w*scale, height=h*scale)

def architecture_table():
    rows = [
        [P("1. DISPARO", "WhiteDV"), P("2. INGESTA Y MEMORIA", "WhiteDV"), P("3. FILTRO", "WhiteDV")],
        [P("Manual de prueba<br/>Diario 08:30", "BoxDV"), P("Airtable: inicio y fuente<br/>RSS Google News<br/>Historial de temas", "BoxDV"), P("Límite de noticias<br/>Deduplicación URL y semántica<br/>IF: hay candidatos", "BoxDV")],
        [P("4. RAZONAMIENTO IA", "WhiteDV"), P("5. CONTROL HUMANO", "WhiteDV"), P("6. CIERRE Y KPIs", "WhiteDV")],
        [P("Prompt dinámico<br/>GPT-4o-mini<br/>JSON estructurado<br/>Score ponderado", "BoxDV"), P("Guardar revisión<br/>Gmail Send and Wait<br/>Aprobar / Rechazar", "BoxDV"), P("Actualizar Airtable<br/>Estado final<br/>Dashboard KPIs<br/>Error workflow", "BoxDV")],
    ]
    t = Table(rows, colWidths=[57*mm]*3, rowHeights=[12*mm, 28*mm, 12*mm, 28*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY), ("BACKGROUND", (0,2), (-1,2), BLUE),
        ("BACKGROUND", (0,1), (-1,1), LIGHT), ("BACKGROUND", (0,3), (-1,3), colors.HexColor("#E9F7F4")),
        ("GRID", (0,0), (-1,-1), 1, colors.white), ("VALIGN", (0,0), (-1,-1), "MIDDLE")
    ]))
    return t

story = []

# Portada
story += [Spacer(1, 31*mm), P("ECOSISTEMA DE AUTOMATIZACIÓN IA<br/>AUTÓNOMO PARA NEGOCIOS", "TitleDV"),
          HRFlowable(width="68%", thickness=2, color=CYAN, spaceBefore=7, spaceAfter=13),
          P("Felices los Pesos - Radar Autónomo de Contenido Financiero", "SubDV"), Spacer(1, 18*mm),
          architecture_table(), Spacer(1, 18*mm),
          P("Proyecto final · AI Automation · Ramiro Ventura · 26 de septiembre de 2026", "SubDV"),
          Spacer(1, 8*mm), P("Stack: n8n + Airtable + OpenAI + Gmail", "H2DV"), PageBreak()]

# Resumen
story += [P("1. Resumen ejecutivo", "H1DV"),
          P("El Radar Autónomo de Contenido resuelve de punta a punta la detección, priorización, redacción y aprobación de noticias para la cuenta argentina Felices los Pesos. El flujo se ejecuta diariamente, consulta fuentes configurables, utiliza Airtable como memoria, puntúa candidatos con IA y detiene la publicación ante una decisión humana."),
          P("Caso de uso y resultado", "H2DV")]
story += bullets([
    "Problema: revisar manualmente noticias repetidas y convertirlas en contenido útil consume tiempo y produce duplicados.",
    "Solución: automatización diaria con ranking editorial ponderado, redacción estructurada y control humano previo al cierre.",
    "Salida: tema seleccionado, guion, caption, CTA, estado editorial, trazabilidad de ejecución y KPI.",
    "Tecnologías obligatorias: n8n, Airtable, OpenAI GPT-4o-mini y Gmail.",
])
story += [Spacer(1,5*mm), P("Criterios cubiertos", "H2DV"), table([
    ["Criterio", "Evidencia principal", "Estado"],
    ["Mapa de arquitectura", "Diagrama y capturas del workflow", "Cumplido"],
    ["Estructuras de datos", "Tablas relacionadas + contratos JSON", "Cumplido"],
    ["Optimización de costos", "Matriz de decisión y ahorro estimado", "Cumplido"],
    ["Seguridad y resiliencia", "HITL, validaciones y error workflow", "Cumplido"],
    ["Dashboard de control", "Vista pública de Airtable con KPIs", "Cumplido"],
], [48*mm, 95*mm, 28*mm]), PageBreak()]

# Arquitectura
story += [P("2. Mapa de arquitectura", "H1DV"), architecture_table(), Spacer(1,5*mm),
          P("Secuencia funcional", "H2DV")]
story += bullets([
    "El trigger diario evita consultas continuas y reduce operaciones innecesarias.",
    "La configuración y las fuentes se leen dinámicamente; no hay noticias hardcodeadas.",
    "Airtable registra cada ejecución y conserva fuentes, temas, contenidos y métricas.",
    "La IA recibe candidatos ya limitados y deduplicados; devuelve JSON y scores editoriales.",
    "Los umbrales impiden guardar contenido de baja afinidad o utilidad.",
    "Gmail Send and Wait bloquea el flujo hasta la aprobación o rechazo humano.",
    "El workflow FDP 01 Error Handler captura fallos de producción y los registra en KPIs.",
])
story += [Spacer(1,4*mm), screenshot("01_flujo_inicio.jpg", max_h=68*mm), P("Figura 1. Inicio, ingesta, deduplicación y selección con IA.", "SmallDV"), PageBreak(),
          P("2.1 Orquestación y rutas finales", "H1DV"), screenshot("02_flujo_hilt.jpg", max_h=78*mm),
          P("Figura 2. Persistencia, espera de aprobación y bifurcación aprobado/rechazado.", "SmallDV"), Spacer(1,4*mm),
          table([["Ruta", "Acción", "Destino"], ["Aprobado", "Marca contenido y ejecución como exitosa", "Airtable + KPI"], ["Rechazado", "Marca contenido y ejecución como rechazada", "Airtable + KPI"], ["Error", "Error Trigger independiente registra el incidente", "Dashboard KPIs"]], [35*mm, 88*mm, 48*mm]), PageBreak()]

# Datos
story += [P("3. Manual operativo de datos", "H1DV"),
          P("Airtable funciona como memoria persistente. Las relaciones evitan datos aislados: Ejecuciones vincula Temas, Contenidos y Dashboard KPIs; Contenidos referencia el Tema seleccionado."),
          table([
              ["Tabla", "Campos principales", "Relaciones / función"],
              ["Fuentes", "Nombre, URL RSS, activa, prioridad", "Configuración dinámica de entrada"],
              ["Ejecuciones", "Ejecución ID, workflow, inicio, fin, estado, error", "Nodo central; vincula Temas, Contenidos y KPIs"],
              ["Temas", "Título, URL, fuente, fecha, scores, decisión", "Historial editorial y deduplicación"],
              ["Contenidos", "Tema, ejecución, formato, gancho, guion, caption, CTA, estado", "Revisión, aprobación y trazabilidad"],
              ["Dashboard KPIs", "Registro, exitosa, error, generó, aprobado, tasas, costo", "Monitoreo de rendimiento y fallos"],
          ], [31*mm, 83*mm, 57*mm], font=6.7),
          P("Estados operativos", "H2DV"),
          P("Ejecuciones: En curso → Esperando aprobación → Exitosa / Rechazada. Ante fallos: Error. Contenidos: En revisión → Aprobado / Rechazado."),
          P("Reglas de operación", "H2DV")]
story += bullets([
    "URL normalizada en minúsculas, sin fragmentos y sin barra final.",
    "La idempotency_key evita procesar dos veces una misma URL.",
    "El historial de títulos ayuda a evitar acontecimientos repetidos publicados por medios distintos.",
    "Los campos de estado gobiernan las transiciones; las credenciales permanecen en n8n.",
])
story += [PageBreak(), P("3.1 Esquemas JSON de transferencia", "H1DV"),
          P("Entrada normalizada RSS → IA", "H2DV"),
          P("{ title, summary, url, normalized_url, published_at, source }", "BodyDV"),
          P("Respuesta IA → parser", "H2DV"),
          P("{ decision, title, summary, url, published_at, source, viralidad, afinidad, utilidad, urgencia, originalidad, justification, formato, gancho, guion, caption, cta, top_3_alternativas }"),
          P("Salida parser → Airtable", "H2DV"),
          P("Agrega score_total, top_3_resumen e idempotency_key. Convierte puntajes a números 0-100, serializa guion y normaliza la decisión."),
          table([
              ["Métrica", "Peso", "Uso"],
              ["Viralidad", "35%", "Crecimiento, cobertura mediática y potencial social"],
              ["Afinidad", "25%", "Ajuste a finanzas personales argentinas"],
              ["Utilidad", "20%", "Valor práctico para la audiencia"],
              ["Urgencia", "10%", "Vigencia y necesidad de publicar pronto"],
              ["Originalidad", "10%", "Diferenciación del enfoque"],
          ], [40*mm, 25*mm, 106*mm]),
          Spacer(1,4*mm), P("Fórmula: score_total = V×0,35 + A×0,25 + U×0,20 + Ur×0,10 + O×0,10.", "BodyDV"), PageBreak()]

# IA y costos
story += [P("4. Motor de IA y optimización de costos", "H1DV"),
          P("La implementación usa GPT-4o-mini porque la tarea combina clasificación, puntuación y redacción breve en JSON. La temperatura 0,3 reduce variabilidad y el límite de 3.500 tokens controla el máximo de salida."),
          table([
              ["Alternativa", "Entrada USD/1M", "Salida USD/1M", "Costo estimado/ejecución*", "Decisión"],
              ["GPT-4o-mini (actual)", "$0,15", "$0,60", "$0,0021", "Elegido: mejor relación costo/calidad"],
              ["GPT-5 mini", "$0,25", "$2,00", "$0,0055", "Escalamiento si se requiere más precisión"],
              ["GPT-5", "$1,25", "$10,00", "$0,0275", "Reservar para análisis crítico excepcional"],
              ["Batch API", "50% menor", "50% menor", "$0,00105 sobre actual", "Útil si deja de ser urgente"],
          ], [41*mm, 25*mm, 25*mm, 34*mm, 46*mm], font=6.4),
          P("*Supuesto conservador: 6.000 tokens de entrada y 2.000 de salida por ejecución. Los precios son referenciales y deben revisarse antes de producción.", "SmallDV"),
          P("Ahorro estimado", "H2DV")]
story += bullets([
    "Frente a GPT-5 mini, GPT-4o-mini reduce el costo estimado por ejecución aproximadamente 62%.",
    "Frente a GPT-5, la reducción estimada es aproximadamente 92%.",
    "A 30 ejecuciones mensuales, el consumo estimado de IA es USD 0,063 con GPT-4o-mini, frente a USD 0,825 con GPT-5.",
    "La limitación previa a 8-10 noticias y la deduplicación disminuyen tokens antes de invocar el modelo.",
])
story += [P("Fuente de referencia", "H2DV"),
          P("OpenAI API Pricing: https://openai.com/api/pricing/ . La página oficial informa además un ahorro del 50% para trabajos asincrónicos con Batch API."),
          Spacer(1,3*mm), screenshot("06_openai.jpg", max_h=78*mm),
          P("Figura 3. Nodo de IA configurado con prompt dinámico y GPT-4o-mini.", "SmallDV"), PageBreak()]

# Seguridad
story += [P("5. Seguridad, resiliencia y Human-in-the-loop", "H1DV"),
          table([
              ["Control", "Implementación", "Riesgo mitigado"],
              ["Minimización", "Solo título, resumen, URL, fecha y fuente", "Exposición innecesaria de datos"],
              ["Credenciales", "OAuth/API gestionadas por n8n; no se exportan secretos", "Filtración de claves"],
              ["JSON estructurado", "Modo json_object + parser defensivo", "Respuesta de IA inválida"],
              ["Conversión de tipos", "Puntajes limitados a 0-100", "Comparaciones número/texto"],
              ["Antiduplicados", "URL normalizada, historial e idempotency_key", "Bucles y republicación"],
              ["Umbrales", "IF antes de guardar contenido", "Acciones sobre material de baja calidad"],
              ["HITL", "Gmail Send and Wait con Aprobar/Rechazar", "Efecto metralleta"],
              ["Error workflow", "Error Trigger → registro Airtable", "Fallas silenciosas"],
          ], [34*mm, 82*mm, 55*mm], font=6.5),
          P("Human-in-the-loop", "H2DV"),
          P("El flujo crea el contenido como En revisión, marca Esperando aprobación y se pausa. Solo una respuesta humana habilita la ruta crítica. El rechazo conserva trazabilidad y evita cualquier acción posterior."),
          screenshot("04_hitl.jpg", max_h=79*mm),
          P("Figura 4. Nodo Gmail detenido en Waiting for input con opciones Aprobar/Rechazar.", "SmallDV"), PageBreak(),
          P("5.1 Gestión de errores", "H1DV"), screenshot("03_error_handler.jpg", max_h=86*mm),
          P("Figura 5. Workflow de error independiente y publicado.", "SmallDV"), Spacer(1,4*mm),
          P("Pruebas de camino infeliz", "H2DV")]
story += bullets([
    "Respuesta de IA sin top_3_alternativas: el parser detectó el faltante; luego se degradó el Top 3 a dato complementario para mantener disponibilidad.",
    "Actualización Airtable con ID inválido: la ejecución se detuvo y se corrigió el mapeo al ID creado por Registrar Inicio.",
    "Estas pruebas muestran fallos explícitos y recuperables, evitando cierres falsamente exitosos.",
    "Para producción, el workflow principal referencia el Error Handler y registra nodo, mensaje y momento del fallo.",
])
story += [PageBreak()]

# Evidencia
story += [P("6. Evidencias de ejecución", "H1DV"), screenshot("05_parser.jpg", max_h=105*mm),
          P("Figura 6. Parser ejecutado: decisión, score y contenido estructurado.", "SmallDV"), PageBreak(),
          P("6.1 Resultado editorial en Airtable", "H1DV"), screenshot("07_contenidos.png", max_h=80*mm),
          P("Figura 7. Contenidos generados y dos registros aprobados.", "SmallDV"), Spacer(1,5*mm),
          P("Enlace público: https://airtable.com/appxI2IKCoBWmPZQp/shre0HzEuc4gNljXr"), PageBreak(),
          P("7. Dashboard de control", "H1DV"),
          P("La vista pública expone únicamente métricas operativas: ejecución, resultado, error, contenido generado, aprobación, tasas y costo. No permite editar la base ni muestra credenciales."),
          screenshot("08_dashboard.png", max_h=73*mm),
          P("Figura 8. Dashboard filtrado a ejecuciones registradas.", "SmallDV"), Spacer(1,5*mm),
          table([
              ["KPI", "Definición", "Valor evidenciado"],
              ["Generó contenido", "1 cuando se crea contenido editorial", "1"],
              ["Fue aprobado", "1 cuando el HITL aprueba", "1"],
              ["Tasa de error", "Errores / ejecuciones", "0%"],
              ["Tasa de aprobación", "Aprobados / contenidos generados", "100%"],
              ["Costo USD", "Costo estimado por ejecución", "0,00 redondeado"],
          ], [45*mm, 90*mm, 36*mm]),
          Spacer(1,5*mm), P("Enlace público obligatorio", "H2DV"),
          P("https://airtable.com/appxI2IKCoBWmPZQp/shrCmCXdf2JFA3CHq"), PageBreak()]

# Pruebas y cierre
story += [P("8. Plan y registro de pruebas", "H1DV"),
          table([
              ["Prueba", "Escenario", "Resultado / evidencia"],
              ["1", "Ejecución con respuesta IA completa", "Parser y score estructurado"],
              ["2", "Aprobación humana", "Ruta aprobada y contenido Aprobado"],
              ["3", "Rechazo humano", "Ruta rechazada conservando registro"],
              ["4", "IA sin Top 3", "Error detectado; fallback implementado"],
              ["5", "ID Airtable inválido", "Fallo visible; expresión corregida"],
          ], [18*mm, 70*mm, 83*mm]),
          P("Checklist de seguridad", "H2DV")]
story += bullets([
    "Filtro contra duplicados y claves de idempotencia: implementado.",
    "Comparaciones numéricas normalizadas: implementado.",
    "Prompt dinámico con variables del sistema: implementado.",
    "Credenciales y claves fuera del repositorio: verificado.",
    "Punto de aprobación humana previo a acción crítica: implementado.",
    "Workflow independiente de errores: publicado.",
])
story += [P("Archivos técnicos", "H2DV"),
          P("Se adjuntan FDP_01_Radar_de_Contenido.json y FDP_01_Error_Handler.json. Los JSON pueden importarse en n8n, pero requieren conectar credenciales propias de Airtable y Gmail."),
          P("Conclusión", "H2DV"),
          P("El ecosistema integra las cuatro categorías tecnológicas obligatorias y ejecuta un proceso real de negocio de punta a punta. La combinación de memoria persistente, razonamiento estructurado, aprobación humana, registro de KPIs y manejo independiente de errores permite operar con bajo costo y trazabilidad."),
          Spacer(1,8*mm), P("Fin de la documentación", "SubDV")]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc = SimpleDocTemplate(OUT, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=19*mm,
                        title="Entrega Final - Felices los Pesos", author="Ramiro Ventura")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
