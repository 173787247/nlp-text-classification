#!/bin/bash
# Docker构建测试脚本

echo "=========================================="
echo "测试Docker镜像构建"
echo "=========================================="

echo "1. 测试Dockerfile语法..."
docker build --dry-run -f Dockerfile . 2>&1 | head -20

echo ""
echo "2. 开始构建镜像（仅测试构建过程，不运行）..."
docker build -t nlp-company-classification:test -f Dockerfile . 2>&1 | tail -10

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ 镜像构建成功！"
    echo ""
    echo "可以运行以下命令启动容器："
    echo "  docker-compose up"
    echo "  或"
    echo "  docker-compose -f docker-compose.gpu.yml up"
else
    echo ""
    echo "✗ 镜像构建失败，请检查错误信息"
    exit 1
fi

