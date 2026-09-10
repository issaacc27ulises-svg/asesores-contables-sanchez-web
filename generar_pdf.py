import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def crear_pdf_completo():
    pdf_filename = "Guia_SAT_2026_Asesores_Contables_Sanchez.pdf"
    
    # Documento ajustado para 2 páginas exactas
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    
    # Paleta de Colores: Verde Principal y Azul Acento
    c_green_dark = colors.HexColor("#064e3b")    # Verde Bosque Oscuro (Estructura Principal / Header)
    c_green_emerald = colors.HexColor("#059669") # Verde Esmeralda (Títulos y Subsecciones)
    c_blue_bright = colors.HexColor("#2563eb")   # Azul Eléctrico (Acentos y CTA)
    c_blue_light = colors.HexColor("#eff6ff")    # Azul Cielo Suave (Fondos de Tarjetas / Filas)
    c_card_border = colors.HexColor("#cbd5e1")   # Bordes
    c_text_dark = colors.HexColor("#1e293b")     # Texto principal
    c_white = colors.white

    # Estilos Tipográficos
    title_style = ParagraphStyle(
        'HeaderTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, textColor=c_white,
        leading=17
    )

    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, textColor=c_green_dark,
        spaceBefore=8, spaceAfter=3, leading=14
    )

    body_style = ParagraphStyle(
        'BodyDark', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, textColor=c_text_dark,
        leading=11.5, spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'BulletText', parent=body_style,
        leftIndent=8, spaceAfter=2.5
    )

    badge_style = ParagraphStyle(
        'BadgeText', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#93c5fd"),
        alignment=2
    )

    story = []

    # --- ENCABEZADO PRINCIPAL ---
    logo_path = "logo.png"
    if not os.path.exists(logo_path):
        for alt_ext in ["logo.jpg", "logo.jpeg", "logo.png", "logo.svg"]:
            if os.path.exists(alt_ext):
                logo_path = alt_ext
                break

    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=90, height=70)
        header_left = Table([
            [logo_img, Paragraph("<b>ASESORES CONTABLES SÁNCHEZ</b><br/><font color='#6ee7b7'>Soluciones Contables & Fiscales</font>", title_style)]
        ], colWidths=[98, 250])
        header_left.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 0)
        ]))
    else:
        header_left = Paragraph("<b>ASESORES CONTABLES SÁNCHEZ</b><br/><font color='#6ee7b7'>Soluciones Contables & Fiscales</font>", title_style)

    header_right = Paragraph("<b>CHECKLIST SAT 2026</b><br/><font color='#93c5fd'>Guía para Emprendedores</font>", badge_style)

    header_table = Table([[header_left, header_right]], colWidths=[355, 185])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_green_dark),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    
    # --- PÁGINA 1 ---
    story.append(header_table)
    story.append(Spacer(1, 8))

    # Banner Introductorio
    intro_box = [
        [Paragraph(
            "<b>💡 Guía Práctica de Regularización Fiscal:</b> Preparada por <b>Asesores Contables Sánchez</b> en Manzanillo para apoyar a emprendedores y pymes. Cumple con tus trámites indispensables ante el SAT sin complicaciones.",
            ParagraphStyle('IntroText', parent=body_style, textColor=colors.HexColor("#1e40af"), fontSize=8, leading=11)
        )]
    ]
    intro_table = Table(intro_box, colWidths=[540])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_blue_light),
        ('BORDER', (0,0), (-1,-1), 1, c_blue_bright),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(intro_table)
    story.append(Spacer(1, 6))

    # Módulo 1: e.firma Primera Vez y Renovación en Línea
    story.append(Paragraph("1. Trámite y Renovación de e.firma (Firma Electrónica)", h2_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue_bright, spaceBefore=2, spaceAfter=4))
    
    efirma_data = [
        [Paragraph("<b>Requisito / Modalidad</b>", ParagraphStyle('TH1', parent=body_style, fontName='Helvetica-Bold', textColor=c_green_dark)), 
         Paragraph("<b>Especificaciones y Procedimiento Paso a Paso</b>", ParagraphStyle('TH2', parent=body_style, fontName='Helvetica-Bold', textColor=c_green_dark))],
        [Paragraph("Trámite Presencial (1ª Vez)", body_style), Paragraph("Cita en el SAT con INE o Pasaporte vigente, comprobante de domicilio (<3 meses) y USB limpia.", body_style)],
        [Paragraph("Renovación con Certifica (Vigente)", body_style), Paragraph("<b>Si tu e.firma sigue vigente:</b><br/>1. Descarga el programa <b>Certifica</b> (versión 32/64 bits) desde el portal del SAT.<br/>2. Selecciona la opción <i>'Solicitud de Requerimiento de Renovación de Firma Electrónica'</i>.<br/>3. Adjunta tu certificado vigente (<b>.CER</b>) y genera tu archivo de requerimiento (<b>.REN</b>) y clave privada nueva (<b>.KEY</b>).<br/>4. Ingresa al portal del SAT en la sección <i>'CertiSAT Web'</i>, envía el archivo <b>.REN</b> y descarga tu nuevo certificado (<b>.CER</b>).", body_style)],
        [Paragraph("Renovación con SAT ID (Vencida)", body_style), Paragraph("<b>Si venció hace menos de 1 año:</b> Ingresa a <i>satid.sat.gob.mx</i> o la app SAT ID, adjunta tu INE, graba un video de confirmación y tras la aprobación genera tu requerimiento con Certifica.", body_style)]
    ]
    efirma_table = Table(efirma_data, colWidths=[140, 400])
    efirma_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_blue_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(efirma_table)
    story.append(Spacer(1, 6))

    # Módulo 2: Facturación CFDI 4.0
    story.append(Paragraph("2. Requisitos para Facturación Electrónica (CFDI 4.0)", h2_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_green_emerald, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph("• <b>Constancia de Situación Fiscal Actualizada:</b> Nombre completo/Razón Social, RFC, Régimen y Código Postal deben coincidir sin variaciones.", bullet_style))
    story.append(Paragraph("• <b>Certificado de Sello Digital (CSD):</b> Archivo generado mediante el programa Certifica a partir de la e.firma para emitir facturas en sistemas de cobro.", bullet_style))
    story.append(Paragraph("• <b>Clave de Uso de CFDI:</b> Asignación precisa según la solicitud de tu cliente (<i>G03 - Gastos en general</i>, <i>CP01 - Pagos</i>, etc.).", bullet_style))
    story.append(Paragraph("• <b>Complemento de Pago:</b> Obligatorio en ventas a crédito o diferidas (PPD) al momento de recibir la transferencia.", bullet_style))

    # Salto a la Página 2
    story.append(PageBreak())

    # --- PÁGINA 2 ---
    story.append(header_table)
    story.append(Spacer(1, 8))

    # Módulo 3: RESICO Tabla
    story.append(Paragraph("3. Tablas del Régimen Simplificado de Confianza (RESICO 2026)", h2_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue_bright, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph("Aprovecha tasas preferenciales de Impuesto sobre la Renta (ISR) para ingresos menores a $3.5 MDP anuales:", body_style))

    resico_tabla = [
        [Paragraph("<b>Ingreso Mensual Bruto</b>", ParagraphStyle('RTH1', parent=body_style, fontName='Helvetica-Bold', textColor=c_white)), 
         Paragraph("<b>Tasa ISR SAT</b>", ParagraphStyle('RTH2', parent=body_style, fontName='Helvetica-Bold', textColor=c_white, alignment=1)), 
         Paragraph("<b>Pago Estimado de ISR</b>", ParagraphStyle('RTH3', parent=body_style, fontName='Helvetica-Bold', textColor=c_white, alignment=2))],
        [Paragraph("Hasta $25,000.00 MXN", body_style), Paragraph("1.00%", ParagraphStyle('C1', parent=body_style, alignment=1)), Paragraph("$250.00 MXN", ParagraphStyle('C2', parent=body_style, alignment=2))],
        [Paragraph("Hasta $50,000.00 MXN", body_style), Paragraph("1.10%", ParagraphStyle('C1', parent=body_style, alignment=1)), Paragraph("$550.00 MXN", ParagraphStyle('C2', parent=body_style, alignment=2))],
        [Paragraph("Hasta $83,333.33 MXN", body_style), Paragraph("1.50%", ParagraphStyle('C1', parent=body_style, alignment=1)), Paragraph("$1,250.00 MXN", ParagraphStyle('C2', parent=body_style, alignment=2))],
        [Paragraph("Hasta $208,333.33 MXN", body_style), Paragraph("2.00%", ParagraphStyle('C1', parent=body_style, alignment=1)), Paragraph("$4,166.66 MXN", ParagraphStyle('C2', parent=body_style, alignment=2))],
        [Paragraph("Hasta $291,666.67 MXN", body_style), Paragraph("2.50%", ParagraphStyle('C1', parent=body_style, alignment=1)), Paragraph("$7,291.66 MXN", ParagraphStyle('C2', parent=body_style, alignment=2))],
    ]
    resico_table = Table(resico_tabla, colWidths=[190, 150, 200])
    resico_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_green_dark),
        ('GRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_white, c_blue_light]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(resico_table)
    story.append(Spacer(1, 8))

    # Módulo 4: Errores Comunes
    story.append(Paragraph("4. Evita los 4 Errores Fiscales Más Comunes", h2_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_green_emerald, spaceBefore=2, spaceAfter=4))
    story.append(Paragraph("❌ <b>Omitir dos o más declaraciones consecutivas:</b> El SAT puede reclasificarte al Régimen de Actividad Empresarial con tasas de hasta el 35%.", bullet_style))
    story.append(Paragraph("❌ <b>Mezclar gastos personales con cuentas del negocio:</b> Todo gasto a deducir o acreditar requiere pago con tarjetas o transferencias del titular.", bullet_style))
    story.append(Paragraph("❌ <b>Ignorar las notificaciones del Buzón Tributario:</b> Los avisos surten efecto legal a los 3 días hábiles de su envío.", bullet_style))
    story.append(Paragraph("❌ <b>No facturar tus compras o suministros:</b> Sin CFDI pierdes la oportunidad de reducir cargos en tus declaraciones de IVA.", bullet_style))
    story.append(Spacer(1, 10))

    # LLAMADO A LA ACCIÓN (CTA)
    cta_box = [
        [Paragraph(
            "<font size=9.5 color='#ffffff'><b>¿QUIERES REVISAR TU ESTATUS DEL SAT SIN COSTO?</b></font><br/><br/>"
            "<font size=8 color='#eff6ff'>"
            "Solicita tu diagnóstico fiscal gratuito con nuestro equipo en Manzanillo.<br/>"
            "📍 <b>Ubicación:</b> Manzanillo, Colima | 📱 <b>WhatsApp:</b> +52 (314) 000-0000<br/>"
            "🌐 <b>Página Web:</b> Asesores Contables Sánchez"
            "</font>",
            ParagraphStyle('CtaStyle', parent=styles['Normal'], alignment=1, leading=12)
        )]
    ]
    cta_table = Table(cta_box, colWidths=[540])
    cta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_blue_bright),
        ('BORDER', (0,0), (-1,-1), 1.5, c_green_dark),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(cta_table)

    doc.build(story)
    print("PDF generado con éxito: Guia_SAT_2026_Asesores_Contables_Sanchez.pdf")

if __name__ == "__main__":
    crear_pdf_completo()