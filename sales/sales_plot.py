import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# 字体设置
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

try:
    importance_df = pd.read_csv("feature_importance.csv")
    print("特征重要性数据加载成功")
except FileNotFoundError:
    print("错误：找不到 feature_importance.csv，请先运行 sales_train.py")
    sys.exit(1)

plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=importance_df)
plt.title('TOP10 重要特征', fontsize=14, fontweight='bold')
plt.xlabel('重要性分数', fontsize=12)
plt.ylabel('特征名称', fontsize=12)
plt.tight_layout()
plt.show()
