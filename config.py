#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目配置文件
"""

import os
from pathlib import Path

# 项目根目录
ROOT = Path(__file__).resolve().parent

# 数据集配置
DATASET_DIR = ROOT / "yolo_dataset_split"
DATA_YAML = ROOT / "data.yaml"
CLASSES_FILE = ROOT / "classes.txt"

# 模型配置
MODEL_PATH = ROOT / "best.pt"
PRETRAINED_MODEL = "yolo11n.pt"

# 训练配置
TRAIN_CONFIG = {
    "epochs": 100,
    "imgsz": 640,
    "batch": 16,
    "device": "auto",
    "workers": 8,
    "patience": 50,
    "optimizer": "auto",
    "lr0": 0.01,  # 初始学习率
}

# 预测配置
PREDICT_CONFIG = {
    "conf": 0.25,  # 置信度阈值
    "iou": 0.7,    # IOU阈值
    "max_det": 300,  # 每张图片最大检测数
}

# 输出配置
OUTPUT_DIR = ROOT / "runs"
TRAIN_OUTPUT = OUTPUT_DIR / "detect" / "yolo11_train"

# 类别配置
NUM_CLASSES = 17

def get_config():
    """获取完整配置"""
    return {
        "root": str(ROOT),
        "dataset_dir": str(DATASET_DIR),
        "data_yaml": str(DATA_YAML),
        "classes_file": str(CLASSES_FILE),
        "model_path": str(MODEL_PATH),
        "pretrained_model": PRETRAINED_MODEL,
        "train_config": TRAIN_CONFIG,
        "predict_config": PREDICT_CONFIG,
        "output_dir": str(OUTPUT_DIR),
        "num_classes": NUM_CLASSES,
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_config(), indent=2, ensure_ascii=False))