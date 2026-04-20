import pandas as pd
import joblib

# 加载模型
model = joblib.load("online_sales_model.pkl")

# 预测数据
sample = pd.DataFrame({
    "Quantity": [10],
    "UnitPrice": [2.5],
    "Country": ["United Kingdom"]
})

# 预测
pred = model.predict(sample)
print("预测销售额：", round(pred[0], 2))
