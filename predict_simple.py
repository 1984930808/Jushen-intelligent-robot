#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 YOLO 预测示例脚本（默认使用仓库自带 demo 样例）。
"""

from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "best.pt"
IMAGE_PATH = ROOT / "demo" / "sample.png"
OUTPUT_PATH = ROOT / "runs" / "simple_result.jpg"


def main() -> None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"未找到模型: {MODEL_PATH}")
    if not IMAGE_PATH.exists():
        raise FileNotFoundError(f"未找到样例图: {IMAGE_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    model = YOLO(str(MODEL_PATH))
    results = model(str(IMAGE_PATH), conf=0.25)

    for result in results:
        result.save(str(OUTPUT_PATH))
        print(f"检测到 {len(result.boxes)} 个物体:")
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            confidence = float(box.conf[0])
            print(f"  {class_name}: {confidence:.2f}")
    print(f"结果已保存: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
