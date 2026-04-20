# Sales-Prediction-ML
本项目基于零售订单数据与在线电商交易数据，构建机器学习回归模型实现销售额预测，包含完整的数据处理、特征工程、模型训练、超参调优、特征重要性分析及可视化交互界面。
##支持功能：
- 多数据源接入：Excel / CSV / MySQL
- 线性回归与随机森林回归模型对比
- GridSearchCV 自动超参调优
- 模型持久化与批量预测
- Streamlit 交互式可视化部署
##技术栈
- 语言：Python
- 数据分析：Pandas、NumPy
- 机器学习：Scikit-learn
- 可视化：Matplotlib、Seaborn、Streamlit
- 数据库：MySQL + SQLAlchemy
- 模型保存：Joblib
##项目结构
```
├── data/                     # 数据集目录
├── sales_train.py            # 零售数据模型训练
├── sales_plot.py             # 特征重要性可视化
├── sales_predict.py          # 单样本预测脚本
├── online_train.py           # 在线零售模型训练
├── online_plot.py            # 在线零售特征可视化
├── online_predict.py         # 在线零售预测
├── mysql_schema.sql          # MySQL 建表语句
├── mysql_export.py           # 数据库导出为CSV
├── app.py                    # Streamlit 可视化交互页面
├── requirements.txt          # 依赖清单
└── README.md
```
##快速开始
1. 安装依赖
```
pip install -r requirements.txt
```
2. 训练模型
```
python sales_train.py
python online_train.py
```
4. 启动可视化界面
```
streamlit run app.py
```
模型与评估
- 模型：随机森林回归（RandomForestRegressor）
- 评估指标：R²、MAE、RMSE
