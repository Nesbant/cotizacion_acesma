import streamlit as st
from cotizaciones import addCotizaciones, mostrarCotizaciones, generarPDF
import json
import os
from datetime import datetime
from pdf_generator import generar_cotizacion_pdf

# Definir el archivo donde se guardarán las cotizaciones
COTIZACIONES_FILE = "cotizaciones.json"

def load_cotizaciones():
    """Carga las cotizaciones desde un archivo JSON."""
    if os.path.exists(COTIZACIONES_FILE):
        try:
            with open(COTIZACIONES_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Retorna lista vacía si hay un error en el JSON
    return []

def save_cotizacion(datos_cliente, productos):
    """Guarda una nueva cotización en el JSON."""
    cotizaciones = load_cotizaciones()
    cotizacion = {
        "id": len(cotizaciones) + 1,
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        "datos del cliente": datos_cliente,
        "productos": productos
    }
    cotizaciones.append(cotizacion)

    with open(COTIZACIONES_FILE, "w") as file:
        json.dump(cotizaciones, file, indent=4)
    return cotizacion

def main():
    """Función principal de la aplicación."""
    
    # Crear directorio pdfs si no existe
    os.makedirs("pdfs", exist_ok=True)
    
    st.set_page_config(
        page_title="Sistema de Cotizaciones ACESMA INOX",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Sistema de Cotizaciones ACESMA INOX")
    
    menu = st.sidebar.selectbox(
        "Menú",
        ["Crear Cotización", "Ver Cotizaciones"]
    )
    
    if menu == "Crear Cotización":
        st.header("Nueva Cotización")

        # Datos del cliente
        st.subheader("Datos del Cliente")
        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre del Cliente")
            ruc = st.text_input("RUC")
            telefono = st.text_input("Teléfono")

        with col2:
            email = st.text_input("Email")
            direccion = st.text_input("Dirección")

        # Productos
        st.subheader("Productos")

        productos = []
        num_productos = st.number_input("Número de productos", min_value=1, value=1)

        for i in range(int(num_productos)):
            st.markdown(f"### Producto {i+1}")
            col1, col2, col3 = st.columns(3)

            with col1:
                descripcion = st.text_input(f"Descripción", key=f"desc_{i}")
            with col2:
                precio = st.number_input(f"Precio", min_value=0.0, key=f"precio_{i}")
            with col3:
                cantidad = st.number_input(f"Cantidad", min_value=1, key=f"cant_{i}")

            if descripcion and precio and cantidad:
                productos.append({
                    "descripcion": descripcion,
                    "precio": precio,
                    "cantidad": cantidad
                })

        if st.button("Generar Cotización"):
            if nombre and ruc and telefono and email and direccion and productos:
                datos_cliente = {
                    "Nombre del cliente": nombre,
                    "RUC": ruc,
                    "Telefono": telefono,
                    "E-mail": email,
                    "Dirección": direccion
                }

                cotizacion = save_cotizacion(datos_cliente, productos)
                if cotizacion:
                    try:
                        pdf_data = generar_cotizacion_pdf(cotizacion)
                        if pdf_data:
                            st.success("Cotización generada exitosamente!")
                            st.download_button(
                                label="⬇️ Descargar Cotización PDF",
                                data=pdf_data,
                                file_name=f"cotizacion_{cotizacion['id']}.pdf",
                                mime='application/pdf'
                            )
                        else:
                            st.error("Error al generar el PDF, el archivo está vacío.")
                    except Exception as e:
                        st.error(f"Error al generar el PDF: {str(e)}")
            else:
                st.warning("Por favor complete todos los campos")

    else:  # Ver Cotizaciones
        st.header("Cotizaciones Existentes")
        cotizaciones = load_cotizaciones()

        if not cotizaciones:
            st.info("No hay cotizaciones registradas")
        else:
            for cotizacion in cotizaciones:
                with st.expander(f"Cotización #{cotizacion['id']} - {cotizacion['datos del cliente']['Nombre del cliente']}"):
                    st.write("### Datos del Cliente")
                    for key, value in cotizacion['datos del cliente'].items():
                        st.write(f"**{key}:** {value}")

                    st.write("### Productos")
                    for producto in cotizacion['productos']:
                        subtotal = producto['precio'] * producto['cantidad']
                        impuesto = subtotal * 0.18
                        total = subtotal + impuesto
                        st.write(f"- **{producto['descripcion']}**")
                        st.write(f"  Precio: S/ {producto['precio']:.2f}")
                        st.write(f"  Cantidad: {producto['cantidad']}")
                        st.write(f"  Subtotal: S/ {subtotal:.2f}")
                        st.write(f"  IGV (18%): S/ {impuesto:.2f}")
                        st.write(f"  Total: S/ {total:.2f}")

                    if st.button("Descargar PDF", key=f"pdf_{cotizacion['id']}"):
                        try:
                            pdf_data = generar_cotizacion_pdf(cotizacion)
                            if pdf_data:
                                st.download_button(
                                    label="⬇️ Descargar PDF",
                                    data=pdf_data,
                                    file_name=f"cotizacion_{cotizacion['id']}.pdf",
                                    mime='application/pdf',
                                    key=f'download-pdf-{cotizacion["id"]}'
                                )
                            else:
                                st.error("Error al generar el PDF, el archivo está vacío.")
                        except Exception as e:
                            st.error(f"Error al generar el PDF: {str(e)}")

if __name__ == "__main__":
    main()  # Llamar a la función principal sin usar subprocess
