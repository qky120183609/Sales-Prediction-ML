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
    Discount = st.slider("折扣", 0.0, 1.0, 0.2)
    Profit = st.number_input("利润", 0, 200, 20)

with col2:
    Category = st.selectbox("类别", ["Technology", "Furniture", "Office Supplies"])
    Sub_Category = st.selectbox("子类别", ["Phones", "Chairs", "Binders", "Paper", "Art", "Storage", "Tables", "Bookcases", "Appliances", "Fasteners", "Labels", "Envelopes", "Furnishings", "Accessories", "Supplies", "Machines", "Copiers"])
    Region = st.selectbox("地区", ["Central", "West", "East", "South"])
    Segment = st.selectbox("客户类型", ["Consumer", "Corporate", "Home Office"])
    Ship_Mode = st.selectbox("运输方式", ["Standard Class", "Second Class", "First Class", "Same Day"])

# 预测
if st.button("🔮 预测销售额", type="primary"):
    df = pd.DataFrame({
        "Quantity": [Quantity],
        "Discount": [Discount],
        "Profit": [Profit],
        "Category": [Category],
        "Sub-Category": [Sub_Category],
        "Region": [Region],
        "Segment": [Segment],
        "Ship Mode": [Ship_Mode]
    })
    pred = model.predict(df)
    st.success(f"预测销售额：¥ {round(pred[0], 2)}")
