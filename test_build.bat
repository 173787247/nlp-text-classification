@echo off
REM Docker构建测试脚本 (Windows)

echo ==========================================
echo 测试Docker镜像构建
echo ==========================================

echo.
echo [1/3] 检查Docker环境...
docker info >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker未运行
    pause
    exit /b 1
)
echo [OK] Docker运行正常

echo.
echo [2/3] 验证Docker Compose配置...
docker-compose config >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker Compose配置有误
    pause
    exit /b 1
)
echo [OK] 配置验证通过

echo.
echo [3/3] 开始构建镜像（这可能需要几分钟）...
echo [提示] 首次构建需要下载基础镜像，请耐心等待...
docker build -t nlp-company-classification:test -f Dockerfile .

if errorlevel 1 (
    echo.
    echo [错误] 镜像构建失败
    pause
    exit /b 1
)

echo.
echo ==========================================
echo [成功] 镜像构建完成！
echo ==========================================
echo.
echo 下一步可以运行：
echo   1. docker-compose up --build
echo   2. 或双击 docker-run.bat
echo.
pause

