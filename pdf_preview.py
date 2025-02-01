import os
import tkinter as tk
from tkinter import ttk
from pdf_generator import generar_cotizacion_pdf
from cotizaciones import load_cotizaciones
from PIL import Image, ImageTk
import fitz  # PyMuPDF

class PDFPreview:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Preview")
        
        # Frame principal
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botón para generar y previsualizar
        self.preview_button = ttk.Button(self.main_frame, text="Generar y Previsualizar", command=self.update_preview)
        self.preview_button.grid(row=0, column=0, pady=10)
        
        # Canvas para mostrar el PDF
        self.canvas = tk.Canvas(self.main_frame, width=600, height=800)
        self.canvas.grid(row=1, column=0, pady=10)
        
    def update_preview(self):
        # Generar el PDF
        cotizaciones = load_cotizaciones()
        if not cotizaciones:
            print("No hay cotizaciones para previsualizar")
            return
            
        # Obtener la última cotización
        ultima_cotizacion = cotizaciones[-1]  # Toma la última cotización de la lista
        generar_cotizacion_pdf(ultima_cotizacion)
        
        try:
            # Obtener el último archivo PDF generado
            pdf_files = [f for f in os.listdir("pdfs") if f.endswith('.pdf')]
            if not pdf_files:
                print("No se encontraron archivos PDF")
                return
                
            latest_pdf = max(pdf_files, key=lambda x: os.path.getctime(os.path.join("pdfs", x)))
            pdf_path = os.path.join("pdfs", latest_pdf)
            
            # Abrir el PDF generado
            doc = fitz.open(pdf_path)
            page = doc[0]  # Primera página
            
            # Convertir a imagen
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Zoom 2x para mejor calidad
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Redimensionar si es necesario
            ratio = min(600/img.width, 800/img.height)
            new_size = (int(img.width*ratio), int(img.height*ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Mostrar en el canvas
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(300, 400, image=self.photo)
            
            doc.close()
        except Exception as e:
            print(f"Error al previsualizar el PDF: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFPreview(root)
    root.mainloop()