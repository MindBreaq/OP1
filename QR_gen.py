import qrcode
import cv2 as cv
import numpy as np
from fpdf import FPDF
import tkinter as tk

class GUI:      ## interaction with user
    num = []
    def __init__(self):
        pass

    def run(self):      ## function sequention
        self.root = self.make_root()
        self.name_entry = self.make_label()
        self.make_submit()
        self.root.mainloop()

    def make_root(self):        ## window creating
        root = tk.Tk()
        root.title("QR code generator")
        root.geometry('350x100')
        root.configure(background='#303030')
        return root

    def make_label(self):       ## adding labels and enter fields
        name_label = tk.Label(self.root, text="Enter number of QR codes:")
        name_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")
        name_entry = tk.Entry(self.root, justify="center")
        name_entry.grid(row=0, column=1, padx=20, pady=0)
        return name_entry

    def make_submit(self):      ## adding submit button
        submit_button = tk.Button(self.root, text="Submit", command=self.get_submit)
        submit_button.grid(row=2, column=1, padx=60, pady=0, sticky="e")

    def get_submit(self):       ## getting input into program
        num = self.name_entry.get()
        num = int(num)
        GUI.num.append(num)
        self.root.destroy()
        

class QR_GEN:       ## QR code generation
    qrs = []
    def __init__(self, place, row, type, id):        ## input vars
        self.place = place
        self.row = row
        self.type = type
        self.id = id

    def run(self):      ## function sequention
        for i in range(1, self.row + 1):
            for j in range(1, self.id + 1):
                for k in range(2):
                    if k == 0:
                        side = "L"
                    else:
                        side = "R"
                    self.data = self.place + "{:02d}".format(i) + side + self.type + "{:03d}".format(j)
                    self.qr_img = self._qr_gen()  
                    self.white = self._num_img()
                    self.join = self._qr_join_num()
                    self.qr_brd = self._qr_bord()
                    self.end = self._qr_out()
    
    def _qr_gen(self):      ## creatin QR code as an array
        qr = qrcode.QRCode(version=1, box_size=20, border=2)
        qr.add_data(self.data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = np.asarray(qr_img, dtype="uint8")*255
        return qr_img

    def _num_img(self):     ## adding visual number label
        white = np.ones((100, self.qr_img.shape[1]), dtype=np.uint8) * 255
        font = cv.FONT_HERSHEY_DUPLEX 
        font_scale = 2
        text_size, _ = cv.getTextSize(str(self.data), font, font_scale, thickness=5)
        text_x = int((white.shape[1] - text_size[0]) / 2)
        text_y = int((white.shape[0] + text_size[1]) / 2)
        cv.putText(white, str(self.data), (text_x, text_y), font, font_scale, (0, 0, 0), thickness=5)
        white = np.reshape(white, (100, self.qr_img.shape[1]))
        return white

    def _qr_join_num(self):     ## joining QR and label
        join = cv.vconcat([self.qr_img, self.white])
        return join

    def _qr_bord(self):     ## adding border for better recognition
        qr_brd = cv.rectangle(self.join, (1,1), (self.join.shape[1]-1, self.join.shape[0]-1), (0,0,0), 1)
        return qr_brd
            
    def _qr_out(self):      ## output of generated QR codes
        # cv.imwrite("pngs\{self.data}.png", self.qr_brd)
        # cv.imshow("pngs\{self.data}", self.qr_brd)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        QR_GEN.qrs.append(self.qr_brd)


class pdf(QR_GEN):      ## pdf generator
    def __init__(self):
        pass

    def run(self):      ## function sequention
        self.pdf, self.void, self.void2 = self.supp()
        self.hor = self.horizontal_merge()
        for i in range(0,len(self.hor),2):
            self.i = i
            self.ver_merg = self.vertical_merge()
            self.make()
        self.out()

    def supp(self):     ## support function
        pdf = FPDF()
        void = np.ones(self.qrs[0].shape, dtype=int)*255
        void2 = np.concatenate((void, void), axis=1)
        return pdf, void, void2

    def horizontal_merge(self):     ## horizontal merging of QRs
        hor = []
        for i in range(0,len(self.qrs),2):
            if i+1 == len(self.qrs):
                hor_merg = np.concatenate((self.qrs[i], self.void), axis=1)
                hor.append(hor_merg)
            else:
                hor_merg = np.concatenate((self.qrs[i], self.qrs[i+1]), axis=1)
                hor.append(hor_merg)
        return hor

    def vertical_merge(self):       ## vertical merging of QRs
        if self.i+1 == len(self.hor):
            ver_merg = np.concatenate((self.hor[self.i], self.void2), axis=0)
        else:
            ver_merg = np.concatenate((self.hor[self.i], self.hor[self.i+1]), axis=0)
        return ver_merg
            
    def make(self):     ## generation of pages of PDF
        cv.imwrite("pngs\QR{:01d}_pdf.png".format(int(1+self.i/2)), self.ver_merg)
        self.pdf.add_page()
        self.pdf.image("pngs\QR{:01d}_pdf.png".format(int(1+self.i/2)), x=10, y=10, w=190, h=228)

    def out(self):      ## saving of PDF
        self.pdf.output('PDF_QRS.pdf', 'F')


## sequention of classes
# GUI().run()
QR_GEN("T", 2, "C", 5).run()
pdf().run()