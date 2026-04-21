import os
import streamlit as st
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

# 页面配置
st.set_page_config(page_title="线下零售利润预测与折扣优化", layout="centered")

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
    Avg_Unit_Price = st.number_input("平均单价 (元/件)", 1.0, 5000.0, 100.0, step=10.0)
    Discount = st.slider("选择折扣比例 (%)", 0, 50, 0, 10, key="discount_slider") / 100
    Category = st.selectbox("类别", ["Technology", "Furniture", "Office Supplies"])
with col2:
    Sub_Category = st.selectbox("子类别", [    "Phones", "Chairs", "Binders", "Paper", "Art", "Storage",
        "Tables", "Bookcases", "Appliances", "Fasteners", "Labels",
        "Envelopes", "Furnishings", "Accessories", "Supplies",
        "Machines", "Copiers", "Furniture", "Office Supplies"
    ])
    Region = st.selectbox("地区", ["Central", "West", "East", "South"])
    Segment = st.selectbox("客户类型", ["Consumer", "Corporate", "Home Office"])
    Ship_Mode = st.selectbox("运输方式", ["Standard Class", "Second Class", "First Class", "Same Day"])

# 预测
if st.button("预测利润", type="primary"):
    df = pd.DataFrame({
        "Quantity": [Quantity],
        "Discount": [Discount],
        "Avg_Unit_Price": [Avg_Unit_Price], 
        "Category": [Category],
        "Sub-Category": [Sub_Category],
        "Region": [Region],
        "Segment": [Segment],
        "Ship Mode": [Ship_Mode]
    })
    profit = model.predict(df)[0]
    
    # 显示当前折扣的利润
    st.info(f"💰 当前折扣 **{int(Discount*100)}%** 下，预期利润：**¥ {round(profit, 2)}**")
    
    # 计算最优折扣作为参考
    best_discount = 0
    best_profit = -float("inf")
    for d in [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
        temp_df = pd.DataFrame({
            "Quantity": [Quantity],
            "Discount": [d],
            "Avg_Unit_Price": [Avg_Unit_Price],
            "Category": [Category],
            "Sub-Category": [Sub_Category],
            "Region": [Region],
            "Segment": [Segment],
            "Ship Mode": [Ship_Mode]
        })
        p = model.predict(temp_df)[0]
        if p > best_profit:
            best_profit = p
            best_discount = d
    
    if best_discount != Discount:
        st.success(f"提示：折扣 **{int(best_discount*100)}%** 可获得更高利润（¥{round(best_profit, 2)}）")
    else:
        st.success(f"当前折扣已是利润最优选择！")
