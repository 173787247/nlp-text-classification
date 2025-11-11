"""
Docker环境测试脚本
用于验证Docker配置是否正确
"""
import subprocess
import sys
import os

def run_command(cmd, check=True):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_docker():
    """测试Docker环境"""
    print("=" * 60)
    print("Docker环境测试")
    print("=" * 60)
    
    # 1. 检查Docker版本
    print("\n1. 检查Docker版本...")
    success, stdout, stderr = run_command("docker --version", check=False)
    if success:
        print(f"  [OK] {stdout.strip()}")
    else:
        print(f"  [ERROR] Docker未安装或未在PATH中")
        return False
    
    # 2. 检查Docker是否运行
    print("\n2. 检查Docker服务状态...")
    success, stdout, stderr = run_command("docker info", check=False)
    if success:
        print("  [OK] Docker服务正在运行")
    else:
        print("  [ERROR] Docker服务未运行，请启动Docker Desktop")
        return False
    
    # 3. 检查Docker Compose
    print("\n3. 检查Docker Compose...")
    success, stdout, stderr = run_command("docker-compose --version", check=False)
    if success:
        print(f"  [OK] {stdout.strip()}")
    else:
        print("  [ERROR] Docker Compose未安装")
        return False
    
    # 4. 检查GPU支持（可选）
    print("\n4. 检查GPU支持...")
    success, stdout, stderr = run_command("nvidia-smi", check=False)
    if success:
        print("  [OK] 检测到NVIDIA GPU")
        print(f"  GPU信息:\n{stdout[:200]}...")  # 只显示前200个字符
    else:
        print("  [INFO] 未检测到NVIDIA GPU，将使用CPU版本")
    
    # 5. 检查Dockerfile是否存在
    print("\n5. 检查项目文件...")
    files_to_check = [
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt",
        "main.py",
        "config.py"
    ]
    all_exist = True
    for file in files_to_check:
        if os.path.exists(file):
            print(f"  [OK] {file}")
        else:
            print(f"  [ERROR] {file} 不存在")
            all_exist = False
    
    if not all_exist:
        return False
    
    # 6. 检查数据文件路径
    print("\n6. 检查数据文件路径...")
    try:
        import config
        if os.path.exists(config.TRAINING_DATA):
            print(f"  [OK] 训练数据: {config.TRAINING_DATA}")
        else:
            print(f"  [WARNING] 训练数据不存在: {config.TRAINING_DATA}")
            print("            (Docker容器中会自动挂载)")
        
        if os.path.exists(config.TESTING_DATA):
            print(f"  [OK] 测试数据: {config.TESTING_DATA}")
        else:
            print(f"  [WARNING] 测试数据不存在: {config.TESTING_DATA}")
            print("            (Docker容器中会自动挂载)")
    except Exception as e:
        print(f"  [ERROR] 无法加载配置: {e}")
    
    print("\n" + "=" * 60)
    print("环境检查完成！")
    print("=" * 60)
    print("\n下一步:")
    print("1. 确保Docker Desktop已更新并运行")
    print("2. 运行: docker-compose up --build")
    print("   或使用: docker-run.bat")
    
    return True

if __name__ == "__main__":
    success = test_docker()
    sys.exit(0 if success else 1)

