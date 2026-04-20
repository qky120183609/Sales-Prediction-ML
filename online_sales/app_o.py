import os
import streamlit as st
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

# 页面配置
st.set_page_config(page_title="在线零售预测", layout="centered")

# 背景（绿色）
st.markdown("""
<style>
.stApp {
    background-color: #f0fff8;
}
</style>
""", unsafe_allow_html=True)

# 加载模型
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "online_sales_model.pkl")
    return joblib.load(model_path)

model = load_model()

# 界面
st.title("🌐 在线零售订单预测")
st.divider()

col1, col2 = st.columns(2)
with col1:
    Quantity = st.number_input("购买数量", 1, 50, 1)
    UnitPrice = st.number_input("商品单价", 0.1, 100.0, 10.0)

with col2:
    Country = st.selectbox("国家", [
        "United Kingdom", "France", "Germany", 
        "Spain", "Australia", "Italy"
    ])

# 预测
if st.button("📊 预测订单金额", type="primary"):
    df = pd.DataFrame({
        "Quantity": [Quantity],
        "UnitPrice": [UnitPrice],
        "Country": [Country]
    })
    pred = model.predict(df)
    st.success(f"预测金额：¥ {round(pred[0], 2)}")
