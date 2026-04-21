import os
import streamlit as st
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

# 页面配置
st.set_page_config(page_title="线下零售预测", layout="centered")

# 背景色（淡蓝）
st.markdown("""
<style>
.stApp {
    background-color: #f0f8fb;
}
</style>
""", unsafe_allow_html=True)

# 加载模型
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "sales_model.pkl")
    return joblib.load(model_path)

model = load_model()

# 界面
st.title("🛒 线下零售销售额预测")
st.divider()

col1, col2 = st.columns(2)
with col1:
    Quantity = st.number_input("销售数量", 1, 20, 5)


with col2:
    Category = st.selectbox("类别", ["Technology", "Furniture", "Office Supplies"])
    Sub_Category = st.selectbox("子类别", [
    "Phones", "Chairs", "Binders", "Paper", "Art", "Storage",
    "Tables", "Bookcases", "Appliances", "Fasteners", "Labels",
    "Envelopes", "Furnishings", "Accessories", "Supplies",
    "Machines", "Copiers", "Furniture", "Office Supplies"
])
    Region = st.selectbox("地区", ["Central", "West", "East", "South"])
    Segment = st.selectbox("客户类型", ["Consumer", "Corporate", "Home Office"])
    Ship_Mode = st.selectbox("运输方式", ["Standard Class", "Second Class", "First Class", "Same Day"])

    st.divider()
    st.caption("💰 价格信息")
    Avg_Unit_Price = st.number_input("平均单价 (元/件)", 1.0, 5000.0, 100.0, step=10.0)

# 预测
if st.button("推荐最优折扣", type="primary"):
    best_discount = 0
    best_profit = -999
    
    for discount in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]:
        df = pd.DataFrame({
            "Quantity": [Quantity],
            "Discount": [discount],
            "Avg_Unit_Price": [Avg_Unit_Price], 
            "Profit": [0],
            "Category": [Category],
            "Sub-Category": [Sub_Category],
            "Region": [Region],
            "Segment": [Segment],
            "Ship Mode": [Ship_Mode]
        })
                profit = model.predict(df)[0]
        if profit > best_profit:
            best_profit = profit
            best_discount = discount
    
    st.success(f"推荐折扣：{int(best_discount * 100)}%")
    st.info(f"预期利润：¥ {round(best_profit, 2)}")
