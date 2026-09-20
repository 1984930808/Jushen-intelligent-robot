#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将YOLO数据集分割为训练集、验证集和测试集
"""

import os
import shutil
import random
from pathlib import Path

def split_from_existing_split(input_dir, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    """
    从已有的分割数据集重新分割为训练集、验证集和测试集
    
    Args:
        input_dir: 输入数据集目录 (包含train/val文件夹)
        output_dir: 输出目录
        train_ratio: 训练集比例
        val_ratio: 验证集比例
        test_ratio: 测试集比例
        seed: 随机种子
    """
    random.seed(seed)
    
    # 创建输出目录结构
    train_images_dir = os.path.join(output_dir, 'train', 'images')
    train_labels_dir = os.path.join(output_dir, 'train', 'labels')
    val_images_dir = os.path.join(output_dir, 'val', 'images')
    val_labels_dir = os.path.join(output_dir, 'val', 'labels')
    test_images_dir = os.path.join(output_dir, 'test', 'images')
    test_labels_dir = os.path.join(output_dir, 'test', 'labels')
    
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)
    os.makedirs(val_labels_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)
    os.makedirs(test_labels_dir, exist_ok=True)
    
    # 收集所有现有的图片文件
    all_image_files = []
    
    # 从训练集收集
    train_images_path = os.path.join(input_dir, 'train', 'images')
    if os.path.exists(train_images_path):
        for f in os.listdir(train_images_path):
            if f.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                all_image_files.append(('train', f))
    
    # 从验证集收集
    val_images_path = os.path.join(input_dir, 'val', 'images')
    if os.path.exists(val_images_path):
        for f in os.listdir(val_images_path):
            if f.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                all_image_files.append(('val', f))
    
    print(f"总共收集到 {len(all_image_files)} 张图片")
    
    # 随机打乱
    random.shuffle(all_image_files)
    
    # 分割为三分
    train_split = int(len(all_image_files) * train_ratio)
    val_split = int(len(all_image_files) * (train_ratio + val_ratio))
    
    train_files = all_image_files[:train_split]
    val_files = all_image_files[train_split:val_split]
    test_files = all_image_files[val_split:]
    
    print(f"训练集: {len(train_files)} 张图片 ({len(train_files)/len(all_image_files)*100:.1f}%)")
    print(f"验证集: {len(val_files)} 张图片 ({len(val_files)/len(all_image_files)*100:.1f}%)")
    print(f"测试集: {len(test_files)} 张图片 ({len(test_files)/len(all_image_files)*100:.1f}%)")
    
    # 复制训练集
    print("复制训练集文件...")
    for source_dir, img_file in train_files:
        # 确定源路径
        if source_dir == 'train':
            src_img = os.path.join(input_dir, 'train', 'images', img_file)
            src_label = os.path.join(input_dir, 'train', 'labels', os.path.splitext(img_file)[0] + '.txt')
        else:
            src_img = os.path.join(input_dir, 'val', 'images', img_file)
            src_label = os.path.join(input_dir, 'val', 'labels', os.path.splitext(img_file)[0] + '.txt')
        
        # 复制图片
        dst_img = os.path.join(train_images_dir, img_file)
        shutil.copy2(src_img, dst_img)
        
        # 复制对应的标注文件
        if os.path.exists(src_label):
            dst_label = os.path.join(train_labels_dir, os.path.splitext(img_file)[0] + '.txt')
            shutil.copy2(src_label, dst_label)
    
    # 复制验证集
    print("复制验证集文件...")
    for source_dir, img_file in val_files:
        # 确定源路径
        if source_dir == 'train':
            src_img = os.path.join(input_dir, 'train', 'images', img_file)
            src_label = os.path.join(input_dir, 'train', 'labels', os.path.splitext(img_file)[0] + '.txt')
        else:
            src_img = os.path.join(input_dir, 'val', 'images', img_file)
            src_label = os.path.join(input_dir, 'val', 'labels', os.path.splitext(img_file)[0] + '.txt')
        
        # 复制图片
        dst_img = os.path.join(val_images_dir, img_file)
        shutil.copy2(src_img, dst_img)
        
        # 复制对应的标注文件
        if os.path.exists(src_label):
            dst_label = os.path.join(val_labels_dir, os.path.splitext(img_file)[0] + '.txt')
            shutil.copy2(src_label, dst_label)
    
    # 复制测试集
    print("复制测试集文件...")
    for source_dir, img_file in test_files:
        # 确定源路径
        if source_dir == 'train':
            src_img = os.path.join(input_dir, 'train', 'images', img_file)
            src_label = os.path.join(input_dir, 'train', 'labels', os.path.splitext(img_file)[0] + '.txt')
        else:
            src_img = os.path.join(input_dir, 'val', 'images', img_file)
            src_label = os.path.join(input_dir, 'val', 'labels', os.path.splitext(img_file)[0] + '.txt')
        
        # 复制图片
        dst_img = os.path.join(test_images_dir, img_file)
        shutil.copy2(src_img, dst_img)
        
        # 复制对应的标注文件
        if os.path.exists(src_label):
            dst_label = os.path.join(test_labels_dir, os.path.splitext(img_file)[0] + '.txt')
            shutil.copy2(src_label, dst_label)
    
    # 复制classes.txt
    src_classes = os.path.join(input_dir, 'classes.txt')
    if not os.path.exists(src_classes):
        src_classes = os.path.join(input_dir, 'train', '..', 'classes.txt')
    
    if os.path.exists(src_classes):
        dst_classes = os.path.join(output_dir, 'classes.txt')
        shutil.copy2(src_classes, dst_classes)
    
    print(f"数据集分割完成！")
    print(f"训练集保存在: {os.path.join(output_dir, 'train')}")
    print(f"验证集保存在: {os.path.join(output_dir, 'val')}")
    print(f"测试集保存在: {os.path.join(output_dir, 'test')}")

if __name__ == "__main__":
    base_dir = r"d:\项目\zsf"
    # 使用现有的分割数据集重新分割
    input_dataset = os.path.join(base_dir, 'yolo_dataset_temp', 'yolo_dataset_split')
    output_dataset = os.path.join(base_dir, 'yolo_dataset_split')
    
    # 先删除旧的输出目录
    if os.path.exists(output_dataset):
        shutil.rmtree(output_dataset)
    
    # 使用70%训练，15%验证，15%测试的比例
    split_from_existing_split(input_dataset, output_dataset, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42)