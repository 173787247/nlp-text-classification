#!/bin/bash
# Docker运行脚本

echo "=========================================="
echo "NLP文本分类 - Docker运行脚本"
echo "=========================================="

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker未运行，请先启动Docker Desktop"
    exit 1
fi

# 检查是否有GPU
if command -v nvidia-smi &> /dev/null; then
    echo "检测到NVIDIA GPU，使用GPU版本..."
    docker-compose -f docker-compose.gpu.yml up --build
else
    echo "未检测到NVIDIA GPU，使用CPU版本..."
    docker-compose up --build
fi

