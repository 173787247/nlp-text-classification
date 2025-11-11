"""
测试模块导入
"""
import sys
import os

print("Testing module imports...")
print("=" * 60)

# 测试config
try:
    import config
    print("[OK] config module imported successfully")
except Exception as e:
    print(f"[ERROR] config import failed: {e}")
    sys.exit(1)

# 测试data_loader
try:
    from data_loader import load_data, preprocess_texts
    print("[OK] data_loader module imported successfully")
except Exception as e:
    print(f"[ERROR] data_loader import failed: {e}")
    sys.exit(1)

# 测试model_trainer
try:
    from model_trainer import CompanyClassifier, train_model
    print("[OK] model_trainer module imported successfully")
except Exception as e:
    print(f"[ERROR] model_trainer import failed: {e}")
    sys.exit(1)

# 测试hyperparameter_tuner
try:
    from hyperparameter_tuner import auto_tune_and_train, tune_hyperparameters
    print("[OK] hyperparameter_tuner module imported successfully")
except Exception as e:
    print(f"[ERROR] hyperparameter_tuner import failed: {e}")
    sys.exit(1)

# 检查数据文件
print("\nChecking data files...")
print("=" * 60)
if os.path.exists(config.TRAINING_DATA):
    print(f"[OK] Training data exists: {config.TRAINING_DATA}")
else:
    print(f"[ERROR] Training data not found: {config.TRAINING_DATA}")

if os.path.exists(config.TESTING_DATA):
    print(f"[OK] Testing data exists: {config.TESTING_DATA}")
else:
    print(f"[ERROR] Testing data not found: {config.TESTING_DATA}")

print("\nAll imports successful!")

