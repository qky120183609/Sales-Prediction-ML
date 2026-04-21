import os
import pandas as pd
import numpy as np
import joblib
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)
import matplotlib.pyplot as plt
import seaborn as sns

#通用中文+解决waning
import warnings
warnings.filterwarnings("ignore")

import logging
logging.getLogger('matplotlib').setLevel(logging.CRITICAL)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False



#----------------------------------------------#
# 1. 数据读取（支持MySQL和Excel）
#----------------------------------------------#
USE_MYSQL = False  # 改成True就用MySQL，False就用Excel

if USE_MYSQL:
    # 从MySQL读取
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    engine = create_engine(f"mysql+pymysql://root:{MYSQL_PASSWORD}@localhost:3306/sales_data")
    df = pd.read_sql("SELECT * FROM retail_sales", engine)
    print("数据来源：MySQL数据库")
else:
    # 从Excel读取
    df = pd.read_csv("retail_sales.csv")
    print("数据来源：CSV文件")


# 亏损订单分析
df["Is_Loss"] = df["Profit"] < 0
loss_rate = df["Is_Loss"].mean() * 100
print(f"\n亏损订单占比: {loss_rate:.1f}%")

# 折扣与亏损的关系
high_discount_loss = df[(df["Discount"] > 0.5) & (df["Profit"] < 0)].shape[0]
print(f"高折扣(>50%)导致亏损的订单数: {high_discount_loss}")



# 目标变量 + 特征
df = df[df["Quantity"] > 0]
df["Cost"] = df["Sales"] - df["Profit"]
df["Gross_Margin"] = df["Profit"] / df["Sales"] 

target = "Profit"
df["Avg_Unit_Price"] = df["Sales"] / df["Quantity"]
numeric_features = ["Quantity","Discount","Avg_Unit_Price","Gross_Margin"]
categorical_features = [
    "Category", 
    "Sub-Category", 
    "Region",
    "Segment",
    "Ship Mode", 
]

X = df[numeric_features + categorical_features]
y = df[target]

# 划分训练集 测试集
X_train, X_test, y_train, y_test = train_test_split(
    X,y,test_size=0.2,random_state=1
)

#----------------------------------------------#
# 2. 特征预处理流水线
#----------------------------------------------#
# 数值特征：填充缺失值 + 标准化
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# 类别特征：填充缺失 + OneHot编码
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore",sparse_output=False))
])

# 合并预处理
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

#----------------------------------------------#
# 3. 线性回归模型训练与评估
#----------------------------------------------#
lr_pipe = Pipeline(
    steps = [
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ]
)
lr_pipe.fit(X_train,y_train)
y_pred_lr = lr_pipe.predict(X_test)

print("\n===== 线性回归结果 =====")
print(f"R²: {r2_score(y_test, y_pred_lr):.3f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred_lr):.2f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lr)):.2f}")

#----------------------------------------------#
# 4. 随机森林模型训练与评估
#----------------------------------------------#
rf_pipe = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=1)),
])
rf_pipe.fit(X_train,y_train)
y_pred_rf = rf_pipe.predict(X_test)

print("\n===== 随机森林结果 =====")
print(f"R²: {r2_score(y_test, y_pred_rf):.3f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred_rf):.2f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_rf)):.2f}")

#----------------------------------------------#
# 5. 网格搜索最优参数
#----------------------------------------------#
param_grid = {
    'regressor__n_estimators': [50, 100],
    'regressor__max_depth': [None,10,20]
}

grid_search = GridSearchCV(
    rf_pipe,param_grid,cv=3,scoring='r2',n_jobs=1
)
grid_search.fit(X_train, y_train)

print("\n===== 网格搜索最优参数 =====")
print(grid_search.best_params_)
print(f"最佳交叉验证 R²: {grid_search.best_score_:.3f}")

#----------------------------------------------#
# 6. 特征重要性分析
#----------------------------------------------#
best_model = grid_search.best_estimator_
rf_model = best_model.named_steps['regressor']

ohe = best_model.named_steps['preprocessor'].transformers_[1][1].named_steps['onehot']
cat_feature_names = ohe.get_feature_names_out(categorical_features).tolist()
all_feature_names = numeric_features + cat_feature_names

importance_df = pd.DataFrame({
    "feature":all_feature_names,
    "importance": rf_model.feature_importances_,
}).sort_values('importance', ascending=False).head(10)

print("\n特征重要性 TOP10")
print(importance_df)

#----------------------------------------------#
# 7. 保存最优模型和特征重要性
#----------------------------------------------#

# 保存模型
joblib.dump(best_model, 'sales_model.pkl', compress=3)
print("\n模型已保存为 sales_model.pkl")

# 保存特征重要性到 CSV
importance_df.to_csv("feature_importance.csv", index=False)
print("特征重要性已保存为 feature_importance.csv")

# 保存模型评估指标
metrics_df = pd.DataFrame({
    "metric": ["R²", "MAE", "RMSE"],
    "value": [
        r2_score(y_test, y_pred_rf),
        mean_absolute_error(y_test, y_pred_rf),
        np.sqrt(mean_squared_error(y_test, y_pred_rf))
    ]
})
metrics_df.to_csv("model_metrics.csv", index=False)
print("模型评估指标已保存为 model_metrics.csv")

# 保存训练配置信息
config_df = pd.DataFrame({
    "config": ["best_params", "cv_best_score", "test_r2", "test_mae", "test_rmse"],
    "value": [
        str(grid_search.best_params_),
        grid_search.best_score_,
        r2_score(y_test, y_pred_rf),
        mean_absolute_error(y_test, y_pred_rf),
        np.sqrt(mean_squared_error(y_test, y_pred_rf))
    ]
})
config_df.to_csv("model_config.csv", index=False)
print("模型配置已保存为 model_config.csv")

print("\n" + "="*50)
print("模型训练完成！")
print(f"最优参数: {grid_search.best_params_}")
print(f"测试集 R²: {r2_score(y_test, y_pred_rf):.3f}")

