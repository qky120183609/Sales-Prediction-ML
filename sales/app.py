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
    Cost = st.number_input("商品成本 (元/件)", min_value=0.1, max_value=5000.0, value=50.0, step=10.0)
    Discount = st.slider("选择折扣比例 (%)", 0, 50, 0, 10, key="discount_slider") / 100

with col2:
    Category = st.selectbox("类别", ["Technology", "Furniture", "Office Supplies"])
    Sub_Category = st.selectbox("子类别", [    "Phones", "Chairs", "Binders", "Paper", "Art", "Storage",
        "Tables", "Bookcases", "Appliances", "Fasteners", "Labels",
        "Envelopes", "Furnishings", "Accessories", "Supplies",
        "Machines", "Copiers", "Furniture", "Office Supplies"
    ])
    Region = st.selectbox("地区", ["Central", "West", "East", "South"])
    Segment = st.selectbox("客户类型", ["Consumer", "Corporate", "Home Office"])
    Ship_Mode = st.selectbox("运输方式", ["Standard Class", "Second Class", "First Class", "Same Day"])




if st.button("预测利润", type="primary"):
    # 考虑折扣，计算实际毛利率
    Actual_Price = Avg_Unit_Price * (1 - Discount)
    Gross_Margin = (Actual_Price - Cost) / Actual_Price if Actual_Price > 0 else 0
    
    # 创建预测数据
    df = pd.DataFrame({
        "Quantity": [Quantity],
        "Discount": [Discount],
        "Avg_Unit_Price": [Avg_Unit_Price],
        "Gross_Margin": [Gross_Margin],
        "Category": [Category],
        "Sub-Category": [Sub_Category],
        "Region": [Region],
        "Segment": [Segment],
        "Ship Mode": [Ship_Mode]
    })
    profit = model.predict(df)[0]
    # 计算数学利润和差值
    formula_profit = (Actual_Price - Cost) * Quantity
    diff = profit - formula_profit
 
    
    # 显示定价合理性分析
    st.divider()
    st.subheader("📊 定价合理性分析")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("📐 数学利润", f"¥ {round(formula_profit, 2)}")
        st.metric("🤖 模型预测利润", f"¥ {round(profit, 2)}", delta=f"{round(diff, 2)}")
    with col_b:
        st.metric("💰 成本", f"¥ {Cost:.2f}")
        st.metric("📊 销售额", f"¥ {round(Actual_Price * Quantity, 2)}")
    
    if diff > 0:
        st.success(f"模型预测利润大于数学利润，模型认为该条件能获得的足够的数学利润，若差值较多可以调整变为更高利润")
    elif diff < 0:
        st.warning(f"模型预测利润小于数学利润，模型认为该条件不能获得的足够的数学利润，若差值较多需要调整变为更低利润")
    else:
        st.info(f"与模型预测完全相符")
    
    st.divider()
    
    # 推荐最佳地区
    best_region = None
    best_profit = -float("inf")
    for r in ["Central", "West", "East", "South"]:
        temp_df = pd.DataFrame({
            "Quantity": [Quantity],
            "Discount": [Discount],
            "Avg_Unit_Price": [Avg_Unit_Price],
            "Gross_Margin": [Gross_Margin],  # 新增
            "Category": [Category],
            "Sub-Category": [Sub_Category],
            "Region": [r],
            "Segment": [Segment],
            "Ship Mode": [Ship_Mode]
        })
        p = model.predict(temp_df)[0]
        if p > best_profit:
            best_profit = p
            best_region = r
    
    if best_region != Region:
        st.info(f"📍 提示：**{best_region}** 地区可获得更高利润（¥{round(best_profit, 2)}）")
    else:
        st.success(f"当前地区已是利润最优选择！")
