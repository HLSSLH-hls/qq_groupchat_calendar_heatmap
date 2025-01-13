import csv
import pandas as pd
import re

# 定义一个函数解析聊天记录
def parse_chat_log(file_path):
    messages = []
    groupname = "unknownFileName"
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    #提取群聊名称
    for line in lines:
        if "消息对象:" in line:
            parts = line.split("消息对象:")
            if(len(parts) > 1):
                groupname = parts[1].strip()
                break
    #规定时间戳
    timestamp_pattern = re.compile(r"\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2} (AM|PM)")
    # 遍历每一行并解析
    for i, line in enumerate(lines):
        # 检查是否包含时间戳
         if timestamp_pattern.match(line.strip()):
            try:
                # 分割时间戳、用户名和QQ号
                timestamp, user_info = line.split(" ", 1)
                user, qq_info = user_info.split("(")
                qq_number = qq_info.strip(")")
                # 获取消息内容（下一行）
                message_content = lines[i + 1].strip() if i + 1 < len(lines) else ""
                # 特殊处理图片标记
                if "[图片]" in message_content:
                    message_content = "[图片]"
                messages.append([timestamp, user.strip(), qq_number, message_content])
            except ValueError:
                # 忽略格式不正确的行
                continue
            
    if len(messages) == 0:
        raise Exception("没有读取到相关数据")
    return groupname,messages

# 写入CSV文件
def write_to_csv(messages, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["时间戳", "用户名", "QQ号", "消息内容"])
        writer.writerows(messages)

# 写入XLSX文件
def write_to_xlsx(messages, output_xlsx):
    df = pd.DataFrame(messages, columns=["时间戳", "用户名", "QQ号", "消息内容"])
    df.to_excel(output_xlsx, index=False)

# 主函数
def parse_and_convert(input_txt, destination_path,output_csv="", output_xlsx="", ):
    # 解析聊天记录
    group_name, messages = parse_chat_log(input_txt)
    
    if output_csv == "":
        output_csv = f"{destination_path}/{group_name}群聊天记录.csv"
    if output_xlsx == "":
        output_xlsx = f"{destination_path}/{group_name}群聊天记录.xlsx"
    # 保存为CSV和XLSX文件
    write_to_csv(messages, output_csv)
    write_to_xlsx(messages, output_xlsx)
    
    return f"数据已成功保存为：\nCSV文件: {output_csv}\nXLSX文件: {output_xlsx}",output_csv,group_name


#parse_and_convert("./意识、意识工程研讨群/意识、意识工程研讨群.txt","./意识、意识工程研讨群/discussion_group.csv","./意识、意识工程研讨群/discussion_group.xlsx")
    