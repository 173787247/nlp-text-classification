"""
快速测试脚本 - 检查环境和依赖
"""
import sys
import os

print("=" * 60)
print("NLP文本分类项目 - 快速测试")
print("=" * 60)

# 检查Python版本
print(f"\n1. Python版本: {sys.version}")

# 检查依赖包
print("\n2. 检查依赖包...")
required_packages = {
    'pandas': 'pandas',
    'numpy': 'numpy',
    'sklearn': 'scikit-learn',
    'jieba': 'jieba',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn'
}

missing_packages = []
for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
        print(f"  [OK] {package_name}")
    except ImportError:
        print(f"  [MISSING] {package_name}")
        missing_packages.append(package_name)

if missing_packages:
    print(f"\n缺少以下依赖包: {', '.join(missing_packages)}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)

# 检查数据文件
print("\n3. 检查数据文件...")
try:
    import config
    if os.path.exists(config.TRAINING_DATA):
        print(f"  [OK] 训练数据: {config.TRAINING_DATA}")
    else:
        print(f"  [ERROR] 训练数据不存在: {config.TRAINING_DATA}")
    
    if os.path.exists(config.TESTING_DATA):
        print(f"  [OK] 测试数据: {config.TESTING_DATA}")
    else:
        print(f"  [ERROR] 测试数据不存在: {config.TESTING_DATA}")
except Exception as e:
    print(f"  [ERROR] 无法加载配置: {e}")

# 测试模块导入
print("\n4. 测试模块导入...")
try:
    from data_loader import load_data, preprocess_texts
    print("  [OK] data_loader")
except Exception as e:
    print(f"  [ERROR] data_loader: {e}")

try:
    from model_trainer import CompanyClassifier
    print("  [OK] model_trainer")
except Exception as e:
    print(f"  [ERROR] model_trainer: {e}")

try:
    from hyperparameter_tuner import auto_tune_and_train
    print("  [OK] hyperparameter_tuner")
except Exception as e:
    print(f"  [ERROR] hyperparameter_tuner: {e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
print("\n如果所有检查都通过，可以运行: python main.py")

