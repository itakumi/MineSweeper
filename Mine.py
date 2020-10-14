import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
from tkinter import ttk
from functools import partial
import time
import os
import pickle
import socket
import threading
SizeOfSquares=24
RequiredExperiencePoint=[0,5,10,15,20,25,30,35,40,45,50,
                        55,60,65,70,75,80,85,90,95,100,
                        100,100,100,100,100,100,100,100,100,100,
                        100,100,100,100,100,100,100,100,100,100,
                        100,100,100,100,100,100,100,100,100,100,
                        100,100,100,100,100,100,100,100,100,100,
                        100,100,100,100,100,100,100,100,100,100,
                        100,100,100,100,100,100,100,100,100,100,
                        100,100,100,100,100,100,100,100,100,100,
                        100,100,100,100,100,100,100,100,100,9999,9999]
ConnectionData=[False,False,False] #s,Recv,Send
class EnemyInformation:
    bomblist=[]
    frame_list=[]
    remainbomb=None
    mistake_num=None
    enemygame_frame=None
    quitflag=False
    playtime,mistake_num,point=None,None,None
    def Initinfo(self):
        self.bomblist=[]
        self.frame_list=[]
        self.remainbomb=None
        self.mistake_num=None
        self.enemygame_frame=None
        self.quitflag=False
        self.playtime,self.mistake_num,self.point=None,None,None

enemyinfo=EnemyInformation()
class ClientSendThread(threading.Thread):
    data=None
    def __init__(self,data):
        self.data=data
        threading.Thread.__init__(self)
    def run(self):
        fromclient = pickle.dumps(self.data)
        ConnectionData[0].send(fromclient)
        if self.data=="quit":
            return
class ClientReceiveThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            msg = ConnectionData[0].recv(1024)
            full_msg = msg
            d = pickle.loads(full_msg)
            if d=='quit':
                return
            if ('event' in d) and ('isplaying' in d):
                enemyinfo.enemygame_frame.left_click(d['event'],d['isplaying'])
            elif 'continue' in d:
                if isinstance(d['continue'],int):
                    enemyinfo.enemygame_frame.frame_list[int(d['continue'])]['relief']='raised'
                    enemyinfo.enemygame_frame.frame_list[int(d['continue'])]['bd']=3
                    enemyinfo.enemygame_frame.frame_list[int(d['continue'])].configure(bg='LightGray')
                elif d['continue']=='giveup':
                    for i in enemyinfo.bomblist:
                        enemyinfo.enemygame_frame.frame_list[i].configure(bg = 'red')
                    enemyinfo.quitflag=True
            elif 'clear' in d:
                for i in enemyinfo.bomblist:
                    enemyinfo.enemygame_frame.frame_list[i].configure(bg = 'gold')
                enemyinfo.quitflag=True
            elif 'result' in d:
                enemyinfo.playtime,enemyinfo.mistake_num,enemyinfo.point=d['playtime'],d['mistake_num'],d['point']
            elif 'flagevent' in d:
                enemyinfo.enemygame_frame.right_click(d['flagevent'],enemyinfo.remainbomb)
def Newgame(root,event=None,width=None,height=None,num_bomb=None,UserData=None,isonline=False,fromcommand=False):
    if not isinstance(isonline,bool):
        isonline=isonline.get()
    if fromcommand and isonline==True:
        return
    root.destroy()
    main(width,height,num_bomb,UserData,isonline)
def WHBRead(root,master,WidthInput,HeightInput,BombInput,UserData):
    try:
        width=int(WidthInput.get())
        height=int(HeightInput.get())
        num_bomb=int(BombInput.get())
    except ValueError:
        messagebox.showinfo('エラー', 'それぞれの値は正の整数型にしてください')
        return
    if not (isinstance(width,int) and isinstance(height,int) and isinstance(num_bomb,int)):
        messagebox.showinfo('エラー', 'それぞれの値は正の整数型にしてください')
        return
    if not (width>0 and height>0,num_bomb>0):
        messagebox.showinfo('エラー', 'それぞれの値は正の整数型にしてください')
        return
    if width>50 or height>50:
        messagebox.showinfo('エラー', 'マス目が大きすぎます')
        return
    if width<4 or height<4:
        messagebox.showinfo('エラー', 'マス目が小さすぎます')
        return
    if num_bomb>=((width*height)-9):
        messagebox.showinfo('エラー', '地雷の数が多すぎます')
        return
    master.destroy()
    root.destroy()
    main(width,height,num_bomb,UserData)

def Customgame(root,UserData,isonline=False,fromcommand=False):
    if not isinstance(isonline,bool):
        isonline=isonline.get()
    if fromcommand and isonline==True:
        return
    master = Tk()
    master.title("幅、高さ、地雷の数を入力")

    Widthframe = ttk.Frame(master, padding=10)
    Widthframe.grid(row=1, column=0, sticky=E)
    WidthInputLabel = ttk.Label(Widthframe, text="Width=", padding=(5, 2))
    WidthInputLabel.pack(side=LEFT)
    WidthInput = tk.Entry(Widthframe,width=50)                   # widthプロパティで大きさを変える
    WidthInput.insert(tk.END, u'幅を入力')        # 最初から文字を入れておく
    WidthInput.pack(side=LEFT)

    Heightframe = ttk.Frame(master, padding=10)
    Heightframe.grid(row=2, column=0, sticky=E)
    HeightInputLabel = ttk.Label(Heightframe, text="Height=", padding=(5, 2))
    HeightInputLabel.pack(side=LEFT)
    HeightInput = tk.Entry(Heightframe,width=50)                   # widthプロパティで大きさを変える
    HeightInput.insert(tk.END, u'高さを入力')        # 最初から文字を入れておく
    HeightInput.pack(side=LEFT)

    Bombframe = ttk.Frame(master, padding=10)
    Bombframe.grid(row=3, column=0, sticky=E)
    BombInputLabel = ttk.Label(Bombframe, text="bomb=", padding=(5, 2))
    BombInputLabel.pack(side=LEFT)
    BombInput = tk.Entry(Bombframe,width=50)                   # widthプロパティで大きさを変える
    BombInput.insert(tk.END, u'地雷の数を入力')        # 最初から文字を入れておく
    BombInput.pack(side=LEFT)
    btnRead=tk.Button(master, height=1, width=10, text="OK",
                        command=partial(WHBRead,root=root,master=master,WidthInput=WidthInput,HeightInput=HeightInput,BombInput=BombInput,UserData=UserData))

    btnRead.grid(row=4, column=1, sticky=E)
    master.mainloop()
