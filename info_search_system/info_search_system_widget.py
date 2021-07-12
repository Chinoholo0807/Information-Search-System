from info_search_system import InfoSystem
from tkinter import *


class Widget:
    def __init__(self):
        self.system = InfoSystem()
        self.results = []
        self.i_result = 0

        self.mainWidget = Tk()
        self.mainWidget.title("Info Search System")
        widgetHeight = 600
        widgetWidth = 600
        screenWidth = self.mainWidget.winfo_screenwidth()
        screenHeight = self.mainWidget.winfo_screenheight()
        alignStr = '%dx%d+%d+%d' % (widgetWidth,
                                    widgetHeight,
                                    (screenWidth - widgetWidth) / 2,
                                    (screenHeight - widgetWidth) / 2)
        self.mainWidget.geometry(alignStr)
        self.mainWidget.resizable(False, False)
        canvas = Canvas(self.mainWidget, height=widgetHeight, width=widgetWidth)
        canvas.place(x=0,y=0)
        bg = PhotoImage(file='bg.jpg')
        bgImage = canvas.create_image(0, 0, image=bg, anchor='nw')
        labelInput=canvas.create_text((50,25),text="Input",font="微软雅黑 10 ")
        labelOutput=canvas.create_text((50,58),text="Output",font="微软雅黑 10 ")

        self.entryInput = Entry(self.mainWidget,
                                font=('微软雅黑', 10),
                                bd=0)
        self.entryInput.place(x=80,
                              y=10,
                              width=360,
                              height=30)
        self.textOutput = Text(self.mainWidget,
                               font=('微软雅黑', 10),
                               bd=0
                               )
        self.textOutput.place(x=80,
                              y=50,
                              width=360,
                              height=450,
                              )
        self.btnSearch = Button(self.mainWidget,
                                text='Search',
                                bg='pink',
                                bd=0,
                                command=self.btnSearchClicked)
        self.btnSearch.place(x=470,
                             y=10,
                             width=100,
                             height=30)
        self.btnNext = Button(self.mainWidget,
                              text='Next',
                              bg='pink',
                              # relief='raised',
                              bd=0,
                              command=self.btnNextClicked)
        self.btnNext.place(x=470,
                           y=250,
                           width=100,
                           height=30)
        self.btnPrev = Button(self.mainWidget,
                              text='Prev',
                              bg='pink',
                              relief='raised',
                              bd=0,
                              command=self.btnPrevClicked)
        self.btnPrev.place(x=470,
                           y=300,
                           width=100,
                           height=30)

        self.labelCount = Label(self.mainWidget,
                                text="Result:-/-",
                                font="微软雅黑 10 ",
                                bg='white')
        self.labelCount.place(x=470,
                              y=180,
                              width=100,
                              height=30)
        self.mainWidget.mainloop()

    def btnSearchClicked(self):
        print("btnSearchClicked.")
        input_str = str(self.entryInput.get())
        print("input :", input_str)
        self.textOutput.delete(1.0, END)
        self.results = self.system.search(input_str)
        if len(self.results) == 0:  # 查询到结果
            self.textOutput.insert('end', "Sorry , can't find the result...")
            self.labelCount.config(text='Result:-/-')
        else:
            self.i_result = 0
            self.textOutput.insert('end', str(self.results[self.i_result]))
            self.labelCount.config(text='Result:%d/%d' % (self.i_result + 1, len(self.results)))

    def btnNextClicked(self):
        print("btnNextClicked.")
        if self.i_result < len(self.results) - 1 and len(self.results) > 0:
            self.textOutput.delete(1.0, END)
            self.i_result = self.i_result + 1
            print('i_result: ', self.i_result)
            self.textOutput.insert('end', str(self.results[self.i_result]))
            self.labelCount.config(text='Result:%d/%d' % (self.i_result + 1, len(self.results)))

    def btnPrevClicked(self):
        print("btnPrevClicked.")
        if self.i_result > 0 and len(self.results) > 0:
            self.textOutput.delete(1.0, END)
            self.i_result = self.i_result - 1
            print('i_result: ', self.i_result)
            self.textOutput.insert('end', str(self.results[self.i_result]))
            self.labelCount.config(text='Result:%d/%d' % (self.i_result + 1, len(self.results)))

