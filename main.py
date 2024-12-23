import gradio as gr
from backend import *

# 数据库连接配置
DB_CONFIG = {
    "host": "xxxx.net",
    "port": 3306,
    "user": "text2sql",
    "password": "xxx",
    "database": "text2sql"
}


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
