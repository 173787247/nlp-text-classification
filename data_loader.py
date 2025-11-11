"""
数据加载和预处理模块
"""
import pandas as pd
import numpy as np
import re
from typing import Tuple, List
import jieba
import config


def load_data(file_path: str) -> Tuple[List[str], List[int]]:
    """
    加载CSV数据文件
    
    Args:
        file_path: CSV文件路径
        
    Returns:
        texts: 文本列表
        labels: 标签列表（0-9）
    """
    try:
        # 读取CSV文件，第一列是标签，第二列是文本
        df = pd.read_csv(file_path, header=None, encoding='utf-8')
        
        # 检查列数
        if df.shape[1] == 2:
            # 标准格式：第一列是标签，第二列是文本
            labels = df.iloc[:, 0].astype(int).tolist()
            texts = df.iloc[:, 1].astype(str).tolist()
        elif df.shape[1] == 3:
            # 三列格式：第一列可能是序号，第二列是标签，第三列是文本
            labels = df.iloc[:, 1].astype(int).tolist()
            texts = df.iloc[:, 2].astype(str).tolist()
        else:
            raise ValueError(f"不支持的CSV格式，列数: {df.shape[1]}")
        
        # 确保标签在0-9范围内（如果标签大于9，取模）
        labels = [label % 10 if label >= 10 else label for label in labels]
        
        # 过滤空文本
        valid_indices = [i for i, text in enumerate(texts) if text and str(text).strip() != '']
        texts = [texts[i] for i in valid_indices]
        labels = [labels[i] for i in valid_indices]
        
        print(f"成功加载 {len(texts)} 条数据")
        print(f"标签分布: {pd.Series(labels).value_counts().sort_index().to_dict()}")
        
        return texts, labels
    
    except Exception as e:
        print(f"加载数据时出错: {e}")
        raise


def preprocess_text(text: str, use_jieba: bool = True) -> str:
    """
    文本预处理
    
    Args:
        text: 原始文本
        use_jieba: 是否使用jieba分词
        
    Returns:
        预处理后的文本
    """
    if pd.isna(text) or text == '':
        return ''
    
    # 去除特殊字符，保留中文、英文、数字
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', ' ', str(text))
    
    # 去除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 使用jieba分词
    if use_jieba and config.USE_JIEBA:
        try:
            words = jieba.cut(text)
            text = ' '.join(words)
        except:
            pass
    
    return text


def preprocess_texts(texts: List[str], use_jieba: bool = True) -> List[str]:
    """
    批量预处理文本
    
    Args:
        texts: 文本列表
        use_jieba: 是否使用jieba分词
        
    Returns:
        预处理后的文本列表
    """
    return [preprocess_text(text, use_jieba) for text in texts]

