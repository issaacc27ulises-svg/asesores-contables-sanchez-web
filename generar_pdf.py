#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la Guía SAT 2026 Premium de Asesores Contables Sánchez.

Coloca en la misma carpeta:
    logo_profesional.png

Instala:
    pip install -r requirements.txt

Ejecuta:
    python generar_pdf.py
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

BASE = Path(__file__).resolve().parent
LOGO = BASE / "logo_profesional.png"
OUT = BASE / "Guia_SAT_2026_Asesores_Contables_Sanchez_Premium.pdf"
W, H = letter

GREEN = colors.HexColor("#075B4C")
GREEN2 = colors.HexColor("#0A7A64")
BLUE = colors.HexColor("#245FE5")
LIGHTBLUE = colors.HexColor("#EEF4FF")
LIGHTGREEN = colors.HexColor("#EAF6F2")
DARK = colors.HexColor("#243044")
MUTED = colors.HexColor("#607086")
BORDER = colors.HexColor("#D7E0EA")
SOFT = colors.HexColor("#F7F9FC")
WHITE = colors.white
GOLD = colors.HexColor("#C9A227")

# Fuente opcional: si no existe, usa Helvetica.
FONT, BOLD = "Helvetica", "Helvetica-Bold"
dejavu = Path("/usr/share/fonts/truetype/dejavu")
if (dejavu / "DejaVuSans.ttf").exists():
    pdfmetrics.registerFont(TTFont("DejaVuSans", str(dejavu / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", str(dejavu / "DejaVuSans-Bold.ttf")))
    FONT, BOLD = "DejaVuSans", "DejaVuSans-Bold"

body = ParagraphStyle("body", fontName=FONT, fontSize=9.2, leading=13.2, textColor=DARK, spaceAfter=5)
small = ParagraphStyle("small", fontName=FONT, fontSize=8.1, leading=11, textColor=DARK)
muted = ParagraphStyle("muted", fontName=FONT, fontSize=8.2, leading=11.5, textColor=MUTED)
h1 = ParagraphStyle("h1", fontName=BOLD, fontSize=16, leading=20, textColor=GREEN, spaceAfter=7)
h2 = ParagraphStyle("h2", fontName=BOLD, fontSize=11.5, leading=14, textColor=DARK, spaceAfter=5)
title = ParagraphStyle("title", fontName=BOLD, fontSize=25, leading=29, textColor=GREEN, spaceAfter=5)
sub = ParagraphStyle("sub", fontName=FONT, fontSize=11.5, leading=15, textColor=MUTED, spaceAfter=10)
white = ParagraphStyle("white", fontName=BOLD, fontSize=9.5, leading=12, textColor=WHITE)
white_center = ParagraphStyle("wc", fontName=BOLD, fontSize=16, leading=19, textColor=WHITE, alignment=TA_CENTER)
white_body = ParagraphStyle("wb", fontName=FONT, fontSize=9.2, leading=13, textColor=WHITE, alignment=TA_CENTER)
center = ParagraphStyle("center", parent=small, alignment=TA_CENTER)

def P(x, s=body):
    return Paragraph(x, s)

def bullet(x):
    return Paragraph("• " + x, ParagraphStyle("b", parent=body, leftIndent=9, firstLineIndent=-7))

def box(items, bg=WHITE, border=BORDER):
    t = Table([[items]], colWidths=[170*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg), ("BOX",(0,0),(-1,-1),0.6,border),
        ("LEFTPADDING",(0,0),(-1,-1),9), ("RIGHTPADDING",(0,0),(-1,-1),9),
        ("TOPPADDING",(0,0),(-1,-1),8), ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def section(n, name, desc=""):
    a = Table([[
        P(str(n), ParagraphStyle("n", fontName=BOLD, fontSize=11, textColor=WHITE, alignment=TA_CENTER)),
        P(name, ParagraphStyle("sn", fontName=BOLD, fontSize=12.5, textColor=WHITE))
    ]], colWidths=[11*mm,159*mm])
    a.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),GREEN), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),6), ("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),7), ("BOTTOMPADDING",(0,0),(-1,-1),7)
    ]))
    return [a, Spacer(1,2*mm), P(desc, muted)] if desc else [a, Spacer(1,3*mm)]

