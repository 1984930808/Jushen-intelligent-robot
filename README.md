# YOLO目标检测项目

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![YOLO](https://img.shields.io/badge/YOLO-v11-orange.svg)](https://github.com/ultralytics/ultralytics)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)

一个基于YOLOv11的工业目标检测项目，支持17个类别的检测。
## 数据集

通过网盘分享的文件：dataset.zip
链接: https://pan.baidu.com/s/1bTLMJsUC7hQVHTSQraW0ZQ 提取码: 4kgy

## 项目简介

本项目提供了一个完整的YOLO目标检测解决方案，包括数据集准备、模型训练、预测推理等功能。项目针对工业场景优化，支持多种常见工业组件的检测。

## 功能特性

- ✅ 完整的数据集处理流程
- ✅ 支持多种标注格式转换（XML、JSON）
- ✅ 自动数据集分割（训练集/验证集/测试集）
- ✅ YOLOv11模型训练
- ✅ 多种预测模式（图片/视频/摄像头/批量）
- ✅ 支持GPU和CPU训练
- ✅ 完整的配置文件和参数调优

## 支持的类别

项目支持17个工业组件类别的检测：

- button (按钮)
- boardback (背板)
- box-battery-g (绿色电池盒)
- box-battery-w (白色电池盒)
- box-dispanel (显示面板盒)
- box-screen (屏幕盒)
- box-screen2 (屏幕盒2)
- screen (屏幕)
- burner (烧炉)
- burner-inside (烧炉内槽)
- pcb (电路板)
- dispanel (显示面板)
- boardback-f (完整背板)
- cover (后盖)
- cover-e (空后盖)
- metalpallet (金属托盘)
- metalpallet-inside (金属托盘内部)

## 快速开始

### 环境要求

- Python 3.8+
- PyTorch 2.0+
- CUDA 11.0+ (用于GPU加速)

### 安装依赖

```bash
pip install -r requirements.txt
```

### 数据集准备

1. 准备标注数据（支持XML和JSON格式）
2. 运行数据转换脚本：

```bash
python convert_to_yolo.py
```

3. 分割数据集：

```bash
python split_dataset.py
```

### 模型训练

```bash
python train.py
```

训练参数可以在 `train.py` 中调整。

### 模型预测

```bash
# 单张图片预测
python predict.py --source test.jpg

# 视频预测
python predict.py --source test.mp4 --output result.mp4

# 摄像头实时预测
python predict.py --source webcam

# 批量预测
python predict.py --source ./images/ --output ./results/
```

## 项目结构

```
.
├── README.md                    # 项目说明
├── LICENSE                      # 开源许可证
├── requirements.txt             # 依赖包列表
├── .gitignore                   # Git忽略文件
├── data.yaml                    # 数据集配置
├── classes.txt                  # 类别名称
├── train.py                     # 训练脚本
├── predict.py                   # 预测脚本
├── predict_simple.py            # 简单预测示例
├── convert_to_yolo.py           # 数据转换脚本
├── split_dataset.py             # 数据集分割脚本
├── yolo_dataset_split/         # 分割后的数据集
│   ├── train/                   # 训练集
│   ├── val/                     # 验证集
│   └── test/                    # 测试集
└── best.pt                      # 训练好的模型
```

## 模型性能

- **模型**: YOLOv11n
- **输入尺寸**: 640x640
- **训练集**: 4,694张图片
- **验证集**: 1,006张图片
- **测试集**: 1,006张图片
- **类别数**: 17个

## 训练参数

- Epochs: 100
- Batch size: 16
- Learning rate: 自动调整
- Optimizer: AdamW
- Image augmentation: Mosaic, Mixup等

## 使用示例

### 1. 数据转换

将XML或JSON格式的标注转换为YOLO格式：

```bash
python convert_to_yolo.py
```

### 2. 自定义数据集分割

修改 `split_dataset.py` 中的比例参数：

```python
split_dataset(input_dir, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)
```

### 3. 调整训练参数

编辑 `train.py` 中的训练参数：

```python
model.train(
    data=str(DATA_YAML),
    epochs=100,              # 训练轮数
    imgsz=640,               # 输入图像尺寸
    batch=16,                # 批次大小
    device="auto",           # 自动选择设备
    # ... 其他参数
)
```

### 4. 模型评估

在测试集上评估模型性能：

```bash
yolo val model=best.pt data=data.yaml split=test
``` 

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) - YOLO实现
- [PyTorch](https://pytorch.org/) - 深度学习框架

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送 Pull Request
- 邮件联系: [1984930808@qq.com]

## 更新日志

### v1.0.0 (2026-09-20)
- 初始版本发布
- 支持17个类别的目标检测
- 完整的训练和预测流程
- 支持多种输入源

## 常见问题

**Q: 如何使用自己的数据集？**

A: 准备好标注数据后，修改 `classes.txt` 中的类别名称，然后运行 `convert_to_yolo.py` 和 `split_dataset.py`。

**Q: 训练需要多长时间？**

A: 取决于硬件配置和数据集大小。使用GPU训练，约1-2小时可完成100个epoch。

**Q: 如何提高检测精度？**

A: 可以尝试增加训练数据、调整模型参数、使用更大的模型（如YOLOv11s）等。

**Q: 支持哪些输入格式？**

A: 支持常见图片格式（JPG、PNG等）和视频格式（MP4、AVI、MKV等）。