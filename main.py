import customtkinter as ctk
import eliza
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("ELIZA APP")
        self.wm_resizable(width = False, height = False)
        
        self.labelmenue = ctk.CTkLabel(self, text = "ELIZA", font = ctk.CTkFont("Arial BLACK"))
        self.optionmenue = ctk.CTkOptionMenu(self,values = ["glove", "enwiki"], anchor = "w", 
                                             font = ctk.CTkFont("Arial"))
        self.target = ctk.CTkOptionMenu(self,values = os.listdir("Initializer\\Target"), anchor = "w", 
                                             font = ctk.CTkFont("Arial"), command = self.target_call_back)
        self.target.set("doctor.txt")
        self.weighted = ctk.CTkSwitch(self, text = "Pondérer", font = ctk.CTkFont("Arial"))
        
        self.seuil = ctk.CTkEntry(self, placeholder_text = "Seuil", font = ctk.CTkFont("Arial"))
        self.labelsubmenue = ctk.CTkLabel(self, text = "Show", font = ctk.CTkFont("Arial BLACK"))
        self.log = ctk.CTkCheckBox(self, text = "logging", font = ctk.CTkFont("Arial"))
        
        self.matchlog = ctk.CTkCheckBox(self, text = "matching", font = ctk.CTkFont("Arial"))
        self.synonlog = ctk.CTkCheckBox(self, text = "synonlog", font = ctk.CTkFont("Arial"))
        self.confirm = ctk.CTkButton(self, text = "ELIZA", font = ctk.CTkFont("Arial BLACK"), fg_color = "darkgreen",
                                     command = self.eliza_call_back)
        self.final = ctk.CTkButton(self, text = "Quitter", command = self.final_call_back,
                                     font = ctk.CTkFont("Arial BLACK"), fg_color = "darkred")
        
        self.synonextend = ctk.CTkCheckBox(self, text = "SynonExtend", font = ctk.CTkFont("Arial"), fg_color="darkorange")
        
        self.labelmenue.pack()
        self.optionmenue.pack()
        self.target.pack()
        self.seuil.pack()
        
        self.weighted.pack()
        self.labelsubmenue.pack()
        self.log.pack()
        self.matchlog.pack()
        self.synonlog.pack()
        self.synonextend.pack()
        
        self.confirm.pack()
        self.final.pack()
        
        self.toplevel = None
        
    def final_call_back(self):
        self.destroy()
    
    def target_call_back(self, buffer):
        if self.target.get().startswith("SE"):
            self.synonextend.select()
        else:
            self.synonextend.deselect()
    
    def eliza_call_back(self):
        if self.seuil.get() == "":
            seuil = 0
        else:
            try:
                seuil = float(self.seuil.get())
                eliza.main(WEdict = self.optionmenue.get(), SEUIL = seuil, WEIGHTED = bool(self.weighted.get()),
                           LOG = bool(self.log.get()), MATCHLOGS = bool(self.matchlog.get()),
                           TARGET = self.target.get(), SYNON_EXTENT = bool(self.synonextend.get()),
                           SYNONLOGS = bool(self.synonlog.get()))
            except:
                if input("Error : do you want to restart ? (y/n) : ") == "y":
                    self.eliza_call_back()
        
    
    
app = App()
app.mainloop()