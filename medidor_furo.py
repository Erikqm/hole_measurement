import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math

def acha_circulos(contours, imagem_shape):
    altura, largura = imagem_shape[0], imagem_shape[1]
    centro_imagem_x = largura // 2
    centro_imagem_y = altura // 2
    melhor_circulo = None
    melhor_raio = None
    menor_distancia = float('inf')
    melhor_centro = None
    
    for bordas_imagem in contours:
        area = cv2.contourArea(bordas_imagem)
        #Elimina ruído
        if area < 100:
            continue
            
        (x, y), raio = cv2.minEnclosingCircle(bordas_imagem)
        area_circulo_envolvente = math.pi * raio * raio
        circularidade = area / area_circulo_envolvente
        
        #Filtra areas que se parecem com um circulo
        if circularidade > 0.5:
            
            dx = x - centro_imagem_x
            dy = y - centro_imagem_y
            distancia = math.sqrt(dx*dx + dy*dy)

            #verifica o circulo mais central
            if distancia < menor_distancia:
                menor_distancia = distancia
                melhor_circulo = bordas_imagem
                melhor_raio = raio
                melhor_centro = (int(x), int(y))
                
    return melhor_circulo, melhor_raio, melhor_centro

def processar_imagem(caminho_imagem):
    img = cv2.imread(caminho_imagem)
    if img is None:
        return None, None, None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 100)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    circulo, raio, centro = acha_circulos(contours, img.shape)
    diametro = raio * 2 if raio else None
    return img, diametro, centro

def criar_canvas_com_circulo(img_cv2, centro, raio, diametro_pixels, diametro_mm, titulo):
    
    img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
    
    h, w = img_rgb.shape[0], img_rgb.shape[1]
    scale = min(800.0/w, 600.0/h)
    new_w, new_h = int(w*scale), int(h*scale)
    img_resized = cv2.resize(img_rgb, (new_w, new_h))
    
    # Ajustar centro e raio para a nova escala
    centro_scaled = (int(centro[0]*scale), int(centro[1]*scale))
    raio_scaled = int(raio*scale)
    
    # Converter para PIL
    img_pil = Image.fromarray(img_resized)
    draw = ImageDraw.Draw(img_pil)
    
    # Desenhar círculo verde
    x, y = centro_scaled
    x1, y1 = x-raio_scaled, y-raio_scaled
    x2, y2 = x+raio_scaled, y+raio_scaled
    draw.ellipse([x1, y1, x2, y2], outline="red", width=3)
    
    # Adicionar texto
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    texto = f"{titulo}\nPixels: {diametro_pixels:.1f}px\nMM: {diametro_mm:.3f}mm"
    draw.text((10, 10), texto, fill="red", font=font)
    
    # Converter para PhotoImage
    return ImageTk.PhotoImage(img_pil)

def selecionar_imagem_ref():
    arquivo = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")])
    if arquivo:
        entry_ref.delete(0, tk.END)
        entry_ref.insert(0, arquivo)

def selecionar_imagem_medicao():
    arquivo = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")])
    if arquivo:
        entry_medicao.delete(0, tk.END)
        entry_medicao.insert(0, arquivo)

def calcular():
    try:
        # Validar inputs
        caminho_ref = entry_ref.get()
        mm_ref = float(entry_mm.get())
        caminho_medicao = entry_medicao.get()
        
        if not caminho_ref or not caminho_medicao:
            messagebox.showerror("Erro", "Selecione as duas imagens")
            return
            
        # Processar imagens
        img_ref, diametro_ref, centro_ref = processar_imagem(caminho_ref)
        img_medicao, diametro_medicao, centro_medicao = processar_imagem(caminho_medicao)
        
        if diametro_ref is None or diametro_medicao is None:
            messagebox.showerror("Erro", "Não foi possível detectar círculos nas imagens")
            return
            
        if centro_ref is None or centro_medicao is None:
            messagebox.showerror("Erro", "Não foi possível detectar centros dos círculos")
            return
            
        # Calcular medida
        pixel_mm = mm_ref / diametro_ref
        resultado_mm = diametro_medicao * pixel_mm
        
        # Criar canvas com imagens
        img_tk_ref = criar_canvas_com_circulo(img_ref, centro_ref, diametro_ref/2, 
                                            diametro_ref, mm_ref, "REFERÊNCIA")
        img_tk_medicao = criar_canvas_com_circulo(img_medicao, centro_medicao, diametro_medicao/2,
                                                diametro_medicao, resultado_mm, "MEDIÇÃO")
        
        # Atualizar canvas
        canvas_ref.delete("all")
        canvas_medicao.delete("all")
        canvas_ref.create_image(400, 300, image=img_tk_ref)
        canvas_medicao.create_image(400, 300, image=img_tk_medicao)
        
        # Manter referência das imagens
        canvas_ref.image = img_tk_ref
        canvas_medicao.image = img_tk_medicao
        
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido para mm")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro no processamento: {str(e)}")

# Interface
root = tk.Tk()
root.title("Medição de Furos")
root.geometry("900x800")

# Frame superior com controles
frame_controles = tk.Frame(root)
frame_controles.pack(pady=10)

tk.Label(frame_controles, text="Imagem de Referência:").pack(pady=2)
frame_ref = tk.Frame(frame_controles)
frame_ref.pack(pady=2)
entry_ref = tk.Entry(frame_ref, width=50)
entry_ref.pack(side=tk.LEFT, padx=5)
tk.Button(frame_ref, text="Selecionar", command=selecionar_imagem_ref).pack(side=tk.LEFT)

tk.Label(frame_controles, text="Medida de Referência (mm):").pack(pady=2)
entry_mm = tk.Entry(frame_controles, width=20)
entry_mm.pack(pady=2)

tk.Label(frame_controles, text="Imagem para Medição:").pack(pady=2)
frame_medicao = tk.Frame(frame_controles)
frame_medicao.pack(pady=2)
entry_medicao = tk.Entry(frame_medicao, width=50)
entry_medicao.pack(side=tk.LEFT, padx=5)
tk.Button(frame_medicao, text="Selecionar", command=selecionar_imagem_medicao).pack(side=tk.LEFT)

tk.Button(frame_controles, text="CALCULAR", command=calcular, bg="lightblue", font=("Arial", 12, "bold")).pack(pady=10)

# Frame para os canvas
frame_canvas = tk.Frame(root)
frame_canvas.pack(pady=10)

# Canvas para imagem de referência
tk.Label(frame_canvas, text="IMAGEM DE REFERÊNCIA", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10)
canvas_ref = tk.Canvas(frame_canvas, width=800, height=600, bg="white", relief="raised", bd=2)
canvas_ref.grid(row=1, column=0, padx=10, pady=5)

# Canvas para imagem de medição
tk.Label(frame_canvas, text="IMAGEM DE MEDIÇÃO", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10)
canvas_medicao = tk.Canvas(frame_canvas, width=800, height=600, bg="white", relief="raised", bd=2)
canvas_medicao.grid(row=1, column=1, padx=10, pady=5)

root.mainloop()