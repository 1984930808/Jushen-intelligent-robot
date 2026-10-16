# 环境安装

## 系统要求

- Python 3.8+（推荐 3.10）  
- Windows / Linux / macOS  
- 可选：NVIDIA GPU + CUDA 11.0+（加速训练与推理）  

## 安装步骤

```bash
# 1. 获取代码
git clone <your-repo-url>
cd zsf

# 2. 建议使用虚拟环境
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

## GPU 版 PyTorch（可选）

若需要 CUDA，请按本机 CUDA 版本从 PyTorch 官网安装对应 wheel，例如：

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

## 验证安装

```bash
python -c "from ultralytics import YOLO; import torch; print('ok', torch.__version__)"
python run_demo.py
```

## 数据集（评估/训练需要）

Demo 与基础测试**不依赖**完整数据集（仓库已含 `best.pt` 与 `demo/sample.png`）。

若要训练或复现验证集指标：

1. 下载 `dataset.zip`（见 README 网盘链接）  
2. 解压到项目根目录，得到 `dataset/train|val|test`  
3. 运行：`python verify_dataset.py`  