def SetSizeOfSquares(size,menu,sizebar):
    global SizeOfSquares
    sizebar.set(size)
    menu.entryconfigure(3,label = "マス目の大きさ("+str(sizebar.get())+")")
    SizeOfSquares=size
def setRule(root,master,WidthInput,HeightInput,BombInput,UserData):
    if isinstance(WidthInput,int):
        width,height,num_bomb=WidthInput,HeightInput,BombInput
        rule=dict(width=width,height=height,num_bomb=num_bomb)
        ConnectionData[2]=ClientSendThread(rule)
    else:
        try:
            width=int(WidthInput.get())
            height=int(HeightInput.get())
            num_bomb=int(BombInput.get())
        except ValueError:
            messagebox.showinfo('エラー', 'それぞれの値は正の整数型にしてください')
            return
        if not (isinstance(width,int) and isinstance(height,int) and isinstance(num_bomb,int)):
            messagebox.showinfo('エラー', 'それぞれの値は正の整数型にしてください')
            return
        if not (width>0 and height>0,num_bomb>0):
            messagebox.showinfo('エラー', 'それぞれの値は正の整数型にしてください')
            return
        if width>50 or height>50:
            messagebox.showinfo('エラー', 'マス目が大きすぎます')
            return
        if width<4 or height<4:
            messagebox.showinfo('エラー', 'マス目が小さすぎます')
            return
        if num_bomb>=((width*height)-9):
            messagebox.showinfo('エラー', '地雷の数が多すぎます')
            return
        rule=dict(width=width,height=height,num_bomb=num_bomb)
        ConnectionData[2]=ClientSendThread(rule)
    ConnectionData[2].start()
    master.destroy()
    messagebox.showinfo('ゲーム開始3秒前','お互いがOKした3秒後にゲームを開始します')
    full_msg = b''
    fromHostMessage=pickle.dumps(True)
    ConnectionData[0].send(fromHostMessage)
    msg = ConnectionData[0].recv(1024)
    full_msg = msg
    d = pickle.loads(full_msg)
    print("3秒後に開始")
    time.sleep(3)
    Newgame(root,width,height,num_bomb,UserData=UserData,isonline=True)

