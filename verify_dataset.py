#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验数据集目录结构、类别配置与图片/标注数量。"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
DATA_YAML = ROOT / "data.yaml"
CLASSES_FILE = ROOT / "classes.txt"
REQUIRED_SPLITS = ("train", "val", "test")


def load_names() -> list[str]:
    if not CLASSES_FILE.exists():
        raise FileNotFoundError(f"缺少类别文件: {CLASSES_FILE}")
    names = [line.strip() for line in CLASSES_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not names:
        raise ValueError("classes.txt 为空")
    return names


def load_data_yaml() -> dict:
    if not DATA_YAML.exists():
        raise FileNotFoundError(f"缺少数据配置: {DATA_YAML}")
    with DATA_YAML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("data.yaml 格式无效")
    return data


def count_images(split_dir: Path) -> int:
    images_dir = split_dir / "images"
    if not images_dir.exists():
        return 0
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    return sum(1 for p in images_dir.iterdir() if p.suffix.lower() in exts and p.is_file())


def count_labels(split_dir: Path) -> int:
    labels_dir = split_dir / "labels"
    if not labels_dir.exists():
        return 0
    return sum(1 for p in labels_dir.iterdir() if p.suffix.lower() == ".txt" and p.is_file())


def verify() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    names = load_names()
    data = load_data_yaml()

    nc = int(data.get("nc", 0))
    yaml_names = list(data.get("names") or [])
    if nc != len(names):
        errors.append(f"classes.txt 类别数={len(names)}，与 data.yaml nc={nc} 不一致")
    if yaml_names and yaml_names != names:
        errors.append("data.yaml names 与 classes.txt 不一致")

    dataset_path = Path(data.get("path", "dataset"))
    if not dataset_path.is_absolute():
        dataset_path = ROOT / dataset_path

    if not dataset_path.exists():
        errors.append(
            f"数据集目录不存在: {dataset_path}\n"
            "请按 README 下载并解压 dataset，或将数据放到项目根目录 dataset/"
        )
        _print_report(names, {}, errors, warnings)
        return 1

    split_stats: dict[str, dict[str, int]] = {}
    for split in REQUIRED_SPLITS:
        split_dir = dataset_path / split
        img_n = count_images(split_dir)
        lbl_n = count_labels(split_dir)
        split_stats[split] = {"images": img_n, "labels": lbl_n}
        if img_n == 0:
            errors.append(f"{split} 集无图片: {split_dir / 'images'}")
        if lbl_n == 0:
            warnings.append(f"{split} 集无标注: {split_dir / 'labels'}")
        if img_n and lbl_n and abs(img_n - lbl_n) > max(10, int(img_n * 0.05)):
            warnings.append(f"{split} 集图片数({img_n})与标注数({lbl_n})差异较大")

    _print_report(names, split_stats, errors, warnings)
    return 1 if errors else 0


def _print_report(
    names: list[str],
    split_stats: dict[str, dict[str, int]],
    errors: list[str],
    warnings: list[str],
) -> None:
    print("=" * 60)
    print("数据集校验报告")
    print("=" * 60)
    print(f"类别数: {len(names)}")
    print(f"类别: {', '.join(names)}")
    if split_stats:
        print("-" * 60)
        for split, stats in split_stats.items():
            print(f"{split:5s}  images={stats['images']:<6d} labels={stats['labels']}")
    if warnings:
        print("-" * 60)
        print("警告:")
        for item in warnings:
            print(f"  - {item}")
    if errors:
        print("-" * 60)
        print("错误:")
        for item in errors:
            print(f"  - {item}")
        print("校验失败")
    else:
        print("-" * 60)
        print("校验通过")


if __name__ == "__main__":
    sys.exit(verify())
