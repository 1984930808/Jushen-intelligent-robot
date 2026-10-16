#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO模型预测脚本
支持图片、视频、摄像头等多种输入源
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import cv2
from ultralytics import YOLO

# OpenCV 内部窗口名必须是 ASCII；中文标题在 Windows 上通过 Win32 API 设置
_WINDOW_HANDLES: dict[str, tuple[str, int | None]] = {}


def imshow_cn(title: str, img) -> None:
    """显示图像，窗口标题支持中文。"""
    cached = _WINDOW_HANDLES.get(title)
    if cached is None:
        internal = f"cv_win_{len(_WINDOW_HANDLES)}"
        cv2.namedWindow(internal, cv2.WINDOW_NORMAL)
        cv2.imshow(internal, img)
        hwnd = None
        if sys.platform == "win32":
            import ctypes

            hwnd = ctypes.windll.user32.FindWindowW(None, internal)
            if hwnd:
                ctypes.windll.user32.SetWindowTextW(hwnd, title)
        else:
            try:
                cv2.setWindowTitle(internal, title)
            except cv2.error:
                pass
        _WINDOW_HANDLES[title] = (internal, hwnd)
        return

    internal, hwnd = cached
    cv2.imshow(internal, img)
    if hwnd:
        import ctypes

        ctypes.windll.user32.SetWindowTextW(hwnd, title)


class Tee:
    """同时写入命令行和日志文件。"""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()

    def isatty(self):
        return False


def setup_log_file(log_path: str | None) -> tuple[object | None, Path | None]:
    """把 stdout 同时保存到日志文件。传 none 则不保存。"""
    if log_path and log_path.lower() == "none":
        return None, None

    if not log_path:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = str(Path("logs") / f"predict_{stamp}.log")

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    log_file = open(path, "a", encoding="utf-8")
    sys.stdout = Tee(sys.__stdout__, log_file)
    print(f"命令行日志已保存到: {path}")
    return log_file, path


def print_frame_time(frame_num: int, total_time: int) -> None:
    print(
        "Current Frame:"
        + str(frame_num)
        + ",total cost time:"
        + str(total_time)
        + " ms,average time:"
        + str(total_time / frame_num)
        + " ms"
    )

def predict_on_image(model_path: str, image_path: str, output_path: str = None, conf: float = 0.25, iou: float = 0.7):
    """
    对单张图片进行预测
    
    Args:
        model_path: 模型路径
        image_path: 图片路径
        output_path: 输出图片路径（可选）
        conf: 置信度阈值
        iou: IOU阈值
    """
    # 加载模型
    model = YOLO(model_path)

    frame_num = 0
    total_time = 0

    curtime = int(time.time() * 1000)
    results = model(image_path, conf=conf, iou=iou, verbose=False)
    curtime2 = int(time.time() * 1000)
    timecost = curtime2 - curtime
    frame_num += 1
    total_time += timecost
    print_frame_time(frame_num, total_time)
    
    # 显示结果
    for result in results:
        result.show()  # 显示结果
        
        # 如果指定了输出路径，保存结果
        if output_path:
            result.save(output_path)
            print(f"结果已保存到: {output_path}")
    
    # 打印检测到的物体信息
    for result in results:
        print(f"检测到 {len(result)} 个物体")
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            confidence = float(box.conf[0])
            print(f"  {class_name}: {confidence:.2f}")

def predict_on_video(model_path: str, video_path: str, output_path: str = None, conf: float = 0.25, iou: float = 0.7):
    """
    对视频进行预测
    
    Args:
        model_path: 模型路径
        video_path: 视频路径
        output_path: 输出视频路径（可选）
        conf: 置信度阈值
        iou: IOU阈值
    """
    # 加载模型
    model = YOLO(model_path)
    
    # 打开视频
    cap = cv2.VideoCapture(video_path)
    
    # 获取视频信息
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 如果指定了输出路径，创建视频写入器
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # 逐帧处理
    frame_num = 0
    total_time = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        curtime = int(time.time() * 1000)
        results = model(frame, conf=conf, iou=iou, verbose=False)
        curtime2 = int(time.time() * 1000)
        timecost = curtime2 - curtime
        frame_num += 1
        total_time += timecost
        print_frame_time(frame_num, total_time)

        result = results[0]
        print(f"检测到 {len(result)} 个物体")
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            confidence = float(box.conf[0])
            print(f"  {class_name}: {confidence:.2f}")
        
        # 在帧上绘制结果
        annotated_frame = result.plot()
        
        # 显示结果
        imshow_cn('YOLO Prediction', annotated_frame)
        
        # 如果指定了输出路径，保存帧
        if output_path:
            out.write(annotated_frame)
        
        # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 释放资源
    cap.release()
    if output_path:
        out.release()
    cv2.destroyAllWindows()
    
    if output_path:
        print(f"结果已保存到: {output_path}")

