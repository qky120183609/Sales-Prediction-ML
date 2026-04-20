import pandas as pd
import joblib
import sys

try:
    model = joblib.load("sales_model.pkl")
    print("模型加载成功")
except FileNotFoundError:
    print("错误：找不到 sales_model.pkl，请先运行 sales_train.py")
    sys.exit(1)

sample = pd.DataFrame({
    "Quantity": [5],
    "Discount": [0.2],
    "Profit": [20],
    "Category": ["Technology"],
    "Sub-Category": ["Phones"],
    "Region": ["Central"],
    "Segment": ["Consumer"]
})

try:
    pred = model.predict(sample)
    print(f"预测销售额：¥{round(pred[0], 2)}")
except Exception as e:
    print(f"预测失败：{e}")
