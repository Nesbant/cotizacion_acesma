import os 
import json
from pdf_generator import generar_cotizacion_pdf

cotizaciones_file = "cotizaciones.json"


def load_cotizaciones():
    if os.path.exists(cotizaciones_file):
        with open(cotizaciones_file, "r") as file:
            return json.load(file)
    return []

def save_cotizaciones(cotizaciones):
    with open(cotizaciones_file, "w") as file:
        json.dump(cotizaciones, file, indent=4)


def generarPDF(cotizacion):
    try:
        # Crear directorio pdfs si no existe
        if not os.path.exists("pdfs"):
            os.makedirs("pdfs")
            
        # Generar el PDF y obtener la ruta
        pdf_path = os.path.join("pdfs", f"cotizacion_{cotizacion['id']}.pdf")
        if generar_cotizacion_pdf(cotizacion, pdf_path):
            return pdf_path
        return None
    except Exception as e:
        print(f"Error al generar PDF: {str(e)}")
        return None



def addCotizaciones():
    cotizaciones = load_cotizaciones()
    print("Ingrese los datos del cliente")
    nombreCliente = input("Ingrese el nombre: ")
    ruc = input("Ingrese el N° RUC")
    telefono = input("Imgrese el telefono: ")
    email = input("Ingrese suc correo electrónico")
    direccion = input("Ingrese la direccción: ")
    datosCliente = {
        "Nombre del cliente": nombreCliente,
        "RUC": ruc,
        "Telefono": telefono,
        "E-mail": email,
        "Dirección": direccion,

    }
    numProductos = int(input("Cuantos productos va a llenar en la cotización: "))
    
    productos = []  
    
    for i in range(numProductos):  # Usamos range() para iterar sobre el número de productos
        producto = {
            "descripcion": input("Ingrese la descripción completa del producto: "),
            "precio": float(input("Ingrese el precio: ")),
            "cantidad": int(input("Ingrese la cantidad: "))
        }
        productos.append(producto)
    
    cotizacion = {
        "datos del cliente": datosCliente,
        "id": len(cotizaciones) + 1,
        "productos": productos
    }
    cotizaciones.append(cotizacion)
    save_cotizaciones(cotizaciones)
    print("Cotización agregada con éxito\n")
    pdf_path = generarPDF(cotizacion)
    if pdf_path:
        print(f"PDF generado exitosamente. Ruta: {pdf_path}")
    else:
        print("No se pudo generar el PDF")

        
def mostrarCotizaciones():
    cotizaciones = load_cotizaciones()
    if not cotizaciones:
        print("No hay cotizaciones registradas.")
        return
        
    for cotizacion in cotizaciones:  # Cambiar el bucle para iterar directamente
        print(f"\nID: {cotizacion['id']}")
        print("Productos:")
        for producto in cotizacion['productos']:
            print(f"- Descripción: {producto['descripcion']}")
            print(f"  Precio: ${producto['precio']}")
            print(f"  Cantidad: {producto['cantidad']}")
            print(f"  Total: ${producto['precio'] * producto['cantidad']}")
        print("-" * 40)    