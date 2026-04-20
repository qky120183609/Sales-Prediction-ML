import pandas as pd
import os
from sqlalchemy import create_engine

# 连接MySQL的sales_data数据库，导出online_retail表
engine = create_engine("mysql+pymysql://root:2002li,you,cong.@localhost:3306/sales_data")

df = pd.read_sql("SELECT * FROM online_retail", engine)

# 导出CSV
df.to_csv("online_retail.csv", index=False, encoding='utf-8-sig')

print("导出成功！")
print(f"数据条数：{len(df)}")
