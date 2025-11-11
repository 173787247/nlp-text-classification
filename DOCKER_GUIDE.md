# Docker部署指南

## 概述

本项目支持使用Docker和Docker Compose进行部署，支持GPU加速（NVIDIA GPU）。

## 前置要求

1. **Docker Desktop** 已安装并运行
2. **NVIDIA GPU**（可选，用于加速训练）
3. **NVIDIA Container Toolkit**（如果使用GPU）

## 快速开始

### 方式1: 使用Docker Compose（推荐）

#### CPU版本
```bash
docker-compose up --build
```

#### GPU版本
```bash
docker-compose -f docker-compose.gpu.yml up --build
```

### 方式2: 使用脚本（Windows）

双击运行 `docker-run.bat`，脚本会自动检测GPU并选择相应版本。

### 方式3: 手动构建和运行

#### 构建镜像
```bash
docker build -t nlp-company-classification .
```

#### 运行容器（CPU）
```bash
docker run -it --rm \
  -v "C:\Users\rchua\WPSDrive\372901964\WPS云盘\桌面\AIFullStackDevelopment\deepseek-quickstart\NLP-文本分类:/app/data:ro" \
  -v "./models:/app/models" \
  -v "./results:/app/results" \
  nlp-company-classification
```

#### 运行容器（GPU）
```bash
docker run -it --rm \
  --gpus all \
  -v "C:\Users\rchua\WPSDrive\372901964\WPS云盘\桌面\AIFullStackDevelopment\deepseek-quickstart\NLP-文本分类:/app/data:ro" \
  -v "./models:/app/models" \
  -v "./results:/app/results" \
  -e CUDA_VISIBLE_DEVICES=0 \
  nlp-company-classification
```

## 配置说明

### 数据路径配置

在 `docker-compose.yml` 中，数据目录挂载路径为：
```yaml
volumes:
  - C:\Users\rchua\WPSDrive\372901964\WPS云盘\桌面\AIFullStackDevelopment\deepseek-quickstart\NLP-文本分类:/app/data:ro
```

如果您的数据路径不同，请修改此路径。

### GPU配置

项目使用 `pytorch/pytorch:2.7.0-cuda12.8-cudnn9-devel` 镜像，支持：
- CUDA 12.8
- cuDNN 9
- PyTorch 2.7.0

### 环境变量

- `CUDA_VISIBLE_DEVICES=0`: 指定使用的GPU设备
- `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512`: PyTorch GPU内存分配配置
- `OMP_NUM_THREADS=8`: OpenMP线程数

## 验证GPU支持

进入容器后，运行以下命令验证GPU：

```bash
python -c "import torch; print('GPU available:', torch.cuda.is_available()); print('GPU count:', torch.cuda.device_count() if torch.cuda.is_available() else 0)"
```

## 查看日志

```bash
# 查看容器日志
docker logs nlp-company-classification

# 实时查看日志
docker logs -f nlp-company-classification
```

## 停止和清理

```bash
# 停止容器
docker-compose down

# 停止并删除卷
docker-compose down -v

# 删除镜像
docker rmi nlp-company-classification
```

## 常见问题

### 1. GPU不可用

**问题**: `torch.cuda.is_available()` 返回 `False`

**解决方案**:
- 确保安装了NVIDIA Container Toolkit
- 检查Docker Desktop的GPU支持是否启用
- 运行 `nvidia-smi` 验证GPU驱动

### 2. 数据文件找不到

**问题**: 容器内找不到数据文件

**解决方案**:
- 检查 `docker-compose.yml` 中的挂载路径是否正确
- 确保数据文件存在于指定路径
- 检查路径中的中文字符是否正确编码

### 3. 内存不足

**问题**: 训练过程中内存不足

**解决方案**:
- 减少 `max_features` 参数（在 `config.py` 中）
- 减少 `OMP_NUM_THREADS` 环境变量
- 使用更小的批次大小

### 4. 权限问题

**问题**: 无法写入模型或结果目录

**解决方案**:
- 确保本地目录有写权限
- 检查Docker Desktop的文件共享设置

## 性能优化

### GPU加速

虽然本项目主要使用CPU进行文本分类，但可以通过以下方式利用GPU：

1. **使用GPU加速的NumPy替代品**:
   ```dockerfile
   RUN pip install cupy-cuda12x
   ```

2. **使用GPU加速的scikit-learn**:
   ```bash
   pip install scikit-learn-intelex
   ```

### 多GPU支持

如果需要使用多个GPU，修改 `docker-compose.yml`:
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all  # 使用所有GPU
          capabilities: [gpu]
```

## 参考

本项目参考了以下项目的Docker配置：
- `fashion-product-search`: PyTorch CUDA镜像配置
- `intelligent-customer-service`: Docker Compose配置

## 下一步

训练完成后，模型和结果将保存在：
- 模型: `./models/classifier_*.pkl`
- 结果: `./results/results_*.json`

