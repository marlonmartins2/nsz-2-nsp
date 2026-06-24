import sys
# Interceptador para rodar o NSZ nativamente no mesmo executável empacotado
if len(sys.argv) > 1 and ("NSZ_RUNNER_MODE" in sys.argv or any("multiprocessing-fork" in arg for arg in sys.argv)):
    import multiprocessing
    import nsz
    multiprocessing.freeze_support()
    
    if "NSZ_RUNNER_MODE" in sys.argv:
        sys.argv.remove("NSZ_RUNNER_MODE")
        sys.exit(nsz.main())

import customtkinter as ctk
from tkinter import filedialog
import os
from converter import convert_nsz_to_nsp

# Appearance setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("NSZ Converter Desktop")
        self.geometry("600x400")
        self.resizable(False, False)
        
        self.input_file = None
        self.output_dir = None
        
        # --- UI Elements ---
        
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="NSZ Converter", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 30))
        
        # Input Section
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        self.input_btn = ctk.CTkButton(self.input_frame, text="Selecionar NSZ", command=self.select_input)
        self.input_btn.pack(side="left")
        
        self.input_label = ctk.CTkLabel(self.input_frame, text="Nenhum arquivo selecionado", text_color="gray")
        self.input_label.pack(side="left", padx=15)
        
        # Output Section
        self.output_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.output_frame.pack(fill="x", padx=40, pady=(0, 30))
        
        self.output_btn = ctk.CTkButton(self.output_frame, text="Pasta de Saída", command=self.select_output)
        self.output_btn.pack(side="left")
        
        self.output_label = ctk.CTkLabel(self.output_frame, text="Nenhuma pasta selecionada", text_color="gray")
        self.output_label.pack(side="left", padx=15)
        
        # Convert Button
        self.convert_btn = ctk.CTkButton(self, text="CONVERTER PARA NSP", 
                                         font=ctk.CTkFont(size=16, weight="bold"), 
                                         height=50, 
                                         command=self.start_conversion,
                                         state="disabled")
        self.convert_btn.pack(fill="x", padx=40, pady=(10, 20))
        
        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Aguardando arquivos...", text_color="gray")
        self.status_label.pack(pady=(0, 20))

    def select_input(self):
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo NSZ",
            filetypes=[("Arquivos NSZ", "*.nsz")]
        )
        if filename:
            self.input_file = filename
            self.input_label.configure(text=os.path.basename(filename), text_color="white")
            self.check_ready()

    def select_output(self):
        dirname = filedialog.askdirectory(title="Selecione a pasta de destino")
        if dirname:
            self.output_dir = dirname
            self.output_label.configure(text=dirname, text_color="white")
            self.check_ready()

    def check_ready(self):
        if self.input_file and self.output_dir:
            self.convert_btn.configure(state="normal")
            self.status_label.configure(text="Pronto para converter!")

    def update_status(self, message):
        # Update UI safely from another thread
        self.after(0, lambda: self.status_label.configure(text=message, text_color="orange"))

    def on_conversion_success(self):
        self.after(0, lambda: self.status_label.configure(text="Conversão concluída com sucesso!", text_color="green"))
        self.after(0, lambda: self.convert_btn.configure(state="normal"))

    def on_conversion_error(self, err_msg):
        self.after(0, lambda: self.status_label.configure(text=f"Erro: {err_msg}", text_color="red"))
        self.after(0, lambda: self.convert_btn.configure(state="normal"))

    def start_conversion(self):
        if not self.input_file or not self.output_dir:
            return
            
        self.convert_btn.configure(state="disabled")
        self.status_label.configure(text="Iniciando...", text_color="orange")
        
        convert_nsz_to_nsp(
            self.input_file, 
            self.output_dir, 
            self.update_status, 
            self.on_conversion_success, 
            self.on_conversion_error
        )

if __name__ == "__main__":
    app = App()
    app.mainloop()
