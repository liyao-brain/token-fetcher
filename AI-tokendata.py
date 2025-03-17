from pymongo import MongoClient
import requests
from datetime import datetime
import schedule
import time

# MongoDB 连接
client = MongoClient("mongodb+srv://liyao:liyao20011123@memecoin.c54b4.mongodb.net/")  # 替换为你的 MongoDB 地址
db = client["Community_and_Social_Media_Data"]  # 数据库名称

# 需要获取的代币列表
target_tokens = {"Fartcoin 💨", "Turbo 🐸", "aixbt", "AVA", "AGIXBT", "Alchemist AI"}

# 数据获取和插入逻辑
def fetch_and_store_tokens():
    print(f"任务开始执行: {datetime.utcnow()}")

    # 获取数据
    url = "https://www.sentient.market/api/tokens"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("成功获取数据！")

        # 仅保留目标代币的数据
        filtered_tokens = [token for token in data if token.get("agentName") in target_tokens]

        # 插入数据到 MongoDB
        for token in filtered_tokens:
            # 使用 token 的 agentName 作为集合名称
            collection_name = token["agentName"].replace(" ", "_").replace("$", "_").lower()  # 处理集合名称
            collection = db[collection_name]

            # 附加时间戳
            token["timestamp"] = datetime.utcnow()

            # 插入数据到对应集合
            collection.insert_one(token)
            print(f"数据已插入集合: {collection_name}，Token ID: {token['id']}")
    else:
        print(f"请求失败，状态码: {response.status_code}")

# 定时任务设置：每5分钟执行一次
schedule.every(5).minutes.do(fetch_and_store_tokens)

# 启动定时任务
print("开始执行定时任务...")
while True:
    schedule.run_pending()
    time.sleep(1)
