import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import glob, os
from datetime import datetime

# Dosya yolu
dosya_yolu = os.getcwd()

# Uygulama penceresi oluşturuluyor
app = tk.Tk()
app.title("Üretim Raporlama ve Operatör Veri Girişi")

# Verileri gösterme fonksiyonu (Okuma Uygulaması)
def verileri_goster():
    try:
        tum_dosyalar = glob.glob(os.path.join(dosya_yolu, "*.csv"))
        
        if not tum_dosyalar:
            messagebox.showwarning("Uyarı", "Klasörde veri bulunamadı!")
            return
        
        df_list = [pd.read_csv(dosya) for dosya in tum_dosyalar]
        tum_veriler = pd.concat(df_list, ignore_index=True)

        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, tum_veriler.to_string(index=False))

        global rapor_df
        rapor_df = tum_veriler

    except Exception as e:
        messagebox.showerror("Hata", f"Hata oluştu: {e}")

# Verileri dışarıya aktarma fonksiyonu (Okuma Uygulaması)
def disari_aktar():
    try:
        export_file = os.path.join(dosya_yolu, f"Toplu_Rapor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        rapor_df.to_excel(export_file, index=False)
        messagebox.showinfo("Başarılı", f"Veriler Excel'e aktarıldı:\n{export_file}")
    except Exception as e:
        messagebox.showerror("Hata", f"Hata oluştu: {e}")

# Operatör verisi kaydetme fonksiyonu (Operatör Uygulaması)
def veriyi_kaydet():
    try:
        makine_no = makine_no_entry.get()
        vardiya = vardiya_secim.get()
        lot_no = lot_entry.get()
        adet = int(adet_entry.get())
        gramaj = float(gramaj_entry.get())
        tarih_saat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        df = pd.DataFrame({
            "Tarih_Saat": [tarih_saat],
            "Makine_No": [makine_no],
            "Vardiya": [vardiya],
            "Lot_No": [lot_no],
            "Uretim_Adedi": [adet],
            "Gramaj": [gramaj]
        })

        dosya = os.path.join(dosya_yolu, f'Makine_{makine_no}.csv')

        if os.path.isfile(dosya):
            df.to_csv(dosya, mode='a', header=False, index=False)
        else:
            df.to_csv(dosya, mode='w', header=True, index=False)

        messagebox.showinfo("Başarılı", "Veriler kaydedildi!")
        lot_entry.delete(0, tk.END)
        adet_entry.delete(0, tk.END)
        gramaj_entry.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Hata", f"Hata oluştu: {e}")

# GUI elemanları (Okuma Uygulaması)
goster_btn = ttk.Button(app, text="Verileri Göster", command=verileri_goster)
goster_btn.pack(pady=10)

text_box = tk.Text(app, width=100, height=25)
text_box.pack(padx=10, pady=10)

export_btn = ttk.Button(app, text="Excel'e Aktar", command=disari_aktar)
export_btn.pack(pady=10)

# Operatör veri girişi GUI elemanları (Operatör Uygulaması)
tk.Label(app, text="Makine No:").pack(padx=10, pady=5)
makine_no_entry = ttk.Entry(app)
makine_no_entry.pack(padx=10, pady=5)

tk.Label(app, text="Vardiya:").pack(padx=10, pady=5)
vardiya_secim = ttk.Combobox(app, values=["07-15", "15-23", "23-07"])
vardiya_secim.pack(padx=10, pady=5)

tk.Label(app, text="Lot No:").pack(padx=10, pady=5)
lot_entry = ttk.Entry(app)
lot_entry.pack(padx=10, pady=5)

tk.Label(app, text="Üretim Adedi:").pack(padx=10, pady=5)
adet_entry = ttk.Entry(app)
adet_entry.pack(padx=10, pady=5)

tk.Label(app, text="Gramaj:").pack(padx=10, pady=5)
gramaj_entry = ttk.Entry(app)
gramaj_entry.pack(padx=10, pady=5)

kaydet_btn = ttk.Button(app, text="Kaydet", command=veriyi_kaydet)
kaydet_btn.pack(pady=10)

# Uygulama penceresini çalıştır
app.mainloop()
