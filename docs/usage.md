# 使用说明

## 1. 快速 Demo（推荐先跑）

```bash
python run_demo.py
# 等价
python predict_simple.py
```

默认读取：

- 模型：`best.pt`  
- 输入：`demo/sample.png`  
- 输出：`runs/demo_result.jpg`  

## 2. 通用预测

```bash
# 单张图片
python predict.py --source demo/sample.png --output runs/pred.jpg

# 视频
python predict.py --source your.mp4 --output runs/pred.mp4

# 摄像头
python predict.py --source webcam

# 批量目录
python predict.py --source ./images/ --output ./results/
```

常用参数：

- `--conf`：置信度阈值（默认 0.25）  
- `--iou`：NMS IoU 阈值（默认 0.7）  

## 3. 训练

```bash
# 确认 dataset/ 已就绪
python verify_dataset.py
python train.py
```

训练参数可在 `train.py` 中调整。

## 4. 评估

```bash
# Ultralytics CLI
yolo val model=best.pt data=data.yaml split=val

# 或一键复现（含指标核对）
python reproduce.py --eval
```

## 5. 数据准备（自定义数据）

```bash
python convert_to_yolo.py
python split_dataset.py
```

详见 [dataset.md](dataset.md)。
