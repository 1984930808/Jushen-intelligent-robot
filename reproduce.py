#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异地可复现一键脚本：
1) 检查依赖导入
2) 校验数据集配置（数据集可选，缺失时跳过并提示）
3) 运行 Demo 推理
4) 运行单元测试
5) （可选）在验证集上评估并与 README 参考指标对比

用法:
  python reproduce.py
  python reproduce.py --eval
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REFERENCE = {
    "mAP50": 0.994,
    "mAP50_95": 0.935,
    "tolerance": 0.02,
}


def run_step(title: str, cmd: list[str], required: bool = True) -> bool:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(">", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(ROOT))
    if result.returncode != 0:
        if required:
            print(f"[失败] {title}")
            return False
        print(f"[跳过/警告] {title}")
        return True
    print(f"[通过] {title}")
    return True


def check_imports() -> bool:
    print("\n" + "=" * 60)
    print("步骤1: 检查关键依赖")
    print("=" * 60)
    try:
        import cv2  # noqa: F401
        import numpy  # noqa: F401
        import torch  # noqa: F401
        import ultralytics  # noqa: F401
        import yaml  # noqa: F401

        print(f"torch={torch.__version__}")
        print(f"ultralytics={ultralytics.__version__}")
        print("[通过] 依赖导入")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[失败] 依赖导入: {exc}")
        return False


def maybe_eval() -> bool:
    print("\n" + "=" * 60)
    print("步骤5: 验证集评估（与 README 指标对比）")
    print("=" * 60)
    data_yaml = ROOT / "data.yaml"
    model = ROOT / "best.pt"
    dataset = ROOT / "dataset" / "val" / "images"
    if not dataset.exists():
        print("未找到验证集，跳过评估。请先按 README 准备 dataset/")
        return True

    from ultralytics import YOLO

    yolo = YOLO(str(model))
    metrics = yolo.val(data=str(data_yaml), split="val", plots=False, verbose=False)
    box = metrics.box
    map50 = float(box.map50)
    map5095 = float(box.map)
    precision = float(box.mp)
    recall = float(box.mr)

    print(f"实测 mAP50     = {map50:.4f}  (参考 {REFERENCE['mAP50']:.3f})")
    print(f"实测 mAP50-95  = {map5095:.4f}  (参考 {REFERENCE['mAP50_95']:.3f})")
    print(f"实测 Precision = {precision:.4f}")
    print(f"实测 Recall    = {recall:.4f}")

    tol = REFERENCE["tolerance"]
    ok = (
        abs(map50 - REFERENCE["mAP50"]) <= tol
        and abs(map5095 - REFERENCE["mAP50_95"]) <= tol
    )
    if ok:
        print("[通过] 指标与 README 参考值一致（容差内）")
        return True
    print("[失败] 指标偏离 README 参考值过大")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="异地可复现验证脚本")
    parser.add_argument(
        "--eval",
        action="store_true",
        help="额外在验证集上评估并核对 README 指标（耗时更长）",
    )
    args = parser.parse_args()

    if not check_imports():
        return 1

    # 数据集校验：有数据则必须通过；无数据则警告继续（Demo 仍可用）
    dataset_ok = (ROOT / "dataset" / "train" / "images").exists()
    if not run_step(
        "步骤2: 校验数据集",
        [sys.executable, str(ROOT / "verify_dataset.py")],
        required=dataset_ok,
    ):
        return 1

    if not run_step(
        "步骤3: 运行 Demo",
        [sys.executable, str(ROOT / "run_demo.py")],
        required=True,
    ):
        return 1

    if not run_step(
        "步骤4: 运行测试",
        [sys.executable, "-m", "pytest", "tests", "-q"],
        required=True,
    ):
        return 1

    if args.eval and not maybe_eval():
        return 1

    print("\n" + "=" * 60)
    print("复现流程完成")
    if not args.eval:
        print("提示: 若需核对性能指标，请执行: python reproduce.py --eval")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
