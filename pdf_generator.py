import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generar_cotizacion_pdf(cotizacion):
    # Crear un buffer en memoria para el PDF
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Crear estilos personalizados
    styles.add(ParagraphStyle(
        name='Empresa',
        fontSize=16,
        alignment=1,  # Centro
        spaceAfter=20
    ))
    
    styles.add(ParagraphStyle(
        name='DatosEmpresa',
        fontSize=8,
        leading=10
    ))
    
    styles.add(ParagraphStyle(
        name='TituloCotizacion',
        fontSize=14,
        alignment=2,  # Derecha
        spaceBefore=10,
        spaceAfter=20
    ))
    
    # Estilo para la descripción de los productos (para ajustar el texto y que se expanda la celda)
    style_descripcion = ParagraphStyle(
        name='DescripcionProducto',
        fontSize=8,
        leading=10,
        leftIndent=0,
        rightIndent=0
    )
    
    # Cargar el logo
    logo_path = "logo.png"  # Asegúrate de que este archivo se encuentre en la ruta indicada
    try:
        # Ajusta el ancho y alto según tus necesidades
        logo = Image(logo_path, width=1.5*inch, height=1*inch)
    except Exception as e:
        # En caso de error, se utiliza el texto "ACESMA INOX"
        logo = Paragraph("ACESMA INOX", styles['Empresa'])
    
    # Información de la empresa y cotización (encabezado)
    data_header = [
        [logo, 'COTIZACIÓN'],
        ['Calle Constantino Carvallo N°276 Urb. Santa Catina, La Victoria', f'FECHA: {datetime.now().strftime("%d/%m/%Y")}'],
        ['Ciudad: Lima', f'COTIZACIÓN #: {cotizacion["id"]}'],
        ['Sitio Web: acesmainox.com', f'CLIENTE ID: {cotizacion["datos del cliente"]["RUC"]}'],
        ['Teléfono: 952439843 | 980165809 | 92049843', 'VÁLIDO HASTA:'],
        ['E-mail: contacto@acesmainox.com', ''],
        ['Asesor de venta: Arturo Ledesma', ''],
        ['Cuenta Corriente Soles Interbank: 2003003503664', ''],
        ['CCI: 00320000300350366436', '']
    ]
    
    t_header = Table(data_header, colWidths=[4.5*inch, 2.5*inch])
    t_header.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    elements.append(t_header)
    elements.append(Spacer(1, 20))
    
    # Datos del cliente
    data_cliente = [
        ['CLIENTE', ''],
        ['Nombre:', cotizacion['datos del cliente']['Nombre del cliente']],
        ['Email:', cotizacion['datos del cliente']['E-mail']],
        ['Dirección:', cotizacion['datos del cliente']['Dirección']],
        ['RUC:', cotizacion['datos del cliente']['RUC']],
        ['Teléfono:', cotizacion['datos del cliente']['Telefono']]
    ]
    
    t_cliente = Table(data_cliente, colWidths=[1.5*inch, 5.5*inch])
    t_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1C4E4E')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    elements.append(t_cliente)
    elements.append(Spacer(1, 20))
    
    # Tabla de productos con anchos ajustados
    col_widths = [0.7*inch, 2.8*inch, 0.5*inch, 0.75*inch, 0.75*inch, 0.75*inch, 0.75*inch]  # Total = 7 inches
    data_productos = [['CÓDIGO', 'DESCRIPCIÓN', 'CANT.', 'VALOR', 'SUBTOTAL', 'IMPUESTO', 'TOTAL']]
    
    total_general = 0
    for producto in cotizacion['productos']:
        subtotal = producto['precio'] * producto['cantidad']
        impuesto = subtotal * 0.18  # IGV 18%
        total = subtotal + impuesto
        total_general += total
        
        # Envolver la descripción en un Paragraph para que se ajuste y la celda se expanda verticalmente
        descripcion_paragraph = Paragraph(producto['descripcion'], style_descripcion)
        
        data_productos.append([
            '',  # Código (vacío o agrega el valor correspondiente si lo tienes)
            descripcion_paragraph,
            str(producto['cantidad']),
            f"S/ {producto['precio']:.2f}",
            f"S/ {subtotal:.2f}",
            f"S/ {impuesto:.2f}",
            f"S/ {total:.2f}"
        ])
    
    t_productos = Table(data_productos, colWidths=col_widths)
    t_productos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1C4E4E')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),  # Alinear la descripción a la izquierda
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(t_productos)
    
    # Agregar fila final con el total general de todos los productos
    data_total = [["", "", "", "", "", "TOTAL GENERAL", f"S/ {total_general:.2f}"]]
    t_total = Table(data_total, colWidths=col_widths)
    t_total.setStyle(TableStyle([
        # Fusionamos las primeras 6 celdas para dejar espacio al texto "TOTAL GENERAL"
        ('SPAN', (0, 0), (5, 0)),
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ('ALIGN', (6, 0), (6, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(Spacer(1, 10))
    elements.append(t_total)
    
    # Términos y condiciones
    elements.append(Spacer(1, 20))
    terms_data = [
        ['TÉRMINOS Y CONDICIONES', ''],
        ['Fecha de entrega:', '5 días útiles'],
        ['Forma de pago:', '50% al inicio del contrato y el otro 50% contraentrega'],
        ['', 'incluye movilidad hasta el punto de entrega'],
    ]
    
    t_terms = Table(terms_data, colWidths=[2*inch, 5*inch])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1C4E4E')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t_terms)
    
    # Firma
    elements.append(Spacer(1, 30))
    firma_data = [
        ['_____________________'],
        ['Nombre del cliente:'],
    ]
    t_firma = Table(firma_data)
    t_firma.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t_firma)
    
    # Pie de página
    elements.append(Spacer(1, 20))
    footer_text = (
        "Si usted tiene alguna pregunta sobre esta cotización, por favor, póngase en contacto con nosotros\n"
        "ACESMA INOX | Teléfono: 952439843 | 980165809 | 920439843 | E-mail: contacto@acesmainox.com\n"
        "¡Gracias por hacer trato con nosotros!"
    )
    footer = Paragraph(footer_text, styles['DatosEmpresa'])
    elements.append(footer)
    
    # Construir el PDF en memoria
    doc.build(elements)
    
    # Obtener el contenido del PDF
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data
