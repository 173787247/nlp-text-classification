# GitHub上传指南

## 使用GitHub Desktop上传项目

### 步骤1: 在GitHub Desktop中创建新仓库

1. 打开 **GitHub Desktop**
2. 点击菜单栏 **File** → **New Repository**（或按 `Ctrl+N`）
3. 填写仓库信息：
   - **Name**: `nlp-company-classification`（或您喜欢的名称）
   - **Description**: `NLP文本分类 - 公司类型分类模型`
   - **Local path**: 选择项目所在目录
     ```
     C:\Users\rchua\Desktop\AIFullStackDevelopment\nlp-company-classification
     ```
   - 勾选 **Initialize this repository with a README**（可选）
   - 点击 **Create Repository**

### 步骤2: 添加文件到Git

1. 在GitHub Desktop中，您会看到所有项目文件
2. 在左下角的 **Summary** 框中输入提交信息：
   ```
   Initial commit: NLP文本分类项目
   ```
3. 点击 **Commit to main**（或 **Commit to master**）

### 步骤3: 发布到GitHub

1. 点击右上角的 **Publish repository** 按钮
2. 如果已经发布过，点击 **Push origin** 按钮
3. 等待上传完成

### 步骤4: 获取仓库链接

1. 上传完成后，点击 **View on GitHub** 按钮
2. 复制浏览器地址栏中的URL
3. 格式类似：`https://github.com/您的用户名/nlp-company-classification`

### 步骤5: 提交作业

1. 将仓库链接复制到作业提交框
2. 点击"提交"按钮

## 使用命令行上传（可选）

如果您熟悉Git命令行，也可以使用以下命令：

```bash
cd C:\Users\rchua\Desktop\AIFullStackDevelopment\nlp-company-classification

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: NLP文本分类项目"

# 添加远程仓库（替换为您的仓库URL）
git remote add origin https://github.com/您的用户名/nlp-company-classification.git

# 推送到GitHub
git push -u origin main
```

## 注意事项

1. **不要上传数据文件**: `training.csv` 和 `testing.csv` 已在 `.gitignore` 中排除
2. **不要上传模型文件**: 训练生成的 `.pkl` 文件不会上传
3. **确保README.md完整**: 包含项目说明和使用方法
4. **检查requirements.txt**: 确保包含所有依赖包

## 项目文件结构

上传后，GitHub仓库应包含以下文件：

```
nlp-company-classification/
├── main.py                    # 主程序
├── config.py                  # 配置文件
├── data_loader.py             # 数据加载
├── model_trainer.py           # 模型训练
├── hyperparameter_tuner.py    # 超参数调优
├── requirements.txt           # 依赖包
├── README.md                  # 项目说明
├── GITHUB_UPLOAD_GUIDE.md     # 本指南
├── .gitignore                 # Git忽略文件
├── models/                    # 模型目录（空）
└── results/                   # 结果目录（空）
```

## 验证上传

上传完成后，请检查：

- [ ] 所有Python文件都已上传
- [ ] README.md文件存在且内容完整
- [ ] requirements.txt文件存在
- [ ] 仓库链接可以正常访问
- [ ] 代码可以正常查看

## 问题排查

### 问题1: 文件没有显示在GitHub Desktop中

**解决方案**: 
- 检查文件是否在项目目录中
- 检查 `.gitignore` 是否排除了这些文件
- 尝试刷新GitHub Desktop（按 `F5`）

### 问题2: 推送失败

**解决方案**:
- 检查网络连接
- 检查GitHub账户是否已登录
- 尝试使用命令行推送

### 问题3: 找不到仓库链接

**解决方案**:
- 在GitHub Desktop中点击 **Repository** → **View on GitHub**
- 或直接在GitHub网站搜索您的仓库名称

## 完成！

上传成功后，您就可以将仓库链接提交到作业系统了！

