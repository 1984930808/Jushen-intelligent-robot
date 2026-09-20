#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YOLO模型预测脚本
支持图片、视频、摄像头等多种输入源
"""

from __future__ import annotations

import cv2
from pathlib import Path
from ultralytics import YOLO
import argparse

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
    
    # 进行预测
    results = model(image_path, conf=conf, iou=iou)
    
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
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        if frame_count % 10 == 0:  # 每10帧打印一次进度
            print(f"处理第 {frame_count} 帧...")
        
        # 进行预测
        results = model(frame, conf=conf, iou=iou)
        
        # 在帧上绘制结果
        annotated_frame = results[0].plot()
        
        # 显示结果
        cv2.imshow('YOLO Prediction', annotated_frame)
        
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
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 进行预测
        results = model(frame, conf=conf, iou=iou)
        
        # 在帧上绘制结果
        annotated_frame = results[0].plot()
        
        # 显示结果
        cv2.imshow('YOLO Webcam Prediction', annotated_frame)
        
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
    for i, image_file in enumerate(image_files):
        print(f"处理 {i+1}/{len(image_files)}: {image_file.name}")
        
        # 进行预测
        results = model(str(image_file), conf=conf, iou=iou)
        
        # 如果指定了输出目录，保存结果
        if output_dir:
            output_file = output_path / f"result_{image_file.name}"
            results[0].save(str(output_file))

def main():
    parser = argparse.ArgumentParser(description='YOLO模型预测脚本')
    parser.add_argument('--model', type=str, default='best.pt', help='模型路径')
    parser.add_argument('--source', type=str, required=True, help='输入源（图片/视频/目录路径或webcam）')
    parser.add_argument('--output', type=str, help='输出路径（可选）')
    parser.add_argument('--conf', type=float, default=0.25, help='置信度阈值')
    parser.add_argument('--iou', type=float, default=0.7, help='IOU阈值')
    
    args = parser.parse_args()
    
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