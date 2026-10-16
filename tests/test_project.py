#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基础可复现测试：配置、数据集声明、模型与 Demo 推理。"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist():
    required = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "requirements.txt",
        "data.yaml",
        "classes.txt",
        "best.pt",
        "predict.py",
        "train.py",
        "run_demo.py",
        "verify_dataset.py",
        "demo/sample.png",
        "docs/README.md",
    ]
    missing = [name for name in required if not (ROOT / name).exists()]
    assert not missing, f"缺少必要文件: {missing}"


def test_classes_align_with_data_yaml():
    names = [
        line.strip()
        for line in (ROOT / "classes.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    with (ROOT / "data.yaml").open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    assert data["nc"] == len(names)
    assert list(data["names"]) == names
    assert len(names) == 17


def test_data_yaml_uses_relative_path():
    with (ROOT / "data.yaml").open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    path = Path(data["path"])
    assert not path.is_absolute(), "data.yaml 的 path 必须是相对路径，便于异地复现"


def test_config_reference_metrics():
    from config import NUM_CLASSES, REFERENCE_METRICS

    assert NUM_CLASSES == 17
    assert REFERENCE_METRICS["mAP50"] >= 0.99
    assert REFERENCE_METRICS["mAP50_95"] >= 0.90


def test_model_loads():
    from ultralytics import YOLO

    model = YOLO(str(ROOT / "best.pt"))
    assert model is not None


def test_demo_inference_smoke():
    from ultralytics import YOLO

    source = ROOT / "demo" / "sample.png"
    assert source.exists()
    model = YOLO(str(ROOT / "best.pt"))
    results = model(str(source), conf=0.25, verbose=False)
    assert len(results) == 1
    # 样例图应能检出至少一个目标
    assert len(results[0].boxes) >= 1


def test_verify_dataset_script_importable():
    import verify_dataset

    assert hasattr(verify_dataset, "verify")


@pytest.mark.skipif(
    not (ROOT / "dataset" / "train" / "images").exists(),
    reason="本地未准备 dataset/，跳过完整数据集校验",
)
def test_verify_dataset_passes_when_present():
    import verify_dataset

    assert verify_dataset.verify() == 0