def predict_on_webcam(model_path: str, conf: float = 0.25, iou: float = 0.7):
    """
    对摄像头进行实时预测
    
    Args:
        model_path: 模型路径
        conf: 置信度阈值
        iou: IOU阈值
    """
    # 加载模型
    model = YOLO(model_path)
    
    # 打开摄像头
    cap = cv2.VideoCapture(0)  # 0表示默认摄像头
    
    print("按'q'退出摄像头预测")

    frame_num = 0
    total_time = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        curtime = int(time.time() * 1000)
        results = model(frame, conf=conf, iou=iou, verbose=False)
        curtime2 = int(time.time() * 1000)
        timecost = curtime2 - curtime
        frame_num += 1
        total_time += timecost
        print_frame_time(frame_num, total_time)

        result = results[0]
        print(f"检测到 {len(result)} 个物体")
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            confidence = float(box.conf[0])
            print(f"  {class_name}: {confidence:.2f}")
        
        # 在帧上绘制结果
        annotated_frame = result.plot()
        
        # 显示结果
        imshow_cn('具身智能视觉识别系统', annotated_frame)
        
        # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

def predict_on_directory(model_path: str, directory_path: str, output_dir: str = None, conf: float = 0.25, iou: float = 0.7):
    """
    对目录中的所有图片进行批量预测
    
    Args:
        model_path: 模型路径
        directory_path: 图片目录路径
        output_dir: 输出目录（可选）
        conf: 置信度阈值
        iou: IOU阈值
    """
    from pathlib import Path
    
    # 加载模型
    model = YOLO(model_path)
    
    # 获取目录中的所有图片
    directory = Path(directory_path)
    image_files = list(directory.glob('*.jpg')) + list(directory.glob('*.png')) + list(directory.glob('*.jpeg'))
    
    print(f"找到 {len(image_files)} 张图片")
    
    # 创建输出目录
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    
    # 逐张处理
    frame_num = 0
    total_time = 0
    for i, image_file in enumerate(image_files):
        print(f"处理 {i+1}/{len(image_files)}: {image_file.name}")
        
        curtime = int(time.time() * 1000)
        results = model(str(image_file), conf=conf, iou=iou, verbose=False)
        curtime2 = int(time.time() * 1000)
        timecost = curtime2 - curtime
        frame_num += 1
        total_time += timecost
        print_frame_time(frame_num, total_time)

        result = results[0]
        print(f"检测到 {len(result)} 个物体")
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            confidence = float(box.conf[0])
            print(f"  {class_name}: {confidence:.2f}")
        
        # 如果指定了输出目录，保存结果
        if output_dir:
            output_file = output_path / f"result_{image_file.name}"
            result.save(str(output_file))

def main():
    parser = argparse.ArgumentParser(description='YOLO模型预测脚本')
    parser.add_argument('--model', type=str, default='best.pt', help='模型路径')
    parser.add_argument('--source', type=str, required=True, help='输入源（图片/视频/目录路径或webcam）')
    parser.add_argument('--output', type=str, help='输出路径（可选）')
    parser.add_argument('--conf', type=float, default=0.25, help='置信度阈值')
    parser.add_argument('--iou', type=float, default=0.7, help='IOU阈值')
    parser.add_argument(
        '--log',
        type=str,
        default='',
        help='日志文件路径，默认 logs/predict_时间戳.log；传 none 不保存文件',
    )

    args = parser.parse_args()
    log_file, log_path = setup_log_file(args.log)

    try:
        run_prediction(args)
    finally:
        if log_file is not None:
            print(f"命令行日志已保存到: {log_path}")
            sys.stdout = sys.__stdout__
            log_file.close()


def run_prediction(args) -> None:
    # 判断输入源类型
    source = args.source.lower()
    
    if source == 'webcam':
        print("启动摄像头预测...")
        predict_on_webcam(args.model, args.conf, args.iou)
    elif Path(args.source).is_file():
        # 判断是图片还是视频
        file_ext = Path(args.source).suffix.lower()
        if file_ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            print(f"对图片进行预测: {args.source}")
            predict_on_image(args.model, args.source, args.output, args.conf, args.iou)
        elif file_ext in ['.mp4', '.avi', '.mkv', '.mov']:
            print(f"对视频进行预测: {args.source}")
            predict_on_video(args.model, args.source, args.output, args.conf, args.iou)
        else:
            print(f"不支持的文件格式: {file_ext}")
    elif Path(args.source).is_dir():
        print(f"对目录进行批量预测: {args.source}")
        predict_on_directory(args.model, args.source, args.output, args.conf, args.iou)
    else:
        print(f"输入源不存在: {args.source}")

if __name__ == "__main__":
    main()