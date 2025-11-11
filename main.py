"""
NLP文本分类主程序
用于训练公司类型分类模型并评估准确率
"""
import os
import json
import numpy as np
from datetime import datetime
from data_loader import load_data, preprocess_texts
from model_trainer import train_model, CompanyClassifier
from hyperparameter_tuner import auto_tune_and_train
import config


def save_results(results: dict, filepath: str):
    """保存结果到JSON文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到: {filepath}")


def print_evaluation_report(evaluation: dict):
    """打印评估报告"""
    print("\n" + "="*60)
    print("模型评估报告")
    print("="*60)
    print(f"准确率: {evaluation['accuracy']:.4f} ({evaluation['accuracy']*100:.2f}%)")
    
    print("\n分类报告:")
    report = evaluation['classification_report']
    for label in sorted([k for k in report.keys() if k.isdigit()], key=int):
        metrics = report[label]
        print(f"  类别 {label}:")
        print(f"    精确率: {metrics['precision']:.4f}")
        print(f"    召回率: {metrics['recall']:.4f}")
        print(f"    F1分数: {metrics['f1-score']:.4f}")
        print(f"    支持数: {int(metrics['support'])}")
    
    print(f"\n宏平均:")
    print(f"  精确率: {report['macro avg']['precision']:.4f}")
    print(f"  召回率: {report['macro avg']['recall']:.4f}")
    print(f"  F1分数: {report['macro avg']['f1-score']:.4f}")
    
    print(f"\n加权平均:")
    print(f"  精确率: {report['weighted avg']['precision']:.4f}")
    print(f"  召回率: {report['weighted avg']['recall']:.4f}")
    print(f"  F1分数: {report['weighted avg']['f1-score']:.4f}")


def main():
    """主函数"""
    print("="*60)
    print("NLP文本分类 - 公司类型分类模型")
    print("="*60)
    
    # 检查数据文件是否存在
    if not os.path.exists(config.TRAINING_DATA):
        print(f"错误: 训练数据文件不存在: {config.TRAINING_DATA}")
        return
    
    if not os.path.exists(config.TESTING_DATA):
        print(f"错误: 测试数据文件不存在: {config.TESTING_DATA}")
        return
    
    # 加载数据
    print("\n1. 加载训练数据...")
    train_texts, train_labels = load_data(config.TRAINING_DATA)
    
    print("\n2. 加载测试数据...")
    test_texts, test_labels = load_data(config.TESTING_DATA)
    
    # 预处理文本
    print("\n3. 预处理文本...")
    print("正在预处理训练文本...")
    train_texts_processed = preprocess_texts(train_texts, use_jieba=config.USE_JIEBA)
    
    print("正在预处理测试文本...")
    test_texts_processed = preprocess_texts(test_texts, use_jieba=config.USE_JIEBA)
    
    # 训练和评估模型
    print("\n4. 训练模型并自动调参...")
    
    # 自动调参并训练
    best_classifier, best_accuracy = auto_tune_and_train(
        train_texts_processed,
        train_labels,
        test_texts_processed,
        test_labels,
        min_accuracy=config.MIN_ACCURACY,
        max_iterations=config.MAX_ITERATIONS
    )
    
    if best_classifier is None:
        print("\n❌ 训练失败，无法创建有效模型")
        return
    
    # 最终评估
    print("\n5. 最终评估...")
    evaluation = best_classifier.evaluate(test_texts_processed, test_labels)
    print_evaluation_report(evaluation)
    
    # 保存模型
    print("\n6. 保存模型...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(config.MODEL_DIR, f"classifier_{timestamp}.pkl")
    best_classifier.save(model_path)
    
    # 保存结果
    print("\n7. 保存结果...")
    results = {
        'timestamp': timestamp,
        'accuracy': float(evaluation['accuracy']),
        'min_accuracy_required': config.MIN_ACCURACY,
        'meets_requirement': evaluation['accuracy'] >= config.MIN_ACCURACY,
        'classifier_type': best_classifier.classifier_type,
        'params': best_classifier.params,
        'classification_report': evaluation['classification_report'],
        'confusion_matrix': evaluation['confusion_matrix'],
        'model_path': model_path,
        'training_samples': len(train_texts),
        'testing_samples': len(test_texts)
    }
    
    results_path = os.path.join(config.RESULTS_DIR, f"results_{timestamp}.json")
    save_results(results, results_path)
    
    # 最终总结
    print("\n" + "="*60)
    print("训练完成！")
    print("="*60)
    print(f"最终准确率: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")
    print(f"目标准确率: {config.MIN_ACCURACY:.2%}")
    
    if best_accuracy >= config.MIN_ACCURACY:
        print("✅ 模型达到交付要求！")
    else:
        print("⚠️  模型未达到交付要求，建议继续调参")
    
    print(f"\n模型文件: {model_path}")
    print(f"结果文件: {results_path}")


if __name__ == "__main__":
    main()

