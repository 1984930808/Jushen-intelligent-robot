# 常见问题 (FAQ)

## 安装和环境

### Q: 如何安装项目依赖？

A: 运行以下命令安装所有依赖：

```bash
pip install -r requirements.txt
```

### Q: 支持哪些Python版本？

A: 项目支持Python 3.8及以上版本。推荐使用Python 3.10。

### Q: 需要GPU吗？

A: 不强制需要GPU，项目支持CPU训练。但GPU训练速度会快很多。

## 数据集相关

### Q: 如何使用自己的数据集？

A: 准备好标注数据后，按照以下步骤操作：

1. 将图片放在 `images/` 目录
2. 将标注文件放在 `labels/` 目录
3. 修改 `classes.txt` 中的类别名称
4. 运行 `python convert_to_yolo.py`
5. 运行 `python split_dataset.py`

### Q: 支持哪些标注格式？

A: 目前支持：
- XML格式 (Pascal VOC)
- JSON格式 (LabelMe)

### Q: 数据集需要多大的规模？

A: 建议每个类别至少100张图片。总数据集建议1000张以上。

## 训练相关

### Q: 训练需要多长时间？

A: 取决于以下因素：
- 硬件配置（GPU型号）
- 数据集大小
- 训练轮数

使用GPU训练，约1-2小时可完成100个epoch。

### Q: 如何调整训练参数？

A: 编辑 `train.py` 文件中的训练参数：

```python
model.train(
    epochs=100,      # 训练轮数
    batch=16,        # 批次大小
    imgsz=640,       # 输入尺寸
    # ... 其他参数
)
```

### Q: 如何提高检测精度？

A: 可以尝试以下方法：
- 增加训练数据
- 调整数据增强参数
- 使用更大的模型（如YOLOv11s, YOLOv11m）
- 调整学习率和训练轮数
- 优化数据集质量

### Q: 训练中断了如何继续？

A: 在 `train.py` 中设置 `resume=True`：

```python
model.train(
    resume=True,  # 从中断处继续训练
    # ... 其他参数
)
```

## 预测相关

### Q: 支持哪些输入格式？

A: 支持以下格式：
- 图片：JPG, PNG, JPEG, BMP
- 视频：MP4, AVI, MKV, MOV
- 摄像头：实时摄像头输入
- 目录：批量处理目录中的图片

### Q: 如何调整检测灵敏度？

A: 使用 `--conf` 参数调整置信度阈值：

```bash
python predict.py --source test.jpg --conf 0.3
```

较低的值会检测更多目标，但可能包含误检。

### Q: 如何保存预测结果？

A: 使用 `--output` 参数指定输出路径：

```bash
python predict.py --source test.jpg --output result.jpg
```

## 模型相关

### Q: 如何导出模型？

A: 使用Ultralytics提供的导出功能：

```python
from ultralytics import YOLO
model = YOLO('best.pt')
model.export(format='onnx')  # 导出为ONNX格式
```

### Q: 支持哪些模型格式？

A: 支持导出为：
- ONNX
- TensorRT
- CoreML
- TFLite
- 等其他格式

### Q: 如何使用预训练模型？

A: 修改 `train.py` 中的模型路径：

```python
MODEL_PATH = "yolo11n.pt"  # 使用官方预训练模型
```

## 性能优化

### Q: 如何提高推理速度？

A: 可以尝试：
- 使用更小的模型（YOLOv11n）
- 降低输入图像尺寸
- 使用GPU推理
- 导出为ONNX或TensorRT格式
- 批量处理图片

### Q: 内存不足怎么办？

A: 可以：
- 减小batch size
- 降低输入图像尺寸
- 使用更小的模型
- 关闭数据缓存

## 故障排除

### Q: 出现CUDA错误怎么办？

A: 检查以下几点：
- 确认GPU驱动已正确安装
- 检查CUDA版本是否兼容
- 在 `train.py` 中设置 `device="cpu"` 使用CPU训练

### Q: 找不到数据集文件？

A: 确认：
- 数据集路径配置正确
- `data.yaml` 文件路径正确
- 图片和标注文件对应

### Q: 训练过程中出现NaN损失？

A: 可能原因：
- 学习率过高
- 数据标注错误
- 数据预处理问题

尝试降低学习率或检查数据质量。

## 其他

### Q: 如何引用本项目？

A: 如果您在研究中使用了本项目，请引用：

```bibtex
@software{yolo_detection,
  title={YOLO目标检测项目},
  author={Your Name},
  year={2024},
  url={https://github.com/your-username/yolo-detection}
}
```

### Q: 商业使用需要授权吗？

A: 本项目采用MIT许可证，可以自由用于商业用途。

### Q: 如何联系作者？

A: 通过以下方式：
- 提交GitHub Issue
- 发送邮件至 [your-email@example.com]
- 查看项目主页获取更多信息