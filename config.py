"""
配置文件
"""
import os

# 数据路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 检查是否在Docker容器中运行
if os.path.exists("/app/data"):
    # Docker环境
    DATA_DIR = "/app/data"
else:
    # 本地环境
    DATA_DIR = r"C:\Users\rchua\WPSDrive\372901964\WPS云盘\桌面\AIFullStackDevelopment\deepseek-quickstart\NLP-文本分类"

TRAINING_DATA = os.path.join(DATA_DIR, "training.csv")
TESTING_DATA = os.path.join(DATA_DIR, "testing.csv")

# 模型保存路径
MODEL_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# 模型参数
MIN_ACCURACY = 0.80  # 最低准确率要求
MAX_ITERATIONS = 10  # 最大调参迭代次数

# 文本预处理参数
USE_JIEBA = True  # 是否使用jieba分词
MIN_DF = 2  # 最小文档频率
MAX_DF = 0.95  # 最大文档频率

# 分类器参数（初始值）
INITIAL_C = 1.0  # SVM的C参数初始值
INITIAL_MAX_ITER = 1000  # 最大迭代次数

