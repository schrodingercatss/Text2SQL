import gradio as gr
from SparkApi import *
from test import *
from schema import *
import json
import pymysql
import matplotlib.pyplot as plt
import pandas as pd

# 数据库连接配置
DB_CONFIG = {
    "host": "xxxx.net",
    "port": 3306,
    "user": "text2sql",
    "password": "xxx",
    "database": "text2sql"
}

def execute_query(sql_query):
    try:
        # 连接到数据库
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            # 执行查询
            cursor.execute(sql_query)
            # 获取查询结果
            result = cursor.fetchall()
            # 获取列名
            columns = [desc[0] for desc in cursor.description]
            # 将结果转换为二维列表格式
            result_table = [list(row) for row in result]
        return result_table, columns
    except Exception as e:
        return f"查询失败: {e}", None
    finally:
        connection.close()

def query(database_type, Input, previous_state):
    # 根据选择的数据库类型拼接第二部分
    if database_type == "学生信息数据库":
        db_schema = STUDENT_DB_SCHEMA
    elif database_type == "图书借阅数据库":
        db_schema = BOOK_DB_SCHEMA
    else:
        db_schema = ""
    
    global text
    text.clear()
    # 拼接完整的 question
    Input = f"{FIXED_PROMPT}{db_schema}{Input}"
    question = checklen(getText("user", Input, text))
    SparkApi.answer = ""
    # 调用 API
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    tmp = getText("assistant", SparkApi.answer, text)[1]
    print(tmp)
    # 解析 JSON 数据
    response_data = json.loads(tmp['content'])
    
    # 提取 SQL 字段的内容
    sql_content = response_data.get('SQL', '')
    
    # 执行 SQL 查询并返回结果
    if sql_content:
        query_result, columns = execute_query(sql_content)
        if isinstance(query_result, str):  # 如果查询失败，返回错误信息
            return sql_content, query_result, None, None, None  # 状态重置为 None
        else:
            # 将查询结果转换为 Pandas DataFrame
            df = pd.DataFrame(query_result, columns=columns)
            return sql_content, "查询成功", df, columns, df  # 更新状态为当前的 DataFrame
    else:
        return "未生成有效的 SQL 查询语句", "未执行查询", None, None, None  # 状态重置为 None

def calculate_statistics(data):
    """
    计算统计数据：均值、方差、标准差、中位数、众数
    """
    mean = data.mean()
    variance = data.var()
    std_dev = data.std()
    median = data.median()
    mode = data.mode().values[0] if not data.mode().empty else "无众数"
    
    return {
        "均值": mean,
        "方差": variance,
        "标准差": std_dev,
        "中位数": median,
        "众数": mode
    }

def visualize_data(query_result, column_name):
    """
    对查询结果进行可视化，并计算统计数据
    """
    if query_result is None or query_result.empty:  # 使用 .empty 判断 DataFrame 是否为空
        return "无数据可用于可视化", None
    
    # 检查用户指定的列名是否存在
    if column_name not in query_result.columns:
        return f"列名 '{column_name}' 不存在，请选择正确的列名。", None
    
    # 提取指定列的数据
    data = query_result[column_name]
    
    # 计算统计数据
    stats = calculate_statistics(data)
    
    # 创建图表
    plt.figure(figsize=(10, 6))
    
    # 示例：绘制柱状图
    if column_name == "age":
        plt.bar(query_result["name"], data, color='skyblue')
        plt.xlabel("姓名")
        plt.ylabel("年龄")
        plt.title("学生年龄分布")
        plt.xticks(rotation=45)
    else:
        # 对于其他列，绘制简单的折线图
        plt.plot(data, marker='o', color='orange')
        plt.xlabel("索引")
        plt.ylabel(column_name)
        plt.title(f"{column_name} 数据分布")
    
    # 将图表保存为临时文件
    temp_file = "temp_plot.png"
    plt.savefig(temp_file, format="png")
    plt.close()
    
    # 返回文件路径和统计数据
    return temp_file, stats

def reset_state():
    """
    清空状态（用于重置按钮）
    """
    return None, None, None, None, None

# 创建 Gradio 界面
def create_interface():
    with gr.Blocks() as demo:
        # 输入部分
        with gr.Row():
            database_type = gr.Radio(["学生信息数据库", "图书借阅数据库"], label="选择数据库")
            query_input = gr.Textbox(label="输入查询任务")
        
        # 查询按钮
        query_button = gr.Button("执行查询")
        reset_button = gr.Button("重置查询")
        
        # 输出部分
        with gr.Row():
            sql_output = gr.Textbox(label="SQL 查询语句", interactive=False)
            status_output = gr.Textbox(label="查询状态", interactive=False)
        
        # 查询结果表格
        result_table = gr.Dataframe(label="查询结果", interactive=False)
        
        # 可视化部分
        with gr.Row():
            column_name_input = gr.Textbox(label="输入要可视化的列名")
            visualize_button = gr.Button("可视化数据")
        
        # 可视化结果
        with gr.Row():
            visualization_output = gr.Image(label="可视化结果", height=600, width=800)
            statistics_output = gr.JSON(label="统计数据")
        
        # 状态管理
        query_state = gr.State(None)  # 初始化状态为 None
        
        # 查询按钮的回调
        query_button.click(
            query,
            inputs=[database_type, query_input, query_state],
            outputs=[sql_output, status_output, result_table, query_state, query_state]
        )
        
        # 重置按钮的回调
        reset_button.click(
            reset_state,
            inputs=[],
            outputs=[sql_output, status_output, result_table, visualization_output, query_state]
        )
        
        # 可视化按钮的回调
        visualize_button.click(
            visualize_data,
            inputs=[query_state, column_name_input],
            outputs=[visualization_output, statistics_output]
        )
    
    return demo

# 启动 Gradio 界面
demo = create_interface()
demo.launch()
