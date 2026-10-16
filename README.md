# YOLO 工业目标检测开源包

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![YOLO](https://img.shields.io/badge/YOLO-v11-orange.svg)](https://github.com/ultralytics/ultralytics)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)

基于 **YOLOv11** 的工业组件目标检测开源实现，支持 17 类目标的训练、评估与推理，并提供可异地复现的 Demo 与测试脚本。

## 项目简介

本项目面向工业视觉场景，提供从数据准备、模型训练到图片/视频/摄像头推理的完整工具链。仓库内置训练好的权重 `best.pt` 与样例图 `demo/sample.png`，开源用户无需先下载大数据集即可验证推理效果。

## 算法原理

采用 Ultralytics YOLOv11n 单阶段检测器：

1. Backbone 提取多尺度特征  
2. Neck 融合语义与细节  
3. Detect Head 输出类别、置信度与边界框，经 NMS 得到最终结果  

相较两阶段方法，更适合产线实时检测。详细说明见 [docs/algorithm.md](docs/algorithm.md)。

## 应用场景

- 工业装配线视觉质检  
- 仓储托盘部件识别与盘点  
- 工位监控与目标统计  
- 为下游机器人抓取提供视觉检测输入  

> **范围说明**：本开源包聚焦**视觉识别**。机械臂运动规划、轨迹控制及“规划成功率”不在本仓库范围内；检测结果可作为外部规划系统的输入。

## 性能指标（验证集）

模型：YOLOv11n | 输入：640×640 | 权重：`best.pt`

| 指标 | 数值 |
|------|------|
| **识别 mAP@0.5** | **0.994** |
| **识别 mAP@0.5:0.95** | **0.935** |
| Precision | 0.992 |
| Recall | 0.993 |
| 机械臂规划成功率 | 不适用（本包不含机械臂规划模块） |

指标曲线见 [`docs/assets/`](docs/assets/)。异地复现允许 ±0.02 容差，可用：

```bash
python reproduce.py --eval
```

## 数据集

完整训练/评估数据（约 7022 张）：

- 网盘：https://pan.baidu.com/s/1bTLMJsUC7hQVHTSQraW0ZQ  
- 提取码：`4kgy`  
- 解压后目录应为：`dataset/train|val|test/{images,labels}`

| 子集 | 图片数 |
|------|--------|
| train | 4915 |
| val | 1053 |
| test | 1054 |

> 仅跑 Demo / 单元测试时，**不必**下载完整数据集。

## 支持的类别（17）

button, boardback, box-battery-g, box-battery-w, box-dispanel, box-screen, box-screen2, screen, burner, burner-inside, pcb, dispanel, boardback-f, cover, cover-e, metalpallet, metalpallet-inside

## 环境安装

- Python 3.8+  
- PyTorch 2.0+  
- 可选：CUDA 11.0+  

```bash
pip install -r requirements.txt
```

更多说明：[docs/install.md](docs/install.md)

## 快速运行 Demo

```bash
# 1) 安装依赖
pip install -r requirements.txt

# 2) 运行官方 Demo（使用 demo/sample.png）
python run_demo.py

# 3) 运行测试
python -m pytest tests -q

# 4) 一键复现（推荐）
python reproduce.py
```

预测示例：

```bash
python predict.py --source demo/sample.png --output runs/pred.jpg
python predict.py --source your.mp4 --output runs/pred.mp4
python predict.py --source webcam
```

## 训练与评估

```bash
# 准备 dataset/ 后校验
python verify_dataset.py

# 训练
python train.py

# 评估
yolo val model=best.pt data=data.yaml split=val
# 或
python reproduce.py --eval
```

## 项目结构

```text
.
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── requirements.txt
├── data.yaml                 # 相对路径数据集配置
├── classes.txt
├── best.pt                   # 发布权重
├── config.py
├── train.py
├── predict.py
├── predict_simple.py
├── run_demo.py               # 快速 Demo
├── verify_dataset.py         # 数据集校验
├── reproduce.py              # 异地一键复现
├── convert_to_yolo.py
├── split_dataset.py
├── demo/
│   └── sample.png            # 官方样例图
├── docs/                     # 技术文档
│   ├── README.md
│   ├── algorithm.md
│   ├── install.md
│   ├── usage.md
│   ├── dataset.md
│   ├── evaluation.md
│   ├── api.md
│   └── assets/               # 指标曲线图
├── tests/                    # 自动化测试
└── dataset/                  # 完整数据（需自行下载）
```

## 功能特性

- 完整数据集处理流程（XML/JSON → YOLO）  
- 自动划分 train/val/test  
- YOLOv11 训练与评估  
- 图片 / 视频 / 摄像头 / 批量预测  
- GPU / CPU 推理  
- Demo、数据集校验、一键复现与单元测试  

## 引用方式

若本项目对你的研究或产品有帮助，请按如下方式引用：

```bibtex
@software{zsf_yolo_detection_2026,
  title  = {YOLO Industrial Object Detection},
  author = {ZSF Project Authors},
  year   = {2026},
  note   = {MIT License},
  url    = {https://github.com/your-org/zsf}
}
```

## 开源许可声明

本项目采用 **MIT License** 开源。完整许可证文本见根目录 [LICENSE](LICENSE)。

你可自由使用、复制、修改、合并、发布、分发及商业使用本软件，但须保留版权与许可声明；软件按“现状”提供，不附带明示或暗示担保。

## 贡献

欢迎提交 Issue / PR。请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 技术文档

完整文档入口：[docs/README.md](docs/README.md)

## 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)。

## 常见问题

见 [FAQ.md](FAQ.md) 与 README 下文。

**Q: 没有完整数据集能否跑通？**  
A: 可以。`python run_demo.py` 与 `pytest` 仅依赖 `best.pt` 与 `demo/sample.png`。

**Q: 如何核对 README 指标？**  
A: 准备好 `dataset/` 后执行 `python reproduce.py --eval`。

**Q: 为什么没有机械臂规划成功率？**  
A: 本仓库只开源视觉检测；规划模块需对接外部机械臂系统单独评估。

## 联系方式

- 提交 Issue / Pull Request  
- 邮件：1984930808@qq.com  

## 致谢

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)  
- [PyTorch](https://pytorch.org/)  