def table(headers, rows, widths):
    data = [[P("<b>"+h+"</b>", white) for h in headers]]
    data += [[P(str(c), small) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    cmd = [
        ("BACKGROUND",(0,0),(-1,0),GREEN2), ("GRID",(0,0),(-1,-1),0.45,BORDER),
        ("VALIGN",(0,0),(-1,-1),"TOP"), ("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6), ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6)
    ]
    for r in range(1,len(data)):
        cmd.append(("BACKGROUND",(0,r),(-1,r),WHITE if r%2 else SOFT))
    t.setStyle(TableStyle(cmd))
    return t

def info(title_, text_, bg=LIGHTBLUE, color=BLUE):
    return box([P(title_, ParagraphStyle("it", fontName=BOLD, fontSize=9.5, textColor=color, spaceAfter=3)), P(text_, small)], bg)

def two(left, right):
    t = Table([[left,right]], colWidths=[84*mm,84*mm])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),4)]))
    return t

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#FBFCFE"))
    canvas.rect(0,0,W,H,fill=1,stroke=0)
    canvas.setFillColor(GREEN)
    canvas.roundRect(14*mm,H-31*mm,W-28*mm,18*mm,5*mm,fill=1,stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(14*mm,H-31*mm,2*mm,18*mm,fill=1,stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont(BOLD,8.5); canvas.drawString(21*mm,H-21*mm,"ASESORES CONTABLES SÁNCHEZ")
    canvas.setFont(FONT,6.5); canvas.drawString(21*mm,H-26*mm,"Soluciones Contables & Fiscales")
    canvas.setStrokeColor(BORDER); canvas.line(14*mm,14*mm,W-14*mm,14*mm)
    canvas.setFillColor(MUTED); canvas.setFont(FONT,6.8)
    canvas.drawString(14*mm,9*mm,"Asesores Contables Sánchez · Manzanillo, Colima")
    canvas.drawRightString(W-14*mm,9*mm,f"Página {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(
    str(OUT), pagesize=letter, leftMargin=18*mm, rightMargin=18*mm,
    topMargin=38*mm, bottomMargin=19*mm,
    title="Guía SAT 2026 - Asesores Contables Sánchez",
    author="Asesores Contables Sánchez"
)
S = []

# PORTADA
if LOGO.exists():
    im = PILImage.open(LOGO)
    iw, ih = im.size
    scale = min((80*mm)/iw, (35*mm)/ih)
    logo = Image(str(LOGO), width=iw*scale, height=ih*scale)
    logo.hAlign = "CENTER"
    lc = Table([[logo]], colWidths=[84*mm])
    lc.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),WHITE),("BOX",(0,0),(-1,-1),0.7,BORDER),
                            ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
                            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    S += [Spacer(1,7*mm),lc]
else:
    S += [Spacer(1,10*mm)]

S += [Spacer(1,7*mm), P("GUÍA SAT 2026",title),
      P("Una guía sencilla para entender y poner en orden tus obligaciones fiscales.",sub),
      HRFlowable(width="100%",thickness=1,color=GOLD,spaceAfter=5*mm),
      info("¿PARA QUIÉN ES ESTA GUÍA?",
           "Para emprendedores, pequeños negocios y personas que quieren entender sus obligaciones fiscales sin necesidad de conocer contabilidad avanzada."),
      Spacer(1,5*mm), P("Checklist rápido",h1),
      table(["QUÉ REVISAR","¿QUÉ SIGNIFICA?"],[
          ("RFC y régimen fiscal","Verifica que tus datos y régimen correspondan a tu actividad."),
          ("e.firma","Revisa su vigencia y conserva tus archivos de forma segura."),
          ("CSD","Certificado necesario para emitir facturas electrónicas."),
          ("CFDI","Comprueba que tus facturas tengan los datos correctos."),
          ("Declaraciones","Confirma que tus obligaciones estén presentadas."),
          ("Buzón Tributario","Revisa periódicamente avisos y mensajes."),
          ("Comprobantes","Conserva facturas de compras, gastos y operaciones.")
      ],[55*mm,115*mm]), Spacer(1,5*mm),
      info("IMPORTANTE",
           "Esta guía es informativa. Las obligaciones pueden variar según el régimen, actividad y situación de cada contribuyente.",LIGHTGREEN,GREEN),
      PageBreak()]

# E.FIRMA
S += section(1,"e.firma: tu identificación digital ante el SAT",
             "La e.firma permite realizar diversos trámites y servicios fiscales por internet.")
