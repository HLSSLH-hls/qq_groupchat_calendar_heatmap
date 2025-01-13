
from datetime import datetime
import analysis_chat
import test_heatmap
import qqinfo_to_csv

import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, messagebox

def export_log(content):
    
    # 检验 save_path_valuesav
    if save_path_value.get():
        
        # 这里是导出日志到文件的代码
        with open(f"{save_path_value.get()}/logfile-{datetime.now().strftime('%Y-%m-%d %H:%M')}.txt", "a",encoding="utf-8") as file:
            file.write(content+"\n")


def validate_variables():
    errors = []

    # 检验 title_value
    #if not title_value.get():
    #    errors.append("标题不能为空。")

    # 检验 year_value
    try:
        year = int(year_value.get())
        if year < 0 or year > 9999:  # 假设年份在0到9999之间
            errors.append("年份无效。")
    except ValueError:
        errors.append("年份必须是整数。")

    # 检验 file_path_value
    if not file_path_value.get():
        errors.append("文件路径不能为空。")

    # 检验 save_path_value
    if not save_path_value.get():
        errors.append("保存路径不能为空。")

    # 如果有错误，显示错误消息
    if errors:
        error_message = "\n".join(errors)
        show_error_message(error_message)
        return False
    return True

def select_file():
    filetypes = [('Text files', '*.txt')]
    file_path = filedialog.askopenfilename(title="选择文件", filetypes=filetypes)
    if file_path:
        file_path_value.set(file_path)
    else:
        show_error_message("未选择文件或选择的文件不是 txt 格式。")

def treat_log_area_insert(message):
    # 将文本区域的状态更改为 'normal' 以便插入文本
    log_text_area.config(state='normal')
    # 插入信息到文本区域的末尾
    log_text_area.insert('end',message + '\n')
    # 将文本区域的状态改回 'disabled'
    log_text_area.config(state='disabled')
    # 滚动到文本区域的末尾
    log_text_area.see('end')
def save_file():
    
    # 使用文件对话框选择保存目录
    save_path = filedialog.askdirectory(initialdir=file_path_value.get())
    if save_path:
        # 更新文件保存路径输入框的内容
        save_path_value.set(save_path)
        
def show_error_message(text):
    messagebox.showerror("似乎出了点问题？",text)
def run_convert():
    
    if not validate_variables():
        return
    parse_result,result_filename,group_name = "","",""
    try:
        parse_result,result_filename,group_name = qqinfo_to_csv.parse_and_convert(file_path_value.get(),save_path_value.get())
    except Exception as e:
        cur_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 在解析{file_path_value.get()}时出错: {e}"
        treat_log_area_insert(cur_message)
        export_log(cur_message)
        return
    
    treat_log_area_insert(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {parse_result}")
    export_log(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {parse_result}")
    analysis_result,analysis_filepath = "",""
    
    try:
        analysis_result,analysis_filepath = analysis_chat.analyze_chat_frequency(result_filename)
    except Exception as e:
        treat_log_area_insert(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 在分析{analysis_filepath}时出错: {e}")
        export_log(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 在分析{analysis_filepath}时出错: {e}")
        return
    
    treat_log_area_insert(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {analysis_result}")
    export_log(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {analysis_result}")
    
    
    try:
        #print("title:",title_value.get(), "year:",year_value.get(),"path:",analysis_filepath,"savepath:",save_path_value.get(),"group_name:",group_name)
        test_heatmap.generateCalendarMain([int(year_value.get())],analysis_filepath,save_path_value.get(),group_name,title=title_value.get())
    except Exception as e:
        treat_log_area_insert(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 在绘图时出错: {e}")
        export_log(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {analysis_result}")
        return
    
    treat_log_area_insert(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 绘制完成")
    export_log(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 绘制完成")
    
    
    
    
    
    
    
        



# 创建窗口
root = Tk()
root.title("热力图生成器")

# 初始化变量
title_value = tk.StringVar()
year_value = tk.StringVar()
file_path_value = tk.StringVar()
save_path_value = tk.StringVar()



# 创建标签和输入框（热力图标题）
title_label = Label(root, text="热力图标题:")
title_label.pack(side=tk.TOP, padx=10, pady=5)
title_entry = Entry(root, textvariable=title_value, width=50)
title_entry.pack(side=tk.TOP, padx=10)

# 创建标签和输入框（年份）
year_label = Label(root, text="年份（*必填）:")
year_label.pack(side=tk.TOP, padx=10, pady=5)
year_entry = Entry(root, textvariable=year_value, width=50)
year_entry.pack(side=tk.TOP, padx=10)

# 创建选择文件按钮和输入框
file_label = Label(root, text="选择QQ消息文件路径(*必填):")
file_label.pack(side=tk.TOP, padx=10, pady=5)
file_entry = Entry(root, textvariable=file_path_value, width=50,state='readonly')
file_entry.pack(side=tk.TOP, padx=10)
select_button = Button(root, text="选择待转换QQ消息路径", command=select_file)
select_button.pack(side=tk.TOP, padx=10)

# 创建保存文件路径的标签和输入框
save_label = Label(root, text="保存文件路径(*必填):")
save_label.pack(side=tk.TOP, padx=10, pady=5)
save_path_entry = Entry(root, textvariable=save_path_value, width=50,state='readonly')
save_path_entry.pack(side=tk.TOP, padx=10)
save_button = Button(root, text="选择保存文件路径", command=save_file)
save_button.pack(side=tk.TOP, padx=10)
# 确认转换的按钮
convert_button = Button(root, text="确认转换", command=run_convert,bg="#f37012", fg="black")
convert_button.pack(side=tk.TOP, pady=(20,0))


# 创建操作日志文本区域
log_text_area = scrolledtext.ScrolledText(root, height=10, width=60,state='disabled')
log_text_area.pack(side=tk.BOTTOM, padx=10, pady=40)


# 创建状态标签
status_label = Label(root, text="")
status_label.pack(side=tk.BOTTOM, padx=10, pady=10)



# 启动事件循环
root.mainloop()
