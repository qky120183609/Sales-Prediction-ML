import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===================== 中文显示 =====================
import warnings
warnings.filterwarnings("ignore")

import logging
logging.getLogger('matplotlib').setLevel(logging.CRITICAL)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
# ====================================================

# 直接读取已保存的特征重要性
imp_df = pd.read_csv("online_feature_importance.csv")

# 绘图
plt.figure(figsize=(8,4))
sns.barplot(x="importance", y="feature", data=imp_df.head(5))
plt.title("在线零售 特征重要性TOP5")
plt.tight_layout()
plt.show()
