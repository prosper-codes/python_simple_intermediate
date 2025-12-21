from fpdf import FPDF


class PDF(FPDF):
    
    def header(self):
        return super().header()
    
    def footer(self):
        return super().footer()
    
    def chapter_title(self, num , label):
        self.set_font("Arial","",13)
        self.set_fill_color(255,100,220,)
        self.cell(0,6,f"Chapter {num} : {label}", new_x= "LMARGIN", new_y ="NEXT",align ="L", fill =True)
    
    def chapter_body(self,filepath):
        with open(filepath,"rb")as fh:
            txt=fh.read().decode("latin-1")
        self.set_font("Times",size=13)
        self.multi_cell(0,5,txt)
        self.ln()
        self.set_font(style="I")
        self.cell(0,5,"===================")
       
    
    def print_chapter(self,num , title, filepath):
        
        self.add_page()
        self.chapter_title(num,title)
        self.chapter_body(filepath)
        pass
    


pdf= PDF()

pdf.print_chapter(1,"WHAT IS A HACKER","sample.txt")
pdf.output("demo.pdf",)