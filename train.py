"""YOLOv11 训练入口脚本。"""

from __future__ import annotations

from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
DATA_YAML = ROOT / "data.yaml"
DEFAULT_WEIGHTS = ROOT / "best.pt"


def main() -> None:
    if not DATA_YAML.exists():
        raise FileNotFoundError(f"未找到 {DATA_YAML}，请确认仓库文件完整")

    dataset_images = ROOT / "dataset" / "train" / "images"
    if not dataset_images.exists():
        raise FileNotFoundError(
            f"未找到训练集: {dataset_images}\n请先按 README 下载并解压数据集到 dataset/"
        )

    if DEFAULT_WEIGHTS.exists():
        model_path = str(DEFAULT_WEIGHTS)
        print(f"使用已有权重继续/微调: {model_path}")
    else:
        model_path = "yolo11n.pt"
        print("未找到 best.pt，将使用官方预训练模型 yolo11n.pt")

    model = YOLO(model_path)
    model.train(
        data=str(DATA_YAML),
        epochs=100,
        patience=30,
        imgsz=640,
        batch=16,
        amp=True,
        device="auto",
        workers=4,
        project=str(ROOT / "runs" / "detect"),
        name="yolo11_train",
        resume=False,
        pretrained=True,
        optimizer="auto",
        save=True,
        save_period=-1,
        plots=True,
        val=True,
        cache=False,
        seed=42,
        verbose=True,
        hsv_h=0.005,
        hsv_s=0.5,
        hsv_v=0.3,
        degrees=0.0,
        translate=0.1,
        scale=0.25,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        close_mosaic=50,
        mixup=0.0,
        erasing=0.4,
        box=6.0,
        cls=0.75,
    )


if __name__ == "__main__":
    main()
