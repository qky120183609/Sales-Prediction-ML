import os
import streamlit as st
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

# 页面配置
st.set_page_config(page_title="线下零售销售额预测", layout="centered")

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
    try:
        return joblib.load(model_path)
    except:
        st.warning("模型文件未找到，请先训练模型")
        return None

model = load_model()

# 取值范围
def get_range_info(field_name):
    ranges = {
        "Quantity": {"min": 1, "max": 50, "default": 5, "help": "销售数量范围：1-50件"},
        "Discount": {"min": 0.0, "max": 0.8, "default": 0.2, "help": "折扣范围：0-80%"},
        "Profit": {"min": -500, "max": 5000, "default": 50, "help": "利润范围：-500到5000元"},
        "Category": ["Technology", "Furniture", "Office Supplies"],
        "SubCategory": ["Phones", "Chairs", "Binders", "Paper", "Art", "Storage", "Tables", 
                       "Bookcases", "Appliances", "Fasteners", "Labels", "Envelopes", 
                       "Furnishings", "Accessories", "Supplies", "Machines", "Copiers"],
        "Region": ["Central", "West", "East", "South"],
        "Segment": ["Consumer", "Corporate", "Home Office"],
        "ShipMode": ["Standard Class", "Second Class", "First Class", "Same Day"]
    }
    return ranges.get(field_name)

st.title("🛒 线下零售销售额预测")
st.caption("基于历史销售数据，预测订单销售额")

if model is None:
    st.error("请先运行训练脚本生成模型文件")
    st.stop()

st.divider()

# 输入表单
with st.form("prediction_form"):
    st.subheader("📋 订单信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        qty_range = get_range_info("Quantity")
        Quantity = st.number_input(
            "销售数量", 
            min_value=qty_range["min"], 
            max_value=qty_range["max"], 
            value=qty_range["default"],
            help=qty_range["help"]
        )
        
        discount_range = get_range_info("Discount")
        Discount = st.slider(
            "折扣", 
            min_value=discount_range["min"], 
            max_value=discount_range["max"], 
            value=discount_range["default"],
            step=0.05,
            help=discount_range["help"]
        )
        
        profit_range = get_range_info("Profit")
        Profit = st.number_input(
            "利润", 
            min_value=profit_range["min"], 
            max_value=profit_range["max"], 
            value=profit_range["default"],
            step=10,
            help=profit_range["help"]
        )
    
    with col2:
        Category = st.selectbox("产品类别", get_range_info("Category"))
        Sub_Category = st.selectbox("产品子类别", get_range_info("SubCategory"))
        Region = st.selectbox("销售地区", get_range_info("Region"))
        Segment = st.selectbox("客户类型", get_range_info("Segment"))
        Ship_Mode = st.selectbox("运输方式", get_range_info("ShipMode"))
    
    submitted = st.form_submit_button("🔮 预测销售额", type="primary", use_container_width=True)

if submitted:
    # 构建预测输入
    input_data = pd.DataFrame({
        "Quantity": [Quantity],
        "Discount": [Discount],
        "Profit": [Profit],
        "Category": [Category],
        "Sub-Category": [Sub_Category],
        "Region": [Region],
        "Segment": [Segment],
        "Ship Mode": [Ship_Mode]
    })
    
    try:
        pred = model.predict(input_data)
        st.success(f"💵 预测销售额：¥ {round(pred[0], 2)}")
        
        # 显示额外信息
        st.info(f"""
        📊 **输入参数汇总**
        - 销售数量：{Quantity} 件
        - 折扣：{Discount*100:.0f}%
        - 利润：¥{Profit:,.2f}
        - 产品类别：{Category} > {Sub_Category}
        - 地区：{Region}
        - 客户类型：{Segment}
        - 运输方式：{Ship_Mode}
        """)
        
    except Exception as e:
        st.error(f"预测失败：{str(e)}")
        st.info("提示：模型可能需要特定的特征组合，请确保模型训练时包含了所有输入特征")