def ConnectByHost(root,UserData,isonline,room_num):
    if isonline.get():
        return
    ConnectionData[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ConnectionData[0].connect(("LAPTOP-KQ122Q8D", 50000+(2*room_num)))
    except ConnectionRefusedError:
        messagebox.showinfo('エラー', 'サーバーを立ててください')
        return
    full_msg = b''
    fromHostMessage=pickle.dumps(UserData)
    ConnectionData[0].send(fromHostMessage)
    try:
        msg = ConnectionData[0].recv(1024)
    except ConnectionResetError:
        messagebox.showinfo('エラー', 'ホストとメンバーは1名ずつです')
        return
    full_msg = msg
    d = pickle.loads(full_msg)
    messagebox.showinfo('マッチング成功！(ホスト)', '相手の情報\n'+str(d))
    full_msg = b''
    fromHostMessage=pickle.dumps(True)
    ConnectionData[0].send(fromHostMessage)
    msg = ConnectionData[0].recv(1024)
    full_msg = msg
    d = pickle.loads(full_msg)
    master = Tk()
    master.title("ルール設定")
    master.protocol('WM_DELETE_WINDOW', (lambda: 'pass')())
    EasyButton=tk.Button(master, height=1, width=10, text="初級(9*9(地雷数=10))",
                        command=partial(setRule,root=root,master=master,WidthInput=9,HeightInput=9,BombInput=10,UserData=UserData))
    EasyButton.grid(row=0, column=0, sticky=E)
    NormalButton=tk.Button(master, height=1, width=10, text="中級(16*16(地雷数=40))",
                        command=partial(setRule,root=root,master=master,WidthInput=16,HeightInput=16,BombInput=40,UserData=UserData))
    NormalButton.grid(row=0, column=1, sticky=E)
    HardButton=tk.Button(master, height=1, width=10, text="上級(30*16(地雷数=99))",
                        command=partial(setRule,root=root,master=master,WidthInput=30,HeightInput=16,BombInput=99,UserData=UserData))
    HardButton.grid(row=0, column=2, sticky=E)
    VeryHardButton=tk.Button(master, height=1, width=10, text="超上級(32*32(地雷数=199))",
                        command=partial(setRule,root=root,master=master,WidthInput=32,HeightInput=32,BombInput=199,UserData=UserData))
    VeryHardButton.grid(row=0, column=3, sticky=E)

    Widthframe = ttk.Frame(master, padding=10)
    Widthframe.grid(row=1, column=0, sticky=E)
    WidthInputLabel = ttk.Label(Widthframe, text="Width=", padding=(5, 2))
    WidthInputLabel.pack(side=LEFT)
    WidthInput = tk.Entry(Widthframe,width=50)                   # widthプロパティで大きさを変える
    WidthInput.insert(tk.END, u'幅を入力')        # 最初から文字を入れておく
    WidthInput.pack(side=LEFT)

    Heightframe = ttk.Frame(master, padding=10)
    Heightframe.grid(row=2, column=0, sticky=E)
    HeightInputLabel = ttk.Label(Heightframe, text="Height=", padding=(5, 2))
    HeightInputLabel.pack(side=LEFT)
    HeightInput = tk.Entry(Heightframe,width=50)                   # widthプロパティで大きさを変える
    HeightInput.insert(tk.END, u'高さを入力')        # 最初から文字を入れておく
    HeightInput.pack(side=LEFT)

    Bombframe = ttk.Frame(master, padding=10)
    Bombframe.grid(row=3, column=0, sticky=E)
    BombInputLabel = ttk.Label(Bombframe, text="bomb=", padding=(5, 2))
    BombInputLabel.pack(side=LEFT)
    BombInput = tk.Entry(Bombframe,width=50)                   # widthプロパティで大きさを変える
    BombInput.insert(tk.END, u'地雷の数を入力')        # 最初から文字を入れておく
    BombInput.pack(side=LEFT)
    btnRead=tk.Button(master, height=1, width=10, text="OK",
                        command=partial(setRule,root=root,master=master,WidthInput=WidthInput,HeightInput=HeightInput,BombInput=BombInput,UserData=UserData))
    btnRead.grid(row=4, column=1, sticky=E)
    master.mainloop()

def ConnectByMember(root,UserData,isonline,room_num):
    if isonline.get():
        return
    ConnectionData[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ConnectionData[0].connect(("LAPTOP-KQ122Q8D", 50000+(2*room_num)+1))
    except ConnectionRefusedError:
        messagebox.showinfo('エラー', 'サーバーを立ててください')
        return
    full_msg = b''
    fromMemberMessage=pickle.dumps(UserData)
    ConnectionData[0].send(fromMemberMessage)
    try:
        msg = ConnectionData[0].recv(1024)
    except ConnectionResetError:
        messagebox.showinfo('エラー', 'ホストとメンバーは1名ずつです')
        return
    full_msg = msg
    d = pickle.loads(full_msg)
    messagebox.showinfo('マッチング成功！(メンバー)', '相手の情報\n'+str(d))
    messagebox.showinfo('待機','ホストがルールを決めています')
    full_msg = b''
    fromHostMessage=pickle.dumps(True)
    ConnectionData[0].send(fromHostMessage)
    msg = ConnectionData[0].recv(1024)
    full_msg = msg
    d = pickle.loads(full_msg)
    msg = ConnectionData[0].recv(1024)
    full_msg = msg
    d = pickle.loads(full_msg)
    messagebox.showinfo('ルール情報','ルールは'+str(d))
    messagebox.showinfo('ゲーム開始3秒前','お互いがOKした3秒後にゲームを開始します')
    full_msg = b''
    fromHostMessage=pickle.dumps(True)
    ConnectionData[0].send(fromHostMessage)
    msg = ConnectionData[0].recv(1024)
    full_msg = msg
    d2 = pickle.loads(full_msg)
    print("3秒後に開始")
    time.sleep(3)
    Newgame(root,d['width'],d['height'],d['num_bomb'],UserData=UserData,isonline=True)

def main(width,height,num_bomb,UserData,isonline=False):
    class ClassFrame(tk.Frame):
        def __init__(self, master, bg=None,width=width,height=height):
            super().__init__(master, bg=bg, width=width, height=height)
    start=time.time()
    root=tk.Tk()
    isplaying=BooleanVar(root,value=True)
    isonlinevar=BooleanVar(root,value=isonline)
    mistake_num=IntVar(root,value=0)
    if isonlinevar.get():
        enemyinfo.mistake_num=IntVar(root,value=0)

    def RenewTime(TimeLabel,start):
        TimeLabel.configure(text=round(time.time()-start,1))
        if isplaying.get()==True:
            root.after(100,RenewTime,TimeLabel,start)
    if UserData['Level']==101:
        root.title("マインスイーパー"+"Lev:☆"+"("+str(UserData['Name'])+")")
    else:
        root.title("マインスイーパー"+"Lev:"+str(UserData['Level'])+"("+str(UserData['Name'])+")")
    menu_ROOT = Menu(root)
    root.configure(menu = menu_ROOT)
    remainbomb=IntVar(value=num_bomb)
    if isonlinevar.get():
        enemyinfo.remainbomb=IntVar(value=num_bomb)
        root.protocol('WM_DELETE_WINDOW', (lambda: 'pass')())
    menu_GAME = Menu(menu_ROOT, tearoff = False)
    menu_SizeOfSquares = Menu(menu_ROOT, tearoff = False)
    menu_DIFFICULTY = Menu(menu_ROOT, tearoff = False)
    menu_Online = Menu(menu_ROOT, tearoff = False)

    menu_ROOT.add_cascade(label = 'ゲーム', under = 4, menu = menu_GAME)
    menu_ROOT.add_cascade(label = '難易度選択', under = 4, menu = menu_DIFFICULTY)
    sizebar=IntVar(value=SizeOfSquares)
    menu_ROOT.add_cascade(label = "マス目の大きさ("+str(sizebar.get())+")", under = 3, menu = menu_SizeOfSquares)
    menu_SizeOfSquares.add_radiobutton(label = "極小", under = 3,command=partial(SetSizeOfSquares,14,menu=menu_ROOT,sizebar=sizebar),variable=sizebar,value=14)
    menu_SizeOfSquares.add_radiobutton(label = "小", under = 3,command=partial(SetSizeOfSquares,20,menu=menu_ROOT,sizebar=sizebar),variable=sizebar,value=20)
    menu_SizeOfSquares.add_radiobutton(label = "中", under = 3,command=partial(SetSizeOfSquares,24,menu=menu_ROOT,sizebar=sizebar),variable=sizebar,value=24)
    menu_SizeOfSquares.add_radiobutton(label = "大", under = 3,command=partial(SetSizeOfSquares,30,menu=menu_ROOT,sizebar=sizebar),value=30,variable=sizebar)
    menu_SizeOfSquares.add_radiobutton(label = "極大", under = 3,command=partial(SetSizeOfSquares,35,menu=menu_ROOT,sizebar=sizebar),value=35,variable=sizebar)

    menu_GAME.add_command(label = "新しいゲーム", under = 3,command=partial(Newgame,root,width=width,height=height,num_bomb=num_bomb,UserData=UserData,isonline=isonlinevar,fromcommand=True))
    menu_DIFFICULTY.add_command(label = "初級(9*9(地雷数=10))", under = 3,command=partial(Newgame,root,width=9,height=9,num_bomb=10,UserData=UserData,isonline=isonlinevar,fromcommand=True))
    menu_DIFFICULTY.add_command(label = "中級(16*16(地雷数=40))", under = 3,command=partial(Newgame,root,width=16,height=16,num_bomb=40,UserData=UserData,isonline=isonlinevar,fromcommand=True))
    menu_DIFFICULTY.add_command(label = "上級(30*16(地雷数=99))", under = 3,command=partial(Newgame,root,width=30,height=16,num_bomb=99,UserData=UserData,isonline=isonlinevar,fromcommand=True))
    menu_DIFFICULTY.add_command(label = "超上級(32*32(地雷数=199))", under = 3,command=partial(Newgame,root,width=32,height=32,num_bomb=199,UserData=UserData,isonline=isonlinevar,fromcommand=True))
    menu_DIFFICULTY.add_command(label = "カスタム", under = 3,command=partial(Customgame,root,UserData,isonline=isonlinevar,fromcommand=True))
    #menu_ROOT.add_command(label = "終了(X)", under = 3,command=lambda:root.destroy())
    menu_ROOT.add_cascade(label = '通信対戦', under = 4, menu = menu_Online)
    for i in range(10):
        second_menu=Menu(menu_Online,tearoff=0)
        menu_Online.add_cascade(label = 'Room'+str(i+1), under = 4,menu=second_menu)
        second_menu.add_command(label = "サーバーへ接続(ホスト)", under = 3,command=partial(ConnectByHost,root=root,UserData=UserData,isonline=isonlinevar,room_num=i))
        second_menu.add_command(label = "サーバーへ接続(メンバー)", under = 3,command=partial(ConnectByMember,root=root,UserData=UserData,isonline=isonlinevar,room_num=i))

    root_frame = Frame(root, relief = 'groove', borderwidth = 5, bg = 'LightGray')
    status_frame = Frame(root_frame, height = 50, relief = 'sunken', borderwidth = 3, bg = 'LightGray')

    BombNumLabel=Label(status_frame,text=remainbomb.get(),font=15)
    BombNumLabel.pack(side=tk.LEFT,anchor=tk.W,expand=1)
    NewGameButton=Button(status_frame,text="N",font=15,command=lambda:Newgame(root,width=width,height=height,num_bomb=num_bomb,UserData=UserData,isonline=isonlinevar,fromcommand=True))
    NewGameButton.pack(side=tk.LEFT,anchor='center',expand=1)
    root.bind("<Control-n>",partial(Newgame,root,width=width,height=height,num_bomb=num_bomb,UserData=UserData,isonline=isonlinevar,fromcommand=True))
    if isonlinevar.get():
        TimeLabel=Label(status_frame,text=0.0,font=15)
        TimeLabel.pack(side=tk.LEFT,anchor=tk.E,expand=1)
    else:
        TimeLabel=Label(status_frame,text=0.0,font=15)
        TimeLabel.pack(side=tk.LEFT,anchor=tk.E,expand=1)
    expscaleframe = ttk.Frame(status_frame)
    exp_label_0=tk.Label(expscaleframe, text="exp:")
    exp_label_0.pack(side=tk.LEFT)
    expval = IntVar(master=root,value=UserData['Exp'])
    expscalebar = tk.Scale(
        expscaleframe,
        state="disable",
        variable=expval,
        orient=HORIZONTAL,
        length=100,
        from_=0,
        to=RequiredExperiencePoint[UserData['Level']])
    expscalebar.pack(side=tk.LEFT)
    exp_label_100=tk.Label(expscaleframe, text=RequiredExperiencePoint[UserData['Level']])
    exp_label_100.pack(side=tk.RIGHT)
    expscaleframe.pack(side=tk.RIGHT)
    class ScrollFrame(ClassFrame):
        start=None
        def __init__(self, master, bg=None,isonlineenemy=False):
            super(ScrollFrame, self).__init__(master, bg=bg, width=width, height=height)

            # スクロールバーの作成
            self.isonlineenemy=isonlineenemy
            self.scroll_bar = tk.Scrollbar(self, orient=tk.VERTICAL)
            self.scroll_bar_H = tk.Scrollbar(self, orient=tk.HORIZONTAL)
            self.scroll_bar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
            self.scroll_bar_H.pack(fill=tk.X, side=tk.BOTTOM, expand=False)
            self.canvas = tk.Canvas(self, xscrollcommand=self.scroll_bar_H.set,yscrollcommand=self.scroll_bar.set)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scroll_bar.config(command=self.canvas.yview)
            self.scroll_bar_H.config(command=self.canvas.xview)
            self.width=width
            self.height=height

            # ビューをリセット
            self.canvas.xview_moveto(0)
            self.canvas.yview_moveto(0)

            self.interior = tk.Frame(self.canvas, bg="LightGray", borderwidth=10)
            self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)

            self.interior.bind('<Configure>', self.configure_interior)
            self.canvas.bind('<Configure>', self.configure_canvas)

            i = 0
            self.frame_list = []
            for x in range(height):
                for y in range(width):
                    frame = Frame(self.interior, width = (SizeOfSquares+2), height = (SizeOfSquares+2), bd = 3, relief = 'raised', bg = 'LightGray')
                    if not self.isonlineenemy:
                        frame.bind("<Button-1>", partial(self.left_click,isplaying=isplaying))
                    frame.bind("<MouseWheel>", self.mouse_y_scroll)
                    if not self.isonlineenemy:
                        frame.bind("<Button-3>", partial(self.right_click,remainbomb=remainbomb))
                    frame.num = i
                    self.frame_list.append(frame)
                    frame.grid(row=x, column=y)
                    i += 1
        def ShowEnemysResult(self):
            if (enemyinfo.playtime is not None) and (enemyinfo.mistake_num is not None) and (enemyinfo.point is not None):
                messagebox.showinfo('リザルト', 'あなたのリザルト\nプレイ時間:'+str(self.result['playtime'])+'\nミス数:'+str(self.result['mistake_num'])+'\nあなたの得点:'+str(self.result['point'])+"点"+'\n相手のリザルト'+'プレイ時間:'+str(enemyinfo.playtime)+'\nミス数:'+str(enemyinfo.mistake_num)+'\n相手の得点:'+str(enemyinfo.point)+"点")
                if self.result['point']>enemyinfo.point:
                    messagebox.showinfo('勝利！','勝利！')
                elif self.result['point']<enemyinfo.point:
                    messagebox.showinfo('敗北','敗北')
                else:
                    messagebox.showinfo('引き分け','引き分け')
                ConnectionData[2]=ClientSendThread('quit')
                ConnectionData[2].start()
                ConnectionData[1].join()
                isonlinevar.set(False)
                enemyinfo.Initinfo()
                root.protocol('WM_DELETE_WINDOW', (lambda:root.destroy()))
            else:
                root.after(100,self.ShowEnemysResult)
        def left_click(self,event,isplaying):
            if hasattr(event,'widget'):
                if hasattr(event.widget,'num'):
                    num=event.widget.num
                else:
                    num=event
            else:
                num=event
            if hasattr(isplaying,'get'):
                isplaying_boolean=isplaying.get()
            else:
                isplaying_boolean=isplaying
            if self.frame_list[num]['bg']=='Yellow':
                return
            if isonlinevar.get():
                if not self.isonlineenemy:
                    if len(bomb_list)!=0:
                        ConnectionData[2]=ClientSendThread(dict(event=num,isplaying=isplaying_boolean,isonlineenemy=self.isonlineenemy))
                        ConnectionData[2].start()
            if not self.frame_list[num]['bg']=='Yellow':
                except_num = num
                self.frame_list[num].configure(relief = 'ridge', bd = '1')
                if not self.isonlineenemy:
                    if len(bomb_list) == 0:
                        while len(bomb_list) != num_bomb:
                            bomb_num = random.randint(0,(width*height)-1)
                            if bomb_num != except_num and bomb_num != (except_num-(width+1)) and bomb_num != (except_num-width) and bomb_num != (except_num-(width-1)) and bomb_num != (except_num-1) and bomb_num != (except_num+1) and bomb_num != (except_num+(width+1)) and bomb_num != (except_num+width) and bomb_num != (except_num+(width-1)) and (bomb_num in bomb_list) == False:
                                bomb_list.append(bomb_num)
                        bomb_list.sort()
                        if not isonlinevar.get():
                            self.start = time.time()
                            RenewTime(TimeLabel,self.start)
                        if isonlinevar.get():
                            ConnectionData[2]=ClientSendThread(bomb_list)
                            ConnectionData[2].start()
                            msg = ConnectionData[0].recv(1024)
                            full_msg = msg
                            d = pickle.loads(full_msg)
                            enemyinfo.bomblist=d
                            ConnectionData[1]=ClientReceiveThread()
                            ConnectionData[1].start()
                            self.start = time.time()
                            RenewTime(TimeLabel,self.start)
                            if not self.isonlineenemy:
                                ConnectionData[2]=ClientSendThread(dict(event=event.widget.num,isplaying=isplaying.get(),isonlineenemy=self.isonlineenemy))
                                ConnectionData[2].start()

                    bomb_count = search_bomb(bomb_list, num)
                else:
                    if len(enemyinfo.bomblist) == 0:
                        while len(enemyinfo.bomblist) != num_bomb:
                            time.sleep(0.1)
                        enemyinfo.bomblist.sort()
                        self.start = time.time()
                        RenewTime(TimeLabel,self.start)
                    bomb_count = search_bomb(enemyinfo.bomblist, num)
                if  bomb_count == 9 :
                    self.frame_list[num].configure(bg='red', bd = '1')
                    if not self.isonlineenemy:
                        mistake_num.set(mistake_num.get()+1)
                        iscontinue=messagebox.askyesno('ゲームオーバー', '地雷を踏みました。コンテニューしますか？(ミス数:'+str(mistake_num.get())+')')
                        if iscontinue:
                            self.frame_list[num]['relief']='raised'
                            self.frame_list[num]['bd']=3
                            self.frame_list[num].configure(bg='LightGray')
                            if not self.isonlineenemy and isonlinevar.get():
                                ConnectionData[2]=ClientSendThread(dict([('continue',num)]))
                                ConnectionData[2].start()
                            return
                        else:
                            if not self.isonlineenemy:
                                for i in bomb_list:
                                    self.frame_list[i].configure(bg = 'red')
                            else:
                                for i in enemyinfo.bomblist:
                                    self.frame_list[i].configure(bg = 'red')
                            for i in self.frame_list:
                                i.bind("<1>", stop)
                                i.bind("<Button-3>", stop)
                            if not self.isonlineenemy and isonlinevar.get():
                                ConnectionData[2]=ClientSendThread(dict([('continue','giveup')]))
                                ConnectionData[2].start()
                            isplaying.set(False)
                            point=0
                            if (not self.isonlineenemy) and isonlinevar.get():
                                ConnectionData[2]=ClientSendThread(dict(result=True,playtime=int(time.time()-self.start),mistake_num=mistake_num.get(),point=point))
                                ConnectionData[2].start()
                            messagebox.showinfo('リザルト', "結果は...")
                            self.result=dict(playtime=int(time.time()-self.start),mistake_num=mistake_num.get(),point=point)
                            messagebox.showinfo('リザルト', 'あなたのリザルト\nプレイ時間:'+str(int(time.time()-self.start))+'\nミス数:'+str(mistake_num.get())+'\nあなたの得点:'+str(point)+"点")
                            if not self.isonlineenemy and isonlinevar.get():
                                root.after(100,self.ShowEnemysResult)
                            return
                    else:
                        enemyinfo.mistake_num.set(enemyinfo.mistake_num.get()+1)
                else:
                    if bomb_count!=0:
                        bomb_count_label = Label(self.frame_list[num], text = bomb_count, bg = 'LightGray')
                        bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
                    self.frame_list[num].bind("<Button-1>",stop)
                    self.frame_list[num].bind("<Button-3>",stop)
                    if bomb_count==0:
                        if not self.isonlineenemy:
                            zero_expantion(bomb_list,num,self.frame_list)
                        else:
                            zero_expantion(enemyinfo.bomblist,num,self.frame_list)
                remain_list=[i for i in range(len(self.frame_list)) if self.frame_list[i]['relief']=="raised"]
                if not self.isonlineenemy:
                    if set(remain_list)==set(bomb_list):
                        for i in self.frame_list:
                            i.bind("<1>", stop)
                            i.bind("<Button-3>", stop)
                        isplaying.set(False)
                        if not self.isonlineenemy and isonlinevar.get():
                            ConnectionData[2]=ClientSendThread(dict([('clear',True)]))
                            ConnectionData[2].start()
                        if not self.isonlineenemy:
                            for i in bomb_list:
                                self.frame_list[i].configure(bg = 'gold')
                        messagebox.showinfo('クリア！', 'ゲームクリア！')
                        point=int(((width*height)-mistake_num.get())/int(time.time()-self.start+1)*num_bomb)
                        if point<0:
                            point=0
                        if not self.isonlineenemy and isonlinevar.get():
                            ConnectionData[2]=ClientSendThread(dict(result=True,playtime=int(time.time()-self.start),mistake_num=mistake_num.get(),point=point))
                            ConnectionData[2].start()
                        messagebox.showinfo('リザルト', "結果は...")
                        self.result=dict(playtime=int(time.time()-self.start),mistake_num=mistake_num.get(),point=point)
                        messagebox.showinfo('リザルト', 'あなたのリザルト\nプレイ時間:'+str(int(time.time()-self.start))+'\nミス数:'+str(mistake_num.get())+'\nあなたの得点:'+str(point)+"点")
                        if not self.isonlineenemy and isonlinevar.get():
                            root.after(100,self.ShowEnemysResult)
                        counter_stop=False
                        while True:
                            if UserData['Level']==101:
                                counter_stop=True
                                break
                            if RequiredExperiencePoint[UserData['Level']]-UserData['Exp']<=point:
                                if UserData['Level']!=100:
                                    messagebox.showinfo('レベルアップ！',"Level:"+str(UserData['Level'])+"→"+str(UserData['Level']+1))
                                else:
                                    messagebox.showinfo('レベルアップ！',"Level:"+str(UserData['Level'])+"→☆")
                                point-=RequiredExperiencePoint[UserData['Level']]-UserData['Exp']
                                UserData['Exp']=0
                                UserData['Level']+=1
                                if UserData['Level']==100:
                                    messagebox.showinfo('レベル100！',"Level:100おめでとう🎉！！ここからはカンスト目指して頑張ろう！！")
                                if UserData['Level']==101:
                                    root.title("マインスイーパー"+"Lev:☆"+"("+str(UserData['Name'])+")")
                                    messagebox.showinfo('カンスト！',"あなたはまさにマインスイーパーの鬼です！")
                                    UserData['Exp']=9999
                                    expscalebar['variable']=IntVar(value=RequiredExperiencePoint[-1])
                                    counter_stop=True
                                    break
                                root.title("マインスイーパー"+"Lev:"+str(UserData['Level'])+"("+str(UserData['Name'])+")")
                                expscalebar['variable']=IntVar(value=0)
                                expscalebar['to']=RequiredExperiencePoint[UserData['Level']]
                                exp_label_100.configure(text=RequiredExperiencePoint[UserData['Level']])
                            elif RequiredExperiencePoint[UserData['Level']]-UserData['Exp']>point:
                                UserData['Exp']+=point
                                break
                        if not counter_stop:
                            root.title("マインスイーパー"+"Lev:"+str(UserData['Level'])+"("+str(UserData['Name'])+")")
                            val = IntVar(master=expscaleframe,value=UserData['Exp'])
                            expscalebar['variable']=val
                            expscalebar['to']=RequiredExperiencePoint[UserData['Level']]
                            exp_label_100.configure(text=RequiredExperiencePoint[UserData['Level']])
                            with open(basedirname+'/PickleData/UserInfomation_'+UserData['Name']+'.pickle','wb') as f:
                                pickle.dump(UserData,f)

        def right_click(self,event,remainbomb):
            if hasattr(event,'widget'):
                if hasattr(event.widget,'num'):
                    num=event.widget.num
                else:
                    num=event
            else:
                num=event
            if isonlinevar.get():
                if not self.isonlineenemy:
                    ConnectionData[2]=ClientSendThread(dict(flagevent=num,isonlineenemy=self.isonlineenemy))
                    ConnectionData[2].start()
            if self.frame_list[num]['bg']=="LightGray":
                self.frame_list[num]['bg']="Yellow"
                if not self.isonlineenemy:
                    remainbomb.set(remainbomb.get()-1)
                    BombNumLabel.configure(text=remainbomb.get())
                else:
                    enemyinfo.remainbomb.set(enemyinfo.remainbomb.get()-1)
                    #BombNumLabel.configure(text=enemyinfo.remainbomb.get())
            else:
                self.frame_list[num]['bg']="LightGray"
                if not self.isonlineenemy:
                    remainbomb.set(remainbomb.get()+1)
                    BombNumLabel.configure(text=remainbomb.get())
                else:
                    enemyinfo.remainbomb.set(enemyinfo.remainbomb.get()+1)
                    BombNumLabel.configure(text=enemyinfo.remainbomb.get())
        def configure_interior(self, event=None):
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion='0 0 {0} {1}'.format(size[0],size[1]))
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                if self.interior.winfo_reqwidth()+40<self.interior.winfo_screenwidth():
                    self.canvas.config(width=self.interior.winfo_reqwidth())
                else:
                    self.canvas.config(width=self.interior.winfo_screenwidth()-40)
            if self.interior.winfo_reqheight() != self.canvas.winfo_height():
                if self.interior.winfo_reqheight()+120<self.interior.winfo_screenheight():
                    self.canvas.config(height=self.interior.winfo_reqheight())
                else:
                    self.canvas.config(height=self.interior.winfo_screenheight()-200)

        def configure_canvas(self, event=None):
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                pass
        def mouse_y_scroll(self,event):
            if event.delta > 0:
                self.canvas.yview_scroll(-1, 'units')
            elif event.delta < 0:
                self.canvas.yview_scroll(1, 'units')

    canvas = tk.Canvas(root)
    game_frame=ScrollFrame(master=canvas)
    root_frame.pack()
    status_frame.pack(pady = 5, padx = 5, side=TOP,fill = tk.BOTH)
    game_frame.pack(pady = 5, padx = 5,side=LEFT,fill=tk.BOTH,expand=1)
    canvas.pack(fill=tk.BOTH,side=LEFT,expand=1)
    if isonlinevar.get():
        enemycanvas = tk.Canvas(root)
        enemyinfo.enemygame_frame=ScrollFrame(master=enemycanvas,isonlineenemy=True)
        enemyinfo.enemygame_frame.pack(pady = 5, padx = 5,side=RIGHT,fill=tk.BOTH,expand=1)
        enemycanvas.pack(fill=tk.BOTH,side=RIGHT,expand=1)



    bomb_list = []
    def zero_expantion(list,num,framelist):
        if num in list:
            return
        if num % width == 0:
            if num>=width:
                if framelist[num-width]['relief']=="raised":
                    if framelist[num-width]['bg']!='Yellow':
                        framelist[num-width].configure(relief = 'ridge', bd = '1')
                        framelist[num-width].bind("<Button-1>",stop)
                        framelist[num-width].bind("<Button-3>",stop)
                    if search_bomb(list,num-width)==0:
                        zero_expantion(list,num-width,framelist)
                    else:
                        if search_bomb(list,num-width)!=9 and framelist[num-width]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num-width], text = search_bomb(list,num-width), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num>=width:
                if framelist[num-(width-1)]['relief']=="raised":
                    if framelist[num-(width-1)]['bg']!='Yellow':
                        framelist[num-(width-1)].configure(relief = 'ridge', bd = '1')
                        framelist[num-(width-1)].bind("<Button-1>",stop)
                        framelist[num-(width-1)].bind("<Button-3>",stop)
                    if search_bomb(list,num-(width-1))==0:
                        zero_expantion(list,num-(width-1),framelist)
                    else:
                        if search_bomb(list,num-(width-1))!=9 and framelist[num-(width-1)]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num-(width-1)], text = search_bomb(list,num-(width-1)), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if framelist[num+1]['relief']=="raised":
                if framelist[num+1]['bg']!='Yellow':
                    framelist[num+1].configure(relief = 'ridge', bd = '1')
                    framelist[num+1].bind("<Button-1>",stop)
                    framelist[num+1].bind("<Button-3>",stop)
                if search_bomb(list,num+1)==0:
                    zero_expantion(list,num+1,framelist)
                else:
                    if search_bomb(list,num+1)!=9 and framelist[num+1]['bg']!='Yellow':
                        bomb_count_label = Label(framelist[num+1], text = search_bomb(list,num+1), bg = 'LightGray')
                        bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num<=((width*height)-(2*width)):
                if framelist[num+width]['relief']=="raised":
                    if framelist[num+width]['bg']!='Yellow':
                        framelist[num+width].configure(relief = 'ridge', bd = '1')
                        framelist[num+width].bind("<Button-1>",stop)
                        framelist[num+width].bind("<Button-3>",stop)
                    if search_bomb(list,num+width)==0:
                        zero_expantion(list,num+width,framelist)
                    else:
                        if search_bomb(list,num+width)!=9 and framelist[num+width]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num+width], text = search_bomb(list,num+width), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num<=((width*height)-(2*width)):
                if framelist[num+(width+1)]['relief']=="raised":
                    if framelist[num+(width+1)]['bg']!='Yellow':
                        framelist[num+(width+1)].configure(relief = 'ridge', bd = '1')
                        framelist[num+(width+1)].bind("<Button-1>",stop)
                        framelist[num+(width+1)].bind("<Button-3>",stop)
                    if search_bomb(list,num+(width+1))==0:
                        zero_expantion(list,num+(width+1),framelist)
                    else:
                        if search_bomb(list,num-(width+1))!=9 and framelist[num+(width+1)]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num+(width+1)], text = search_bomb(list,num+(width+1)), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
        elif (num % width) == (width-1):
            if num>=((2*width)-1):
                if framelist[num-(width+1)]['relief']=="raised":
                    if framelist[num-(width+1)]['bg']!='Yellow':
                        framelist[num-(width+1)].configure(relief = 'ridge', bd = '1')
                        framelist[num-(width+1)].bind("<Button-1>",stop)
                        framelist[num-(width+1)].bind("<Button-3>",stop)
                    if search_bomb(list,num-(width+1))==0:
                        zero_expantion(list,num-(width+1),framelist)
                    else:
                        if search_bomb(list,num-(width+1))!=9 and framelist[num-(width+1)]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num-(width+1)], text = search_bomb(list,num-(width+1)), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num>=((2*width)-1):
                if framelist[num-width]['relief']=="raised":
                    if framelist[num-width]['bg']!='Yellow':
                        framelist[num-width].configure(relief = 'ridge', bd = '1')
                        framelist[num-width].bind("<Button-1>",stop)
                        framelist[num-width].bind("<Button-3>",stop)
                    if search_bomb(list,num-width)==0:
                        zero_expantion(list,num-width,framelist)
                    else:
                        if search_bomb(list,num-width)!=9 and framelist[num-width]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num-width], text = search_bomb(list,num-width), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if framelist[num-1]['relief']=="raised":
                if framelist[num-1]['bg']!='Yellow':
                    framelist[num-1].configure(relief = 'ridge', bd = '1')
                    framelist[num-1].bind("<Button-1>",stop)
                    framelist[num-1].bind("<Button-3>",stop)
                if search_bomb(list,num-1)==0:
                    zero_expantion(list,num-1,framelist)
                else:
                    if search_bomb(list,num-1)!=9 and framelist[num-1]['bg']!='Yellow':
                        bomb_count_label = Label(framelist[num-1], text = search_bomb(list,num-1), bg = 'LightGray')
                        bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num<=((width*height)-width-1):
                if framelist[num+(width-1)]['relief']=="raised":
                    if framelist[num+(width-1)]['bg']!='Yellow':
                        framelist[num+(width-1)].configure(relief = 'ridge', bd = '1')
                        framelist[num+(width-1)].bind("<Button-1>",stop)
                        framelist[num+(width-1)].bind("<Button-3>",stop)
                    if search_bomb(list,num+(width-1))==0:
                        zero_expantion(list,num+(width-1),framelist)
                    else:
                        if search_bomb(list,num+(width-1))!=9 and framelist[num+(width-1)]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num+(width-1)], text = search_bomb(list,num+(width-1)), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num<=((width*height)-width-1):
                if framelist[num+width]['relief']=="raised":
                    if framelist[num+width]['bg']!='Yellow':
                        framelist[num+width].configure(relief = 'ridge', bd = '1')
                        framelist[num+width].bind("<Button-1>",stop)
                        framelist[num+width].bind("<Button-3>",stop)
                    if search_bomb(list,num+width)==0:
                        zero_expantion(list,num+width,framelist)
                    else:
                        if search_bomb(list,num+width)!=9 and framelist[num+width]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num+width], text = search_bomb(list,num+width), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
        else:
            if num>=(width+1):
                if framelist[num-(width+1)]['relief']=="raised":
                    if framelist[num-(width+1)]['bg']!='Yellow':
                        framelist[num-(width+1)].configure(relief = 'ridge', bd = '1')
                        framelist[num-(width+1)].bind("<Button-1>",stop)
                        framelist[num-(width+1)].bind("<Button-3>",stop)
                    if search_bomb(list,num-(width+1))==0:
                        zero_expantion(list,num-(width+1),framelist)
                    else:
                        if search_bomb(list,num-(width+1))!=9 and framelist[num-(width+1)]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num-(width+1)], text = search_bomb(list,num-(width+1)), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num>=(width+1):
                if framelist[num-width]['relief']=="raised":
                    if framelist[num-width]['bg']!='Yellow':
                        framelist[num-width].configure(relief = 'ridge', bd = '1')
                        framelist[num-width].bind("<Button-1>",stop)
                        framelist[num-width].bind("<Button-3>",stop)
                    if search_bomb(list,num-width)==0:
                        zero_expantion(list,num-width,framelist)
                    else:
                        if search_bomb(list,num-width)!=9 and framelist[num-width]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num-width], text = search_bomb(list,num-width), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num>=(width+1):
                if framelist[num-(width-1)]['relief']=="raised":
                    if framelist[num-(width-1)]['bg']!='Yellow':
                        framelist[num-(width-1)].configure(relief = 'ridge', bd = '1')
                        framelist[num-(width-1)].bind("<Button-1>",stop)
                        framelist[num-(width-1)].bind("<Button-3>",stop)
                    if search_bomb(list,num-(width-1))==0:
                        zero_expantion(list,num-(width-1),framelist)
                    else:
                        if search_bomb(list,num-(width-1))!=9 and framelist[num-(width-1)]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num-(width-1)], text = search_bomb(list,num-(width-1)), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num>=1:
                if framelist[num-1]['relief']=="raised":
                    if framelist[num-1]['bg']!='Yellow':
                        framelist[num-1].configure(relief = 'ridge', bd = '1')
                        framelist[num-1].bind("<Button-1>",stop)
                        framelist[num-1].bind("<Button-3>",stop)
                    if search_bomb(list,num-1)==0:
                        zero_expantion(list,num-1,framelist)
                    else:
                        if search_bomb(list,num-1)!=9 and framelist[num-1]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num-1], text = search_bomb(list,num-1), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num<=((width*height)-2):
                if framelist[num+1]['relief']=="raised":
                    if framelist[num+1]['bg']!='Yellow':
                        framelist[num+1].configure(relief = 'ridge', bd = '1')
                        framelist[num+1].bind("<Button-1>",stop)
                        framelist[num+1].bind("<Button-3>",stop)
                    if search_bomb(list,num+1)==0:
                        zero_expantion(list,num+1,framelist)
                    else:
                        if search_bomb(list,num+1)!=9 and framelist[num+1]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num+1], text = search_bomb(list,num+1), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num<=((width*height)-width-2):
                if framelist[num+(width-1)]['relief']=="raised":
                    if framelist[num+(width-1)]['bg']!='Yellow':
                        framelist[num+(width-1)].configure(relief = 'ridge', bd = '1')
                        framelist[num+(width-1)].bind("<Button-1>",stop)
                        framelist[num+(width-1)].bind("<Button-3>",stop)
                    if search_bomb(list,num+(width-1))==0:
                        zero_expantion(list,num+(width-1),framelist)
                    else:
                        if search_bomb(list,num+(width-1))!=9 and framelist[num+(width-1)]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num+(width-1)], text = search_bomb(list,num+(width-1)), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num<=((width*height)-width-2):
                if framelist[num+width]['relief']=="raised":
                    if framelist[num+width]['bg']!='Yellow':
                        framelist[num+width].configure(relief = 'ridge', bd = '1')
                        framelist[num+width].bind("<Button-1>",stop)
                        framelist[num+width].bind("<Button-3>",stop)
                    if search_bomb(list,num+width)==0:
                        zero_expantion(list,num+width,framelist)
                    else:
                        if search_bomb(list,num+width)!=9 and framelist[num+width]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num+width], text = search_bomb(list,num+width), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)
            if num<=((width*height)-width-2):
                if framelist[num+(width+1)]['relief']=="raised":
                    if framelist[num+(width+1)]['bg']!='Yellow':
                        framelist[num+(width+1)].configure(relief = 'ridge', bd = '1')
                        framelist[num+(width+1)].bind("<Button-1>",stop)
                        framelist[num+(width+1)].bind("<Button-3>",stop)
                    if search_bomb(list,num+(width+1))==0:
                        zero_expantion(list,num+(width+1),framelist)
                    else:
                        if search_bomb(list,num+(width+1))!=9 and framelist[num+(width+1)]['bg']!='Yellow':
                            bomb_count_label = Label(framelist[num+(width+1)], text = search_bomb(list,num+(width+1)), bg = 'LightGray')
                            bomb_count_label.place(width = SizeOfSquares, height = SizeOfSquares)

    def search_bomb(list, num):
        around_list = []
        bomb_count = 0
        if num in list:
            return 9
        if num % width == 0:
            around_list.append(num-width)
            around_list.append(num-(width-1))
            around_list.append(num+1)
            around_list.append(num+width)
            around_list.append(num+(width+1))
        elif num % width == (width-1):
            around_list.append(num-(width+1))
            around_list.append(num-width)
            around_list.append(num-1)
            around_list.append(num+(width-1))
            around_list.append(num+width)
        elif num < width:
            around_list.append(num-1)
            around_list.append(num+1)
            around_list.append(num+(width-1))
            around_list.append(num+width)
            around_list.append(num+(width+1))
        elif num > ((width*height)-width):
            around_list.append(num-(width+1))
            around_list.append(num-width)
            around_list.append(num-(width-1))
            around_list.append(num-1)
            around_list.append(num+1)
        else:
            around_list.append(num-(width+1))
            around_list.append(num-width)
            around_list.append(num-(width-1))
            around_list.append(num-1)
            around_list.append(num+1)
            around_list.append(num+(width-1))
            around_list.append(num+width)
            around_list.append(num+(width+1))
        for i in around_list:
            if i in list:
                bomb_count += 1
        return bomb_count
    def stop(event):
        pass
    start = time.time()
    root.mainloop()
