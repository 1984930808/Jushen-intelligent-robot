# 常见问题 (FAQ)

## 安装和环境

### Q: 如何安装项目依赖？

```bash
pip install -r requirements.txt
```

### Q: 支持哪些 Python 版本？

A: Python 3.8+，推荐 3.10。

### Q: 需要 GPU 吗？

A: 不强制。CPU 可跑 Demo 与推理；训练建议使用 GPU。

## 复现相关

### Q: 从零如何完整复现？

```bash
pip install -r requirements.txt
python run_demo.py
python -m pytest tests -q
python reproduce.py
```

有完整数据集时再执行：

```bash
python verify_dataset.py
python reproduce.py --eval
```

### Q: 为什么指标和 README 有微小差异？

A: 允许 ±0.02 容差，常见原因是 PyTorch/CUDA/驱动小版本差异。

### Q: 机械臂规划成功率在哪里？

A: 本仓库只包含视觉检测，不包含机械臂规划，因此不提供该指标。

## 数据集

### Q: 如何使用自己的数据集？

1. 准备图片与标注  
2. 修改 `classes.txt`  
3. 运行 `python convert_to_yolo.py`  
4. 运行 `python split_dataset.py`  
5. 同步更新 `data.yaml`  

### Q: 支持哪些标注格式？

- XML（Pascal VOC）  
- JSON（LabelMe）  

## 训练与预测

### Q: 如何提高检测精度？

- 增加高质量标注数据  
- 调整增强与学习率  
- 尝试更大模型（YOLOv11s/m）  

### Q: 如何调整检测灵敏度？

```bash
python predict.py --source demo/sample.png --conf 0.3
```

## 引用

```bibtex
@software{zsf_yolo_detection_2026,
  title  = {YOLO Industrial Object Detection},
  author = {ZSF Project Authors},
  year   = {2026},
  note   = {MIT License},
  url    = {https://github.com/your-org/zsf}
}
```

## 商业使用

本项目采用 MIT 许可证，可自由用于商业用途，需保留许可声明。

## 联系

- Issue  
- 邮件：1984930808@qq.com  
