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

#忽略警告
import warnings
warnings.filterwarnings("ignore")

#----------------------------------------------#
# 1. 数据读取（支持MySQL和CSV）
#----------------------------------------------#
USE_MYSQL = False  # 改成True就用MySQL，False就用CSV

if USE_MYSQL:
    # 从MySQL读取
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    engine = create_engine(f"mysql+pymysql://root:{MYSQL_PASSWORD}@localhost:3306/sales_data")
    df = pd.read_sql("SELECT * FROM online_retail", engine)
    print("数据来源：MySQL数据库")
else:
    # 从Excel读取
    df = pd.read_csv("retail_online.csv")
    print("数据来源：CSV文件")


# 数据清洗
df = df.dropna(subset=["Quantity", "UnitPrice"])
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

df = df.sample(10000, random_state=2)

# 构造目标：总价
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

target = "TotalPrice"
numeric_features = ["Quantity", "UnitPrice"]
categorical_features = ["Country"]

X = df[numeric_features + categorical_features]
y = df[target]

# 划分训练集 测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#----------------------------------------------#
# 2. 特征预处理流水线
#----------------------------------------------#
# 数值特征：填充缺失 + 标准化
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# 类别特征：填充缺失 + 独热编码
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# 合并预处理
preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

#----------------------------------------------#
# 3. 线性回归模型
#----------------------------------------------#
lr_pipe = Pipeline(steps=[
    ("pre", preprocessor),
    ("model", LinearRegression())
])
lr_pipe.fit(X_train,y_train)
y_pred_lr = lr_pipe.predict(X_test)

print("\n===== 线性回归结果 =====")
print(f"R²: {r2_score(y_test, y_pred_lr):.3f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred_lr):.2f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lr)):.2f}")

#----------------------------------------------#
# 4. 随机森林模型
#----------------------------------------------#
rf_pipe = Pipeline(steps=[
    ("pre", preprocessor),
    ("model", RandomForestRegressor(random_state=2))
])
rf_pipe.fit(X_train,y_train)
y_pred_rf = rf_pipe.predict(X_test)

print("\n===== 随机森林结果 =====")
print(f"R²: {r2_score(y_test, y_pred_rf):.3f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred_rf):.2f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_rf)):.2f}")

#----------------------------------------------#
# 5. 网格搜索调参
#----------------------------------------------#
param_grid = {
    "model__n_estimators": [100],
    "model__max_depth": [20]
}

grid = GridSearchCV(rf_pipe, param_grid, cv=3, scoring="r2", n_jobs=1)
grid.fit(X_train, y_train)
best_model = grid.best_estimator_

print("\n===== 网格搜索最优参数 =====")
print(grid.best_params_)
print(f"最佳交叉验证 R²: {grid.best_score_:.3f}")

#----------------------------------------------#
# 6. 特征重要性
#----------------------------------------------#
importances = best_model.named_steps["model"].feature_importances_
ohe = best_model.named_steps["pre"].transformers_[1][1].named_steps["onehot"]
cat_names = ohe.get_feature_names_out(categorical_features).tolist()
all_features = numeric_features + cat_names

imp_df = pd.DataFrame({
    "feature": all_features,
    "importance": importances
}).sort_values("importance", ascending=False)

# 保存特征重要性
imp_df.to_csv("online_feature_importance.csv", index=False)

print("\n特征重要性 TOP10")
print(imp_df)

#----------------------------------------------#
# 7. 保存模型
#----------------------------------------------#
joblib.dump(best_model, "online_sales_model.pkl")

print("在线零售模型训练完成！已保存：")
print("online_feature_importance.csv")
print("online_sales_model.pkl")
