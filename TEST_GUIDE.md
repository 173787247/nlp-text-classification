# 测试指南

## 更新Docker Desktop后的测试步骤

### 步骤1: 验证Docker环境

更新Docker Desktop后，运行环境测试：

```bash
python test_docker_setup.py
```

这个脚本会检查：
- ✅ Docker版本
- ✅ Docker服务状态
- ✅ Docker Compose版本
- ✅ GPU支持（如果可用）
- ✅ 项目文件完整性
- ✅ 数据文件路径

### 步骤2: 测试Docker配置（不构建镜像）

验证Docker Compose配置是否正确：

```bash
# 验证配置文件语法
docker-compose config

# 验证GPU版本配置
docker-compose -f docker-compose.gpu.yml config
```

### 步骤3: 构建和运行（完整测试）

#### 方式1: 使用脚本（推荐）

**Windows**:
```bash
docker-run.bat
```

**Linux/Mac**:
```bash
bash docker-run.sh
```

#### 方式2: 手动运行

**CPU版本**:
```bash
docker-compose up --build
```

**GPU版本**:
```bash
docker-compose -f docker-compose.gpu.yml up --build
```

### 步骤4: 验证容器运行

在另一个终端中检查容器状态：

```bash
# 查看运行中的容器
docker ps

# 查看容器日志
docker logs nlp-company-classification

# 进入容器（如果需要调试）
docker exec -it nlp-company-classification /bin/bash
```

### 步骤5: 验证GPU（如果使用GPU版本）

进入容器后运行：

```bash
python -c "import torch; print('GPU available:', torch.cuda.is_available()); print('GPU count:', torch.cuda.device_count() if torch.cuda.is_available() else 0)"
```

## 常见问题排查

### 问题1: Docker Desktop未启动

**症状**: `docker info` 命令失败

**解决**: 
1. 打开Docker Desktop应用
2. 等待Docker完全启动（图标不再闪烁）
3. 重新运行测试

### 问题2: GPU不可用

**症状**: `nvidia-smi` 命令失败或Docker无法访问GPU

**解决**:
1. 确保安装了NVIDIA驱动
2. 在Docker Desktop设置中启用GPU支持
3. 安装NVIDIA Container Toolkit（如果需要）
4. 使用CPU版本：`docker-compose up --build`

### 问题3: 构建失败

**症状**: `docker-compose up --build` 在构建阶段失败

**解决**:
1. 检查网络连接（需要下载镜像）
2. 检查Dockerfile语法
3. 查看详细错误信息：`docker-compose up --build --verbose`

### 问题4: 数据文件找不到

**症状**: 容器内找不到训练/测试数据

**解决**:
1. 检查 `docker-compose.yml` 中的挂载路径
2. 确保数据文件存在于指定路径
3. 检查路径中的中文字符是否正确

### 问题5: 权限问题

**症状**: 无法写入模型或结果目录

**解决**:
1. 确保本地目录有写权限
2. 检查Docker Desktop的文件共享设置
3. 在Windows上，确保路径在Docker Desktop的共享驱动器中

## 快速测试清单

更新Docker Desktop后，按以下顺序测试：

- [ ] 运行 `python test_docker_setup.py` 验证环境
- [ ] 运行 `docker-compose config` 验证配置
- [ ] 运行 `docker-run.bat` 或 `docker-compose up --build` 构建镜像
- [ ] 检查容器日志确认训练开始
- [ ] 验证模型和结果文件生成

## 预期结果

成功运行后，您应该看到：

1. **容器启动**: 容器名称 `nlp-company-classification` 运行中
2. **训练开始**: 日志显示数据加载和模型训练过程
3. **文件生成**: 
   - `./models/classifier_*.pkl` - 训练好的模型
   - `./results/results_*.json` - 训练结果和评估报告

## 需要帮助？

如果遇到问题：

1. 查看容器日志：`docker logs nlp-company-classification`
2. 检查Docker Desktop日志
3. 运行 `test_docker_setup.py` 获取详细诊断信息

