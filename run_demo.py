#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速 Demo：使用仓库自带模型与样例图做一次推理。

用法:
  python run_demo.py
  python run_demo.py --source demo/sample.png --output runs/demo_result.jpg
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL = ROOT / "best.pt"
DEFAULT_SOURCE = ROOT / "demo" / "sample.png"
DEFAULT_OUTPUT = ROOT / "runs" / "demo_result.jpg"


def main() -> int:
    parser = argparse.ArgumentParser(description="YOLOv11 工业检测快速 Demo")
    parser.add_argument("--model", default=str(DEFAULT_MODEL), help="模型权重路径")
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="输入图片路径")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="输出图片路径")
    parser.add_argument("--conf", type=float, default=0.25, help="置信度阈值")
    parser.add_argument("--iou", type=float, default=0.7, help="NMS IoU 阈值")
    args = parser.parse_args()

    model_path = Path(args.model)
    source = Path(args.source)
    output = Path(args.output)

    if not model_path.exists():
        raise FileNotFoundError(f"未找到模型: {model_path}")
    if not source.exists():
        raise FileNotFoundError(f"未找到输入图片: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)
    model = YOLO(str(model_path))
    results = model(str(source), conf=args.conf, iou=args.iou, verbose=False)

    total = 0
    for result in results:
        result.save(str(output))
        total += len(result.boxes)
        print(f"检测到 {len(result.boxes)} 个目标:")
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            confidence = float(box.conf[0])
            print(f"  - {class_name}: {confidence:.3f}")

    print(f"结果已保存: {output}")
    print(f"Demo 完成，共检测 {total} 个目标")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
