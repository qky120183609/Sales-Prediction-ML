import os
import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MYSQL_PASSWORD = '{MYSQL_PASSWORD}'

engine = create_engine(f"mysql+pymysql://root:{MYSQL_PASSWORD}@localhost:3306/sales_data")

#---------------------------------------------#

print("正在导入超市数据...")

df1 = pd.read_csv(os.path.join(BASE_DIR, "csv/sample_-_superstore.csv"))

#---------------------------------------------#

df1 = df1.drop_duplicates()
df1 = df1.dropna(subset = ['order_id','order_date','sales','profit','quantity'])
df1['order_date'] = pd.to_datetime(df1['order_date'],errors='coerce')
df1['ship_date'] = pd.to_datetime(df1['ship_date'],errors='coerce')
df1 = df1.dropna(subset=['order_date'])

df1 = df1[df1['quantity'] > 0]
df1 = df1[df1['sales'] > 0]
df1 = df1[(df1['discount'] >= 0) & (df1['discount'] <= 1)]
df1 = df1[df1['profit'] >= -1000]

df1 = df1.reset_index(drop=True)

#---------------------------------------------#

df1.to_sql(
    name="retail_sales",
    con=engine,
    if_exists='append',
    index=False
)
print("超市数据清洗完成，数据已导入 MySQL")