S += [info("¿QUÉ ES LA e.firma?",
            "Es un conjunto de archivos digitales que funciona como firma electrónica. No es lo mismo que tu contraseña del SAT. Guarda los archivos de manera segura."),
      Spacer(1,4*mm), P("¿Qué hacer según tu situación?",h2),
      table(["SITUACIÓN","QUÉ HACER"],[
          ("Primera vez","Acude al SAT con los requisitos que correspondan: identificación, comprobante de domicilio y medio de almacenamiento, entre otros."),
          ("Renovación vigente","Si tu e.firma está vigente, revisa las opciones electrónicas de renovación disponibles y sigue el procedimiento indicado por el SAT."),
          ("e.firma vencida","Revisa si tu situación permite una renovación en línea o si necesitas acudir al SAT.")
      ],[43*mm,127*mm]), Spacer(1,5*mm),
      two(box([P("Archivos importantes",h2),bullet("<b>.CER</b> — certificado público."),bullet("<b>.KEY</b> — llave privada."),bullet("Contraseña de la llave privada."),bullet("Copia de respaldo.")]),
          box([P("Seguridad",h2),P("No compartas tu archivo .KEY ni su contraseña. Trátalos como información confidencial.",small)],LIGHTBLUE)),
      Spacer(1,5*mm),info("SEÑAL DE ALERTA",
          "Si no puedes realizar trámites o firmar electrónicamente, revisa la vigencia de tu e.firma y certificados.",colors.HexColor("#FFF7E6"),colors.HexColor("#A56A00")),
      PageBreak()]

# CFDI
S += section(2,"Facturación electrónica CFDI 4.0",
             "Facturar correctamente ayuda a comprobar tus ingresos y gastos y a mantener orden fiscal.")
S += [P("Datos básicos que debes revisar",h2),
      table(["QUÉ REVISAR","EXPLICACIÓN"],[
          ("RFC","Debe capturarse correctamente."),
          ("Nombre / razón social","Debe coincidir con la información fiscal proporcionada."),
          ("Código postal","Corresponde al domicilio fiscal registrado."),
          ("Régimen fiscal","Selecciona el régimen que corresponda al receptor."),
          ("Uso de CFDI","Indica el uso que tendrá la factura."),
          ("CSD","Certificado necesario para emitir CFDI.")
      ],[55*mm,115*mm]), Spacer(1,5*mm), P("PUE y PPD explicado fácil",h2),
      table(["CONCEPTO","EXPLICACIÓN SENCILLA"],[
          ("PUE","Pago en una sola exhibición."),
          ("PPD","Pago en parcialidades o diferido."),
          ("Complemento de pago","Se utiliza cuando una factura PPD es pagada posteriormente, cuando corresponda.")
      ],[43*mm,127*mm]), Spacer(1,5*mm),
      two(box([P("Antes de emitir",h2),bullet("Confirma datos del cliente."),bullet("Revisa precio e impuestos."),bullet("Verifica PUE o PPD."),bullet("Conserva XML y PDF.")]),
          box([P("Después de emitir",h2),bullet("Revisa que no existan errores."),bullet("Conserva el XML."),bullet("Verifica el estatus cuando sea necesario."),bullet("Relaciona pagos cuando corresponda.")],LIGHTGREEN)),
      Spacer(1,5*mm),info("TIP PARA NEGOCIOS PEQUEÑOS",
          "Haz una revisión semanal de ingresos, compras y gastos en lugar de esperar hasta el cierre del mes."),
      PageBreak()]

# RESICO
S += section(3,"RESICO: entender el régimen sin complicaciones",
             "La tasa de ISR se determina conforme a los ingresos y a las reglas aplicables.")
S += [info("¿QUÉ DEBES ENTENDER?",
            "No confundas la tabla mensual con el cálculo anual. Primero debe confirmarse que el contribuyente cumple los requisitos del régimen."),
      Spacer(1,4*mm),P("Tabla mensual de referencia",h2),
      table(["INGRESOS MENSUALES HASTA","TASA","EJEMPLO ISR"],[
          ("$25,000.00","1.00%","$250.00"),
          ("$50,000.00","1.10%","$550.00"),
          ("$83,333.33","1.50%","$1,250.00"),
          ("$208,333.33","2.00%","$4,166.66"),
          ("$291,666.67","2.50%","$7,291.66")
      ],[70*mm,35*mm,65*mm]), Spacer(1,3*mm),
      P("Los ejemplos son ilustrativos. El cálculo real depende de la situación fiscal y de las disposiciones vigentes.",muted),
      Spacer(1,4*mm),two(box([P("Control mensual",h2),bullet("Ingresos cobrados."),bullet("CFDI emitidos."),bullet("Retenciones, si aplican."),bullet("Declaración mensual."),bullet("Pagos y comprobantes.")]),
          box([P("Recuerda",h2),P("RESICO no significa que todas las personas paguen la misma cantidad. Deben revisarse requisitos y situación fiscal.",small)],LIGHTGREEN)),
      PageBreak()]

# DECLARACIONES / BUZON
S += section(4,"Declaraciones y Buzón Tributario",
             "Dos puntos que conviene revisar constantemente para evitar descuidos.")
