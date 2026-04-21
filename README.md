# 线下零售利润预测与折扣优化系统 (Retail-Profit-Predictor)

基于机器学习构建的线下零售利润预测与智能折扣优化系统，帮助零售商在定价决策前预测订单利润，识别高折扣亏损风险，优化区域销售策略。

## 项目介绍

本项目基于真实的线下零售订单数据，构建机器学习回归模型实现**订单利润预测**，核心解决零售场景中的三大痛点：
- **利润预测**：在定价决策前预测订单最终利润
- **折扣优化**：识别高折扣导致的亏损风险
- **区域策略**：自动推荐最优销售区域

项目包含完整的数据清洗、特征工程、多模型对比、网格搜索调参、特征重要性分析，并提供Streamlit交互式Web界面，可直接部署使用。

## 项目概览

```mermaid
mindmap
  root((💰 线下零售<br/>利润预测系统))
    数据规模
      零售订单数据集
      多维度特征工程
      亏损订单专项分析
    核心功能
      订单利润预测
      折扣合理性分析
      最优销售区域推荐
      数学利润vs模型预测对比
    技术架构
      Python Pandas/NumPy
      Scikit-learn 机器学习
      Streamlit 交互界面
      Joblib 模型持久化
      Pipeline 特征工程流水线
    模型对比
      线性回归 基线模型
      随机森林 主力模型
      GridSearchCV 超参数调优
    业务洞察
      高折扣(>50%)亏损率分析
      特征重要性排序
      区域利润差异分析
    使用方式
      pip install -r requirements.txt
      python train_model.py 训练模型
      streamlit run app.py 启动界面
```
## 核心功能
### 1. 模型训练模块
数据预处理：缺失值处理、特征标准化、类别特征One-Hot编码

特征工程：构造毛利率(Avg_Unit_Price)、平均单价等业务特征

模型对比：线性回归 vs 随机森林回归

超参数优化：GridSearchCV 自动搜索最优参数

特征重要性分析：识别影响利润的关键因素

### 2. Web预测模块
实时利润预测：输入销售参数，即时预测订单利润

折扣优化分析：对比数学利润与模型预测，判断定价合理性

地区推荐：自动计算并推荐利润最优的销售区域

差异化反馈：根据预测结果给出成功/警告/信息提示

## 技术栈
类别	技术
语言	Python 3.8+
数据分析	Pandas, NumPy
机器学习	Scikit-learn (RandomForest, LinearRegression, Pipeline)
可视化	Matplotlib, Seaborn
交互界面	Streamlit
模型序列化	Joblib
## 项目结构
text
retail-profit-predictor/
├── train_model.py              # 模型训练脚本
├── app.py                      # Streamlit Web应用
├── requirements.txt            # 项目依赖
├── README.md                   # 项目说明
│
├── data/
│   └── retail_sales.csv        # 零售数据集
│
├── models/
│   └── sales_model.pkl         # 训练好的模型
│
├── outputs/
│   ├── feature_importance.csv  # 特征重要性
│   ├── model_metrics.csv       # 模型评估指标
│   └── model_config.csv        # 模型配置信息
│
└── images/
    └── app_screenshot.png      # 应用截图
## 快速开始
### 1. 克隆仓库
```
git clone https://github.com/yourname/retail-profit-predictor.git
cd retail-profit-predictor
```
### 2. 安装依赖
```
pip install -r requirements.txt
```
### 3. 训练模型
```
python train_model.py
```
#训练完成后会生成：
```
sales_model.pkl - 模型文件

feature_importance.csv - 特征重要性

model_metrics.csv - 评估指标
```
### 4. 启动Web应用
```
streamlit run app.py
```
### 5. 单样本预测
```
python
# 在predict.py中实现
python predict.py
```
## 模型评估
## 模型对比结果
模型	R²	MAE	RMSE
线性回归	0.72	68.50	125.30
随机森林	0.89	42.30	86.70
## 最优参数
{
    'regressor__n_estimators': 100,
    'regressor__max_depth': 20
}
## 特征重要性 TOP5
特征	重要性
Gross_Margin (毛利率)	0.42
Quantity (销售数量)	0.23
Discount (折扣)	0.15
Avg_Unit_Price (平均单价)	0.08
Region_West (西部地区)	0.04
## 业务洞察
基于数据分析发现的关键结论：

高折扣风险：折扣超过50%的订单中，亏损率高达23%

区域差异：西部地区平均利润率比东部地区高8%

核心驱动：毛利率、销量、折扣贡献了80%的利润解释力

优化空间：通过折扣优化，预计可提升8-12%的订单利润率

## 应用功能展示
输入参数
销售数量、平均单价、商品成本

折扣比例（0-50%）

商品类别、子类别

销售地区、客户类型、运输方式

## 输出结果
数学利润（基于公式计算）

模型预测利润（基于ML模型）

成本与销售额

最优地区推荐

定价合理性分析

## 在线演示
体验地址：https://your-app.streamlit.app

## 项目亮点
端到端完整流程：数据清洗 → 特征工程 → 模型训练 → 调参优化 → Web部署

业务价值导向：不仅做预测，还提供定价合理性和地区优化建议

模型解释性：特征重要性分析 + 数学利润对比，让预测"可解释"

工程规范：Pipeline保证数据一致性，GridSearchCV自动调优

开箱即用：一键训练、一键启动Web界面
