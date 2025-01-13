import pandas as pd
import os
# 定义分析函数
def analyze_chat_frequency(input_csv,key_name="",output_name=""):
    # 读取 CSV 文件
    df = pd.read_csv(input_csv)
    
    # 转换时间戳为日期（提取日期部分）
    df['日期'] = pd.to_datetime(df['时间戳']).dt.date
    
    # 按日期统计聊天条数
    daily_message_count = df.groupby('日期').size().reset_index(name='消息数量')
    
    # 按消息数量降序排序
    sorted_daily_count = daily_message_count.sort_values(by='消息数量', ascending=False)
    file_name_without_postfix = input_csv.rstrip("群聊天消息.csv")
    
    if output_name == "":
        output_csv = f"{file_name_without_postfix}每日消息频次分析结果.csv"
    else:
        output_csv = f"{os.path.dirname(input_csv)}/{output_name}每日消息频次分析结果.csv"
    
    # 保存结果到新的 CSV 文件
    sorted_daily_count.to_csv(output_csv, index=False, encoding='utf-8')
    
    
    
    return f"每日聊天频度分析结果已保存到: {output_csv}", output_csv
    
    

# 示例调用

# 执行分析函数
#analyze_chat_frequency("./意识、意识工程研讨群/discussion_group.csv", "./意识、意识工程研讨群/analysis_ed.csv")