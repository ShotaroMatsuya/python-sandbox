import os
from tkinter import StringVar, Tk, filedialog, messagebox, ttk


# フォルダ指定の関数
def dir_dialog_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir=iDir)
    entry1.set(iDirPath)


# ファイル指定の関数
def filedialog_clicked():
    f = __file__
    open(f)
    iFile = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(iDirPath/iFile)
    iFilePath = filedialog.askopenfilename(initialdir=iFile)
    entry2.set(iFilePath)


# 実行ボタン押下時の実行関数
def conductMain():
    text = ""
    dirPath = entry1.get()
    filePath = entry2.get()
    if dirPath:
        text += "フォルダパス：" + dirPath + "\n"
    if filePath:
        text += "ファイルパス：" + filePath + "\n"
    if text:
        messagebox.showinfo("info", dirPath + "に" + filePath + "ファイルを作成しました")
        os.mkdir(dirPath + "/" + filePath)
    else:
        messagebox.showerror("error", "パスの指定がありません。")


if __name__ == "__main__":
    # rootの作成
    root = Tk()
    root.title("フォルダ／ファイル指定")
    # Frame1の作成
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid(row=0, column=1, sticky=["e"])
    # 『フォルダ作成』ラベルの作成
    IDirLabel = ttk.Label(frame1, text="フォルダ作成＞＞", padding=(5, 2))
    IDirLabel.pack(side=["left"])
    # 『フォルダ作成』エントリーの作成
    entry1 = StringVar()
    IDirEntry = ttk.Entry(frame1, textvariable=entry1, width=30)
    IDirEntry.pack(side=["left"])
    # 『フォルダ作成』ボタンの作成
    IDirButton = ttk.Button(frame1, text="作成", command=dir_dialog_clicked)
    IDirButton.pack(side=["left"])
    # Frame2の作成
    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(row=2, column=1, sticky=["e"])
    # 『ファイル作成』ラベルの作成
    IFileLabel = ttk.Label(frame2, text="ファイル作成＞＞", padding=(5, 2))
    IFileLabel.pack(side=["left"])
    # 『ファイル作成』エントリーの作成
    entry2 = StringVar()
    IFileEntry = ttk.Entry(frame2, textvariable=entry2, width=10)
    IFileEntry.pack(side=["left"])
    # 『ファイル作成』ボタンの作成
    IFileButton = ttk.Button(frame2, text="作成", command=filedialog_clicked)
    IFileButton.pack(side=["left"])
    # Frame3の作成
    frame3 = ttk.Frame(root, padding=10)
    frame3.grid(row=5, column=1, sticky=["w"])
    # 実行ボタンの設置
    button1 = ttk.Button(frame3, text="実行", command=conductMain)
    button1.pack(fill="x", padx=30, side=["left"])
    # キャンセルボタンの設置
    button2 = ttk.Button(frame3, text=("閉じる"), command=quit)
    button2.pack(fill="x", padx=30, side=["left"])
    root.mainloop()
