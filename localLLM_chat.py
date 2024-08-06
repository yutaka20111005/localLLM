## ローカルLLM「Tiny Llama」を使用
from llama_cpp import Llama
import tkinter
import time
import threading

busyflag = 0   # 推論中フラグ

# 推論を行う関数
def timerctrl():
  global busyflag
  if busyflag == 1:   # 推論中フラグがオンの場合
    busyflag = 0
    nowtime = time.time()                  
    prompt = ent_q.get(0., tkinter.END)   
    # 推論を実行して、返答を取得
    output = llm(prompt, max_tokens=150)   
    runningtime = time.time() - nowtime  
    temp = output['choices'][0]['text']
    temp += " (Time:" + str(int(runningtime)) + " sec.)"
    ent_a.delete(0., tkinter.END)
    ent_a.insert(tkinter.END, temp)
    btn.place(x=180, y=170, width=280, height=30)

  timer = threading.Timer(1, timerctrl)
  timer.start()


def button_click(event):
  global busyflag
  btn.place_forget()
  ent_a.delete(0., tkinter.END)
  ent_a.insert(tkinter.END, 'Please wait...')
  busyflag = 1   # 推論中フラグをオンにする


## Hugging Faceよりtinyllama-1.1b-chat-v1.0.Q8_0.ggufをDownloadし
## mkdir tinyllamaで作成したディレクトリに、配置しています。
llm = Llama(
  model_path="./tinyllama/tinyllama-1.1b-chat-v1.0.Q8_0.gguf",
  verbose=False  
)

root = tkinter.Tk()     
root.geometry("1200x480")
root.title("ローカルLLM「Tiny Llama」チャットアプリ(PC上での使用を想定)")
root.resizable(False, False)

canvas = tkinter.Canvas(root, width=1200, height=480, bg="skyblue")
canvas.pack()

fontsize = fonts = ("", 16)

lab_q = tkinter.Label(root, text='質問入力欄', font=fontsize, bg='skyblue') 
lab_q.place(x=30, y=10, width=1000, height=20)
lab_a = tkinter.Label(root, text='AIからの回答', font=fontsize)
lab_a.place(x=30, y=240, width=1000, height=20)

ent_q = tkinter.Text(root, font=fontsize)  
ent_q.place(x=8, y=40, width=1280, height=120)
ent_a = tkinter.Text(root, font=fontsize) 
ent_a.place(x=8, y=240, width=1280, height=230)
ent_q.insert(tkinter.END, "何でも尋ねてください。(^^)/~")

btn = tkinter.Button(root, text='AIに尋ねてみる', font=fontsize, bg='yellow')
btn.place(x=500, y=170, width=280, height=60)
btn.bind("<Button-1>", button_click)


thread = threading.Thread(target=timerctrl)
thread.deamon = True
thread.start()

root.mainloop()

