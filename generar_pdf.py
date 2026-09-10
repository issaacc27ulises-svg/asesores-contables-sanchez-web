import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def crear_pdf_juvenil_profesional():
    pdf_filename = "Guia_SAT_2026_Asesores_Contables_Sanchez.pdf"
    
    # Documento con márgenes optimizados para 2 páginas exactas
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    
    # Paleta Fresca y Juvenil: Azules, Verdes y Blancos
    c_navy = colors.HexColor("#0f172a")       # Azul Oscuro Profundo (Estructura)
    c_blue_bright = colors.HexColor("#2563eb") # Azul Eléctrico (Acentos)
    c_green_emerald = colors.HexColor("#059669")# Verde Esmeralda (Destacados y Éxito)
    c_green_light = colors.HexColor("#ecfdf5")  # Verde Menta Suave (Fondos de Tablas/Llamados)
    c_bg_light = colors.HexColor("#f8fafc")     # Gris/Blanco Suave
    c_card_border = colors.HexColor("#cbd5e1")  # Bordes sutiles
    c_text_dark = colors.HexColor("#1e293b")    # Texto principal
    c_white = colors.white

    # Estilos Tipográficos
    title_style = ParagraphStyle(
        'HeaderTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=15, textColor=c_white,
        leading=18
    )

    subtitle_style = ParagraphStyle(
        'HeaderSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#a7f3d0"), # Verde menta claro
        leading=11
    )

    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, textColor=c_navy,
        spaceBefore=10, spaceAfter=4, leading=15
    )

    body_style = ParagraphStyle(
        'BodyDark', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, textColor=c_text_dark,
        leading=12.5, spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletText', parent=body_style,
        leftIndent=10, spaceAfter=3
    )

    badge_style = ParagraphStyle(
        'BadgeText', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#6ee7b7"), # Verde fluorescente suave
        alignment=2
    )

    story = []

    # --- ENCABEZADO CON LOGO AMPLIADO ---
    logo_path = "logo.png"
    if not os.path.exists(logo_path):
        for alt_ext in ["logo.jpg", "logo.jpeg", "logo.png", "logo.svg"]:
            if os.path.exists(alt_ext):
                logo_path = alt_ext
                break

    # Se ajusta el logo a un tamaño visible de 90px de ancho
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=90, height=70)
        header_left = Table([
            [logo_img, Paragraph("<b>ASESORES CONTABLES SÁNCHEZ</b><br/><font color='#a7f3d0'>Soluciones Contables & Fiscales</font>", title_style)]
        ], colWidths=[98, 250])
        header_left.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 0)
        ]))
    else:
        header_left = Paragraph("<b>ASESORES CONTABLES SÁNCHEZ</b><br/><font color='#a7f3d0'>Soluciones Contables & Fiscales</font>", title_style)

    header_right = Paragraph("<b>CHECKLIST SAT 2026</b><br/><font color='#60a5fa'>Guía para Emprendedores</font>", badge_style)

    header_table = Table([[header_left, header_right]], colWidths=[355, 185])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_navy),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    
    # --- PÁGINA 1 ---
    story.append(header_table)
    story.append(Spacer(1, 10))

    # Banner Introductorio (Estilo Tarjeta Menta)
    intro_box = [
        [Paragraph(
            "<b>💡 Guía Práctica de Regularización Fiscal:</b> Preparada por <b>Asesores Contables Sánchez</b> en Manzanillo para apoyar a emprendedores y pymes. Cumple con tus trámites indispensables ante el SAT sin complicaciones.",
            ParagraphStyle('IntroText', parent=body_style, textColor=colors.HexColor("#065f46"), fontSize=8.5, leading=12)
        )]
    ]
    intro_table = Table(intro_box, colWidths=[540])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_green_light),
        ('BORDER', (0,0), (-1,-1), 1, c_green_emerald),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(intro_table)
    story.append(Spacer(1, 8))

    # Módulo 1: e.firma
    story.append(Paragraph("1. Trámite y Renovación de e.firma (Firma Electrónica)", h2_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_green_emerald, spaceBefore=2, spaceAfter=6))
    
    efirma_data = [
        [Paragraph("<b>Requisito / Documento</b>", ParagraphStyle('TH1', parent=body_style, fontName='Helvetica-Bold', textColor=c_navy)), 
         Paragraph("<b>Especificaciones Oficiales del SAT</b>", ParagraphStyle('TH2', parent=body_style, fontName='Helvetica-Bold', textColor=c_navy))],
        [Paragraph("Identificación Oficial", body_style), Paragraph("INE o Pasaporte vigente (original para cotejo presencial).", body_style)],
        [Paragraph("Comprobante de Domicilio", body_style), Paragraph("Máximo 3 meses de antigüedad (Luz, Agua, Estado de Cuenta). Coincidente con Domicilio Fiscal.", body_style)],
        [Paragraph("Unidad USB Limpia", body_style), Paragraph("Para descarga directa de tus archivos confidenciales: <b>.KEY</b>, <b>.CER</b> y clave secreta.", body_style)],
        [Paragraph("Buzón Tributario", body_style), Paragraph("Correo electrónico y número celular registrados y validados.", body_style)]
    ]
    efirma_table = Table(efirma_data, colWidths=[140, 400])
    efirma_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_green_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(efirma_table)
    story.append(Spacer(1, 8))

    # Módulo 2: Facturación CFDI 4.0
    story.append(Paragraph("2. Requisitos para Facturación Electrónica (CFDI 4.0)", h2_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue_bright, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph("• <b>Constancia de Situación Fiscal Actualizada:</b> Nombre completo/Razón Social, RFC, Régimen y Código Postal deben coincidir sin variaciones.", bullet_style))
    story.append(Paragraph("• <b>Certificado de Sello Digital (CSD):</b> Archivo tramitado a partir de la e.firma necesario para emitir facturas en sistemas de cobro.", bullet_style))
    story.append(Paragraph("• <b>Clave de Uso de CFDI:</b> Asignación precisa según la solicitud de tu cliente (<i>G03 - Gastos en general</i>, <i>CP01 - Pagos</i>, etc.).", bullet_style))
    story.append(Paragraph("• <b>Complemento de Pago:</b> Obligatorio en ventas a crédito o diferidas (PPD) al momento de recibir la transferencia.", bullet_style))

    # Salto a la Página 2
    story.append(PageBreak())

    # --- PÁGINA 2 ---
    story.append(header_table)
    story.append(Spacer(1, 10))

    # Módulo 3: RESICO Tabla
    story.append(Paragraph("3. Tablas del Régimen Simplificado de Confianza (RESICO 2026)", h2_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_green_emerald, spaceBefore=2, spaceAfter=6))
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
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [c_white, c_green_light]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(resico_table)
    story.append(Spacer(1, 10))

    # Módulo 4: Errores Comunes
    story.append(Paragraph("4. Evita los 4 Errores Fiscales Más Comunes", h2_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue_bright, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph("❌ <b>Omitir dos o más declaraciones consecutivas:</b> El SAT puede reclasificarte al Régimen de Actividad Empresarial con tasas de hasta el 35%.", bullet_style))
    story.append(Paragraph("❌ <b>Mezclar gastos personales con cuentas del negocio:</b> Todo gasto a deducir o acreditar requiere pago con tarjetas o transferencias del titular.", bullet_style))
    story.append(Paragraph("❌ <b>Ignorar las notificaciones del Buzón Tributario:</b> Los avisos surten efecto legal a los 3 días hábiles de su envío.", bullet_style))
    story.append(Paragraph("❌ <b>No facturar tus compras o suministros:</b> Sin CFDI pierdes la oportunidad de reducir cargos en tus declaraciones de IVA.", bullet_style))
    story.append(Spacer(1, 12))

    # LLAMADO A LA ACCIÓN (CTA) EN COLOR VERDE ESMERALDA / BLANCO
    cta_box = [
        [Paragraph(
            "<font size=10 color='#ffffff'><b>¿QUIERES REVISAR TU ESTATUS DEL SAT SIN COSTO?</b></font><br/><br/>"
            "<font size=8.5 color='#ecfdf5'>"
            "Solicita tu diagnóstico fiscal gratuito con nuestro equipo en Manzanillo.<br/>"
            "📍 <b>Ubicación:</b> Manzanillo, Colima | 📱 <b>WhatsApp:</b> +52 (314) 170-7265<br/>"
            "🌐 <b>Página Web:</b> Asesores Contables Sánchez"
            "</font>",
            ParagraphStyle('CtaStyle', parent=styles['Normal'], alignment=1, leading=13)
        )]
    ]
    cta_table = Table(cta_box, colWidths=[540])
    cta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_green_emerald),
        ('BORDER', (0,0), (-1,-1), 1.5, c_navy),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(cta_table)

    doc.build(story)
    print("PDF profesional, juvenil e integrado generado con éxito: Guia_SAT_2026_Asesores_Contables_Sanchez.pdf")

if __name__ == "__main__":
    crear_pdf_juvenil_profesional()