import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.ppm")])
    if file_path:
        load_image(file_path)

def load_image(file_path):
    global img_data, img_width, img_height, img_maxval, img_format
    img_format = file_path.split(".")[-1].lower()
    if img_format == "ppm":
        with open(file_path, 'rb') as f:
            header = f.readline().decode().strip()
            if header != 'P6':
                messagebox.showerror("Error", "Hanya mendukung file PPM (P6)")
                return
            
            dimensions = f.readline().decode().strip()
            while dimensions.startswith('#'):
                dimensions = f.readline().decode().strip()
            
            img_width, img_height = map(int, dimensions.split())
            img_maxval = int(f.readline().decode().strip())
            img_data = bytearray(f.read())
    elif img_format == "png":
        image = Image.open(file_path)
        img_width, img_height = image.size
        img_data = image.tobytes()
    
    display_image()

def display_image():
    global img_data, img_width, img_height, img_format
    if not img_data:
        return

    if img_format == "ppm":
        img = tk.PhotoImage(width=img_width, height=img_height)
        for y in range(img_height):
            row_data = []
            for x in range(img_width):
                idx = (y * img_width + x) * 3
                r, g, b = img_data[idx:idx+3]
                row_data.append(f'#{r:02x}{g:02x}{b:02x}')
            img.put("{" + " ".join(row_data) + "}", to=(0, y, img_width, y+1))
    elif img_format == "png":
        img = ImageTk.PhotoImage(Image.frombytes("RGB", (img_width, img_height), img_data))

    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    canvas.image = img

# Membuat GUI dengan tkinter
root = tk.Tk()
root.title("Pengolahan Citra Digital Sederhana")

# Membuat canvas untuk menampilkan gambar
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

# Menambahkan tombol untuk membuka gambar
btn_open = tk.Button(root, text="Buka Gambar", command=open_image)
btn_open.pack()

# Inisialisasi variabel global
img_data = None
img_width = 0
img_height = 0
img_maxval = 255
img_format = None

# Menjalankan loop utama tkinter
root.mainloop()
