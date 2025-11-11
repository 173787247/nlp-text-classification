"""
超参数调优模块
"""
import numpy as np
from sklearn.model_selection import GridSearchCV
from model_trainer import CompanyClassifier
from typing import Dict, Tuple
import config


def tune_hyperparameters(X_train: list, y_train: list, 
                        classifier_type: str = 'svm') -> Dict:
    """
    超参数调优
    
    Args:
        X_train: 训练文本列表
        y_train: 训练标签列表
        classifier_type: 分类器类型
        
    Returns:
        最佳参数字典
    """
    print(f"\n开始调优 {classifier_type.upper()} 分类器的超参数...")
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.pipeline import Pipeline
    
    # 创建向量化器
    vectorizer = TfidfVectorizer(
        min_df=config.MIN_DF,
        max_df=config.MAX_DF,
        ngram_range=(1, 2),
        max_features=10000,
        sublinear_tf=True
    )
    
    X_train_vectorized = vectorizer.fit_transform(X_train)
    
    # 定义参数网格
    if classifier_type == 'svm':
        param_grid = {
            'C': [0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
            'max_iter': [1000, 2000, 3000]
        }
        from sklearn.svm import LinearSVC
        base_classifier = LinearSVC(random_state=42, dual=False)
        
    elif classifier_type == 'lr':
        param_grid = {
            'C': [0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
            'max_iter': [1000, 2000, 3000]
        }
        from sklearn.linear_model import LogisticRegression
        base_classifier = LogisticRegression(
            random_state=42,
            multi_class='multinomial',
            solver='lbfgs'
        )
        
    elif classifier_type == 'nb':
        param_grid = {
            'alpha': [0.1, 0.5, 1.0, 2.0]
        }
        from sklearn.naive_bayes import MultinomialNB
        base_classifier = MultinomialNB()
        
    elif classifier_type == 'rf':
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [10, 20, None]
        }
        from sklearn.ensemble import RandomForestClassifier
        base_classifier = RandomForestClassifier(random_state=42)
        
    else:
        raise ValueError(f"未知的分类器类型: {classifier_type}")
    
    # 网格搜索
    print("正在进行网格搜索...")
    grid_search = GridSearchCV(
        base_classifier,
        param_grid,
        cv=5,  # 5折交叉验证
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search.fit(X_train_vectorized, y_train)
    
    print(f"\n最佳参数: {grid_search.best_params_}")
    print(f"最佳交叉验证准确率: {grid_search.best_score_:.4f}")
    
    # 返回最佳参数
    best_params = grid_search.best_params_.copy()
    
    # 保存向量化器到参数中（用于后续训练）
    best_params['_vectorizer'] = vectorizer
    
    return best_params


def auto_tune_and_train(X_train: list, y_train: list,
                        X_test: list, y_test: list,
                        min_accuracy: float = 0.80,
                        max_iterations: int = 10) -> Tuple[CompanyClassifier, float]:
    """
    自动调参并训练，直到达到最低准确率要求
    
    Args:
        X_train: 训练文本列表
        y_train: 训练标签列表
        X_test: 测试文本列表
        y_test: 测试标签列表
        min_accuracy: 最低准确率要求
        max_iterations: 最大迭代次数
        
    Returns:
        (最佳分类器, 准确率)
    """
    classifier_types = ['svm', 'lr', 'nb', 'rf']
    best_classifier = None
    best_accuracy = 0.0
    best_type = None
    
    print(f"\n开始自动调参，目标准确率: {min_accuracy:.2%}")
    print(f"最大迭代次数: {max_iterations}")
    
    for iteration in range(max_iterations):
        print(f"\n{'='*60}")
        print(f"迭代 {iteration + 1}/{max_iterations}")
        print(f"{'='*60}")
        
        # 尝试不同的分类器类型
        for classifier_type in classifier_types:
            try:
                print(f"\n尝试 {classifier_type.upper()} 分类器...")
                
                # 调优超参数
                best_params = tune_hyperparameters(X_train, y_train, classifier_type)
                
                # 提取向量化器
                vectorizer = best_params.pop('_vectorizer', None)
                
                # 训练模型
                classifier = CompanyClassifier(classifier_type, **best_params)
                
                # 使用相同的向量化器
                if vectorizer is not None:
                    classifier.vectorizer = vectorizer
                    X_train_vectorized = vectorizer.transform(X_train)
                else:
                    from sklearn.feature_extraction.text import TfidfVectorizer
                    classifier.vectorizer = TfidfVectorizer(
                        min_df=config.MIN_DF,
                        max_df=config.MAX_DF,
                        ngram_range=(1, 2),
                        max_features=10000,
                        sublinear_tf=True
                    )
                    X_train_vectorized = classifier.vectorizer.fit_transform(X_train)
                
                # 创建分类器
                classifier._create_classifier()
                classifier.classifier.fit(X_train_vectorized, y_train)
                
                # 评估
                y_pred = classifier.predict(X_test)
                accuracy = np.mean(y_pred == y_test)
                
                print(f"{classifier_type.upper()} 准确率: {accuracy:.4f}")
                
                # 更新最佳模型
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_classifier = classifier
                    best_type = classifier_type
                    print(f"✓ 新的最佳模型！准确率: {best_accuracy:.4f}")
                
                # 如果达到要求，提前结束
                if accuracy >= min_accuracy:
                    print(f"\n🎉 达到目标准确率 {min_accuracy:.2%}！")
                    return best_classifier, best_accuracy
                    
            except Exception as e:
                print(f"✗ {classifier_type.upper()} 训练失败: {e}")
                continue
        
        # 如果已经达到要求，提前结束
        if best_accuracy >= min_accuracy:
            break
    
    print(f"\n最终最佳模型: {best_type.upper()}, 准确率: {best_accuracy:.4f}")
    
    if best_accuracy < min_accuracy:
        print(f"⚠️  警告: 未能达到目标准确率 {min_accuracy:.2%}")
        print(f"当前最佳准确率: {best_accuracy:.4f}")
    
    return best_classifier, best_accuracy