S += [P("Crea una rutina",h2),
      table(["MOMENTO","QUÉ REVISAR"],[
          ("Cada semana","Facturas emitidas, recibidas y pagos."),
          ("Antes del cierre","Ingresos, gastos, bancos y comprobantes pendientes."),
          ("Al presentar","Borrador, impuestos y saldo a pagar o favor."),
          ("Después de presentar","Acuse y comprobante de pago, cuando corresponda.")
      ],[50*mm,120*mm]), Spacer(1,5*mm),
      P("Buzón Tributario",h2),
      info("¿PARA QUÉ SIRVE?",
          "Es un canal de comunicación entre el SAT y el contribuyente. Mantén actualizados tus medios de contacto y revisa los avisos."),
      Spacer(1,4*mm),box([P("Checklist",h2),bullet("Revisar mensajes periódicamente."),bullet("Actualizar correo y teléfono."),bullet("Atender requerimientos dentro del plazo."),bullet("Guardar evidencia de respuestas y trámites.")]),
      Spacer(1,5*mm),info("EVITA ESTE ERROR",
          "No ignores una notificación porque no la entiendas. Guarda el aviso y busca orientación para conocer qué se solicita y el plazo.",colors.HexColor("#FFF7E6"),colors.HexColor("#A56A00")),
      PageBreak()]

# ERRORES
S += section(5,"Los errores fiscales más comunes",
             "Pequeños descuidos pueden complicar la administración de un negocio.")
errors=[
("01","No presentar declaraciones","Dejar pasar obligaciones puede generar recargos, multas u otros problemas."),
("02","Mezclar dinero personal y del negocio","Dificulta comprobar operaciones y saber cuánto gana realmente el negocio."),
("03","No pedir factura de las compras","Puede impedir acreditar o deducir operaciones cuando la legislación lo permita."),
("04","Ignorar el Buzón Tributario","Un aviso puede contener un requerimiento o información que necesita atención."),
("05","No guardar XML y comprobantes","El XML es el archivo fiscal que debe conservarse conforme a las obligaciones aplicables.")
]
for n,t,x in errors:
    row=Table([[P(n,ParagraphStyle("en",fontName=BOLD,fontSize=11,textColor=WHITE,alignment=TA_CENTER)),[P(t,h2),P(x,small)]]],colWidths=[15*mm,155*mm])
    row.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),BLUE),("BACKGROUND",(1,0),(1,0),WHITE),("BOX",(0,0),(-1,-1),0.6,BORDER),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    S += [row,Spacer(1,3*mm)]
S += [info("LA REGLA MÁS ÚTIL",
            "No dejes la contabilidad para el último día. Un pequeño control semanal puede ahorrarte tiempo y errores.",LIGHTGREEN,GREEN),
      PageBreak()]

# RUTINA + CTA
S += section(6,"Tu rutina fiscal mensual",
             "Convierte tus obligaciones en hábitos sencillos.")
S += [table(["PASO","ACCIÓN","¿QUÉ HACER?"],[
    ("1","Ordena","Reúne facturas de ventas, compras, gastos y movimientos bancarios."),
    ("2","Revisa","Comprueba que los CFDI correspondan a operaciones reales."),
    ("3","Compara","Compara ingresos y gastos contra tus estados de cuenta."),
    ("4","Declara","Presenta las obligaciones que correspondan dentro de los plazos."),
    ("5","Guarda","Conserva acuses, pagos, XML y documentación de respaldo."),
    ("6","Verifica","Revisa Buzón Tributario y avisos pendientes.")
],[18*mm,38*mm,114*mm]),Spacer(1,7*mm)]

cta=Table([[[P("¿QUIERES SABER CÓMO ESTÁ TU SITUACIÓN FISCAL?",white_center),
             Spacer(1,3*mm),P("Solicita un diagnóstico fiscal y conoce qué puedes revisar para mantener tus obligaciones en orden.",white_body),
             Spacer(1,4*mm),P("<b>ASESORES CONTABLES SÁNCHEZ</b>",white_body),
             P("Manzanillo, Colima",white_body),P("WhatsApp: +52 (314) 000-0000",white_body)]]],colWidths=[170*mm])
cta.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),BLUE),("LEFTPADDING",(0,0),(-1,-1),13),("RIGHTPADDING",(0,0),(-1,-1),13),("TOPPADDING",(0,0),(-1,-1),13),("BOTTOMPADDING",(0,0),(-1,-1),13)]))
S += [cta,Spacer(1,5*mm),P("<b>Nota:</b> Guía con fines informativos y educativos. Las obligaciones dependen de la situación de cada contribuyente y de las disposiciones vigentes.",muted)]

def main():
    print("Generando PDF...")
    if not LOGO.exists():
        print(f"AVISO: no se encontró {LOGO.name}. Se generará sin logo.")
    doc.build(S,onFirstPage=header_footer,onLaterPages=header_footer)
    print(f"Listo: {OUT}")

if __name__=="__main__":
    main()
