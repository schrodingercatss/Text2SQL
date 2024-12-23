# Text2SQL
一个无代码自然语言执行数据分析查询系统

### 1. 依赖库
```
pymysql
pandas
matplotlib
gradio
```

### 2. 运行配置项
需要在test.py中填入密钥信息：
```
#以下密钥信息从控制台获取
appid = "xxx"     #填写控制台中获取的 APPID 信息
api_secret = "xxx"   #填写控制台中获取的 APISecret 信息
api_key ="xxx"    #填写控制台中获取的 APIKey 信息
```
以及在main.py中填入数据库信息
```
# 数据库连接配置
DB_CONFIG = {
    "host": "xxxx.net",
    "port": 3306,
    "user": "text2sql",
    "password": "xxx",
    "database": "text2sql"
}
```
### 3. 运行
执行语句 `python main.py`， 在浏览器打开`http://localhost:7860`即可运行。
