import pandas as pd
import os
from sqlalchemy import create_engine

# 从MySQL的sales_data数据库导出retail_sales表
engine = create_engine("mysql+pymysql://root:2002li,you,cong.@localhost:3306/sales_data")

df = pd.read_sql("SELECT * FROM retail_sales", engine)
df.to_csv("retail_sales.csv", index=False, encoding='utf-8-sig')

print("导出成功！文件位置：", os.path.abspath("retail_sales.csv"))
print(f"数据条数：{len(df)}")
