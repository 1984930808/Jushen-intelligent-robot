#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目配置文件
"""

from pathlib import Path

# 项目根目录
ROOT = Path(__file__).resolve().parent

# 数据集配置（与 data.yaml 保持一致）
DATASET_DIR = ROOT / "dataset"
DATA_YAML = ROOT / "data.yaml"
CLASSES_FILE = ROOT / "classes.txt"

# 模型配置
MODEL_PATH = ROOT / "best.pt"
PRETRAINED_MODEL = "yolo11n.pt"
DEMO_IMAGE = ROOT / "demo" / "sample.png"

# 训练配置
TRAIN_CONFIG = {
    "epochs": 100,
    "imgsz": 640,
    "batch": 16,
    "device": "auto",
    "workers": 8,
    "patience": 50,
    "optimizer": "auto",
    "lr0": 0.01,
}

# 预测配置
PREDICT_CONFIG = {
    "conf": 0.25,
    "iou": 0.7,
    "max_det": 300,
}

# 已发布模型在验证集上的参考指标（见 docs/evaluation.md）
REFERENCE_METRICS = {
    "mAP50": 0.994,
    "mAP50_95": 0.935,
    "precision": 0.992,
    "recall": 0.993,
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
        "demo_image": str(DEMO_IMAGE),
        "train_config": TRAIN_CONFIG,
        "predict_config": PREDICT_CONFIG,
        "reference_metrics": REFERENCE_METRICS,
        "output_dir": str(OUTPUT_DIR),
        "num_classes": NUM_CLASSES,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(get_config(), indent=2, ensure_ascii=False))