def UserRead(event=None,root=None,UserInput=None):
    if root==None or UserInput==None:
        return
    UserName=UserInput.get()
    if not os.path.isdir(basedirname+'/PickleData'):
        os.mkdir(basedirname+'/PickleData')
    if os.path.exists(basedirname+"/PickleData/UserInfomation_"+UserName+".pickle"):
        with open(basedirname+'/PickleData/UserInfomation_'+UserName+'.pickle', 'rb') as f:
            UserData=pickle.load(f)
        root.destroy()
        main(9,9,10,UserData)
    else:
        iscreate=messagebox.askyesno('ユーザー作成', '新しいユーザーを作成します。よろしいですか？')
        if iscreate:
            UserData=dict(Name=UserName,Level=1,Exp=0)#,'Totalexp'=0)
            with open(basedirname+'/PickleData/UserInfomation_'+UserData['Name']+'.pickle','wb') as f:
                pickle.dump(UserData,f)
            root.destroy()
            main(9,9,10,UserData)

if __name__ == "__main__":
    basedirname=os.path.dirname(os.path.abspath("__file__"))
    Usertk=tk.Tk()
    Usertk.title("User名を入力(ない場合は作成)")
    Userframe = ttk.Frame(Usertk, padding=10)
    Userframe.grid(row=3, column=0, sticky=E)
    UserInputLabel = ttk.Label(Userframe, text="User名:", padding=(5, 2))
    UserInputLabel.pack(side=LEFT)
    UserInput = tk.Entry(Userframe,width=50)                   # widthプロパティで大きさを変える
    UserInput.insert(tk.END, u'User名を入力')        # 最初から文字を入れておく
    UserInput.pack(side=LEFT)
    UserReadbtn=tk.Button(Usertk, height=1, width=10, text="OK",
                        command=partial(UserRead,root=Usertk,UserInput=UserInput))
    UserReadbtn.grid(row=4, column=1, sticky=E)
    Usertk.bind("<Return>",partial(UserRead,root=Usertk,UserInput=UserInput))
    Usertk.mainloop()
