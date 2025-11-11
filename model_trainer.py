"""
模型训练模块
"""
import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from typing import Tuple, Dict
import config


class CompanyClassifier:
    """公司类型分类器"""
    
    def __init__(self, classifier_type: str = 'svm', **kwargs):
        """
        初始化分类器
        
        Args:
            classifier_type: 分类器类型 ('svm', 'lr', 'nb', 'rf')
            **kwargs: 分类器参数
        """
        self.classifier_type = classifier_type
        self.vectorizer = None
        self.classifier = None
        self.pipeline = None
        self.params = kwargs
        
    def _create_classifier(self):
        """创建分类器"""
        if self.classifier_type == 'svm':
            self.classifier = LinearSVC(
                C=self.params.get('C', 1.0),
                max_iter=self.params.get('max_iter', 1000),
                random_state=42,
                dual=False
            )
        elif self.classifier_type == 'lr':
            self.classifier = LogisticRegression(
                C=self.params.get('C', 1.0),
                max_iter=self.params.get('max_iter', 1000),
                random_state=42,
                multi_class='multinomial',
                solver='lbfgs'
            )
        elif self.classifier_type == 'nb':
            self.classifier = MultinomialNB(
                alpha=self.params.get('alpha', 1.0)
            )
        elif self.classifier_type == 'rf':
            self.classifier = RandomForestClassifier(
                n_estimators=self.params.get('n_estimators', 100),
                max_depth=self.params.get('max_depth', None),
                random_state=42
            )
        else:
            raise ValueError(f"未知的分类器类型: {self.classifier_type}")
    
    def train(self, X_train: list, y_train: list, min_df: int = 2, max_df: float = 0.95):
        """
        训练模型
        
        Args:
            X_train: 训练文本列表
            y_train: 训练标签列表
            min_df: 最小文档频率
            max_df: 最大文档频率
        """
        print(f"\n开始训练 {self.classifier_type.upper()} 分类器...")
        
        # 创建TF-IDF向量化器
        self.vectorizer = TfidfVectorizer(
            min_df=min_df,
            max_df=max_df,
            ngram_range=(1, 2),  # 使用1-gram和2-gram
            max_features=10000,  # 最大特征数
            sublinear_tf=True  # 使用对数缩放
        )
        
        # 创建分类器
        self._create_classifier()
        
        # 创建Pipeline
        self.pipeline = Pipeline([
            ('tfidf', self.vectorizer),
            ('classifier', self.classifier)
        ])
        
        # 训练
        print("正在向量化文本...")
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        print(f"特征维度: {X_train_vectorized.shape}")
        
        print("正在训练分类器...")
        self.classifier.fit(X_train_vectorized, y_train)
        
        print("训练完成！")
    
    def predict(self, X_test: list) -> np.ndarray:
        """
        预测
        
        Args:
            X_test: 测试文本列表
            
        Returns:
            预测标签数组
        """
        if self.vectorizer is None or self.classifier is None:
            raise ValueError("模型尚未训练，请先调用train()方法")
        
        X_test_vectorized = self.vectorizer.transform(X_test)
        return self.classifier.predict(X_test_vectorized)
    
    def evaluate(self, X_test: list, y_test: list) -> Dict[str, float]:
        """
        评估模型
        
        Args:
            X_test: 测试文本列表
            y_test: 真实标签列表
            
        Returns:
            评估指标字典
        """
        y_pred = self.predict(X_test)
        
        accuracy = np.mean(y_pred == y_test)
        
        from sklearn.metrics import classification_report, confusion_matrix
        
        report = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm.tolist()
        }
    
    def save(self, filepath: str):
        """
        保存模型
        
        Args:
            filepath: 保存路径
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'classifier': self.classifier,
                'classifier_type': self.classifier_type,
                'params': self.params
            }, f)
        print(f"模型已保存到: {filepath}")
    
    @classmethod
    def load(cls, filepath: str):
        """
        加载模型
        
        Args:
            filepath: 模型文件路径
            
        Returns:
            CompanyClassifier实例
        """
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        instance = cls(data['classifier_type'], **data['params'])
        instance.vectorizer = data['vectorizer']
        instance.classifier = data['classifier']
        
        return instance


def train_model(X_train: list, y_train: list, 
                classifier_type: str = 'svm',
                min_df: int = 2,
                max_df: float = 0.95,
                **kwargs) -> CompanyClassifier:
    """
    训练模型
    
    Args:
        X_train: 训练文本列表
        y_train: 训练标签列表
        classifier_type: 分类器类型
        min_df: 最小文档频率
        max_df: 最大文档频率
        **kwargs: 分类器参数
        
    Returns:
        训练好的分类器
    """
    classifier = CompanyClassifier(classifier_type, **kwargs)
    classifier.train(X_train, y_train, min_df, max_df)
    return classifier

