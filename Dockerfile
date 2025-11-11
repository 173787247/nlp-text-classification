# 使用您现有的PyTorch CUDA镜像（支持GPU）
FROM pytorch/pytorch:2.7.0-cuda12.8-cudnn9-devel

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV CUDA_VISIBLE_DEVICES=0
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
ENV OMP_NUM_THREADS=8

# 设置工作目录
WORKDIR /app

# 安装系统依赖（PyTorch镜像已包含大部分工具，只需安装必要的）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 升级pip
RUN pip install --upgrade pip setuptools wheel

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p models results data

# 设置环境变量
ENV PYTHONPATH=/app

# 默认命令
CMD ["python", "main.py"]

