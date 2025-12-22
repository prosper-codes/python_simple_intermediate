from fpdf import FPDF


class PDF(FPDF):
    
    def header(self):
          self.set_font("helvetica","",16)
          width = self.get_string_width(self.title)+6
          self.set_x((210-width)/2)
          self.set_draw_color(90,100,160)
          self.set_fill_color(50,20,210)
          self.set_text_color(0,0,0)
          self.set_line_width(1)
          self.cell(width,10,self.title,new_x="LMARGIN",new_y="NEXT",align="C",fill="True")
          self.ln(10)
          
    
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica","I",12)
        self.set_text_color(128)
        self.cell(0,10,f"Page {self.page_no()}", align="C")
    
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
pdf.set_title("Learn Hacking and Prosper")
pdf.print_chapter(1,"WHAT IS A HACKER","sample.txt")
pdf.output("demo.pdf")