import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends import *
from datetime import datetime as dtm
import datetime
import matplotlib as mpl
 
 


# 数据生成函数
def generate_data(input_csv):
    # 读取CSV文件
    df = pd.read_csv(input_csv, parse_dates=['日期'])
    df['日期'] = pd.to_datetime(df['日期'])
    maxvalue = df["消息数量"].iloc[0]
    return df,maxvalue

# 数据切分函数
def split_months(df, year):
    """
    Take a df, slice by year, and produce a list of months,
    where each month is a 2D array in the shape of the calendar
    :param df: dataframe or series
    :return: matrix for daily values and numerals
    """
    df = df[df['日期'].dt.year == year]

    # Empty matrices
    a = np.empty((6, 7))
    a[:] = np.nan

    day_nums = {m:np.copy(a) for m in range(1,13)}  # matrix for day numbers
    day_vals = {m:np.copy(a) for m in range(1,13)}  # matrix for day values
    #print(df.iterrows())
    print(len(df))
    

    # Logic to shape datetimes to matrices in calendar layout
    for _,d in df.iterrows():  # use iterrows if you have a DataFrame
        #print("aaaa",d)
        
        day = d["日期"].day
        month = d["日期"].month
        col = d["日期"].dayofweek
        
        firstweekDay = datetime.date(2024, month, 1).weekday()

        
        #print(day,month,col)
         # Calculate the difference between the current date and the first day of the month
        #first_day_of_month = datetime(year, month, 1)
        #diff = d["日期"] - first_day_of_month
     
        row_idx = day // 7 
        
        if day % 7 == 0:
            row_idx -= 1
        
        if col < firstweekDay:
            row_idx += 1
        

        day_nums[month][row_idx, col] = day  # day number (0-31)
        day_vals[month][row_idx, col] = d["消息数量"] # day value (the heatmap data)

        #if col == 6:
        #    row_idx += 1

    return day_nums, day_vals

# 绘图函数
def create_year_calendar(day_nums, day_vals,the_plot_title,saved_path,color_map,month_names,days,weeks,max_value):
    fig, ax = plt.subplots(3, 4, figsize=(14.85, 10.5))
    
    

    for i, axs in enumerate(ax.flat):

        im = axs.imshow(day_vals[i+1], cmap=color_map, vmin=1, vmax=max_value)  # heatmap
        axs.set_title(month_names[i])

        # Labels
        axs.set_xticks(np.arange(len(days)))
        axs.set_xticklabels(days, fontsize=10, fontweight='bold', color='#555555')
        axs.set_yticklabels([])

        # Tick marks
        axs.tick_params(axis=u'both', which=u'both', length=0)  # remove tick marks
        axs.xaxis.tick_top()

        # Modify tick locations for proper grid placement
        axs.set_xticks(np.arange(-.5, 6, 1), minor=True)
        axs.set_yticks(np.arange(-.5, 5, 1), minor=True)
        axs.grid(which='minor', color='w', linestyle='-', linewidth=2.1)

        # Despine
        for edge in ['left', 'right', 'bottom', 'top']:
            axs.spines[edge].set_color('#FFFFFF')

        # Annotate
        for w in range(len(weeks)):
            for d in range(len(days)):
                day_val = day_vals[i+1][w, d]
                day_num = day_nums[i+1][w, d]
                
                #if i == 1:d
                    #print(f"day_val:{day_val}\nday_num:{day_num}")
                

                # Value label
                axs.text(d, w+0.3, f"{day_val:0.0f}",
                         ha="center", va="center",
                         fontsize=7, color="w", alpha=0.8)

                # If value is 0, draw a grey patch
                if day_val == 0:
                    patch_coords = ((d - 0.5, w - 0.5),
                                    (d - 0.5, w + 0.5),
                                    (d + 0.5, w + 0.5),
                                    (d + 0.5, w - 0.5))

                    square = Polygon(patch_coords, fc='#DDDDDD')
                    axs.add_artist(square)

                # If day number is a valid calendar day, add an annotation
                if not np.isnan(day_num):
                    axs.text(d+0.45, w-0.31, f"{day_num:0.0f}",
                             ha="right", va="center",
                             fontsize=6, color="#003333", alpha=0.8)  # day

                # Aesthetic background for calendar day number
                patch_coords = ((d-0.1, w-0.5),
                                (d+0.5, w-0.5),
                                (d+0.5, w+0.1))

                triangle = Polygon(patch_coords, fc='w', alpha=0.7)
                axs.add_artist(triangle)


        # 在最后一个子图上添加颜色条
        if i == 11:
            cax = fig.add_axes([0.95, 0.15, 0.01, 0.7])  # 创建一个用于颜色条的轴
            plt.colorbar(im,cax=cax, label='消息条数')
    # Final adjustments
    fig.suptitle(the_plot_title, fontsize=16)
    plt.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.04)
    

    # Save to file
    plt.savefig(f'{saved_path}/{the_plot_title}.pdf')
    #print(f'{saved_path}/{the_plot_title}.pdf')
def generateCalendarMain(selected_years,acquired_filepath,saved_path,group_name,title=""):
    try:
        mpl.rcParams['font.family'] = 'SimHei'

        # Settings
        
        weeks = [1, 2, 3, 4, 5, 6]
        days = ['一', '二', '三', '四', '五', '六', '日']
        month_names = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']

        #颜色映射
        # 定义颜色映射的颜色段
        #colors = ['#61bfb4', '#0e3560', '#2e1054', '#e82f0f']  # 
        #n_bins = [6, 6, 6, 17]  # 每个颜色段的区间数

        colors = ['#61bfb4', '#0e3560', '#2e1054']  # 
        n_bins = [6, 6, 6]  # 每个颜色段的区间数

        # 创建自定义颜色映射
        my_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=sum(n_bins))
        
        for year in selected_years:
            df,maxvalue = generate_data(acquired_filepath)
            #print(acquired_filepath,"\n",int(year.strip()))
            
            # 获取指定年份最早的日期
            #print(df[df['日期'].dt.year == int(year.strip())]['日期'])
            earliest_date = df[df['日期'].dt.year == year]['日期'].min()
            #print(earliest_date)
            starts_date = earliest_date.strftime('%Y年%m月%d日')
            
            day_nums, day_vals = split_months(df, year)
            
            if title == "":
                fixed_title = f"{year}年{group_name}群每日群聊消息数量（{starts_date}至年底）"
                create_year_calendar(day_nums, day_vals, fixed_title, saved_path,my_cmap,month_names,days,weeks,maxvalue)
            else:
                create_year_calendar(day_nums, day_vals, title, saved_path,my_cmap,month_names,days,weeks,maxvalue)
            plt.show()
    except Exception as e:
        raise Exception(e)
        
'''

for year in years:
    df = generate_data('./意识、意识工程研讨群./analysis_ed.csv')
    day_nums, day_vals = split_months(df, year)
    title = "2024年意识、意识工程研讨群每日群聊消息数量（2024年1月12日至年底）"
    create_year_calendar(day_nums, day_vals, title)
    plt.show()'''