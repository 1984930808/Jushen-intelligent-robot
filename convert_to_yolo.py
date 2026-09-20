#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将三份数据的标注格式转换为YOLO训练格式
支持XML(Pascal VOC)和JSON(LabelMe)格式转换为YOLO格式
"""

import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import shutil

class LabelConverter:
    def __init__(self, base_dir: str, correct_classes_file: str = None):
        self.base_dir = base_dir
        self.classes = set()
        self.correct_classes = []
        
        # 如果提供了正确的类别文件，加载正确的类别顺序
        if correct_classes_file and os.path.exists(correct_classes_file):
            with open(correct_classes_file, 'r', encoding='utf-8') as f:
                self.correct_classes = [line.strip() for line in f.readlines()]
            print(f"使用正确的类别顺序，共 {len(self.correct_classes)} 个类别")
            for i, class_name in enumerate(self.correct_classes):
                print(f"  {i}: {class_name}")
        else:
            print("未提供正确的类别文件，将自动提取类别")
            self.correct_classes = None
        self.groups_info = {
            'group1': {
                'images_dir': os.path.join(base_dir, 'group1', 'iamges'),  # 注意拼写错误
                'labels_dir': os.path.join(base_dir, 'group1', 'labels'),
                'label_format': 'xml'
            },
            'group2': {
                'images_dir': os.path.join(base_dir, 'group2', 'images'),
                'labels_dir': os.path.join(base_dir, 'group2', 'labels'),
                'label_format': 'json'
            },
            'group3': {
                'images_dir': os.path.join(base_dir, 'group3', 'images'),
                'labels_dir': os.path.join(base_dir, 'group3', 'labels'),
                'label_format': 'json'
            }
        }
    
    def parse_xml_label(self, xml_path: str) -> Tuple[int, int, List[Dict]]:
        """
        解析XML格式的标注文件 (Pascal VOC格式)
        
        Args:
            xml_path: XML文件路径
            
        Returns:
            (image_width, image_height, objects_list)
            objects_list: [{"name": str, "bbox": [xmin, ymin, xmax, ymax]}, ...]
        """
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 获取图片尺寸
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        
        # 解析所有对象
        objects = []
        for obj in root.findall('object'):
            name = obj.find('name').text
            self.classes.add(name)
            
            bndbox = obj.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)
            
            objects.append({
                'name': name,
                'bbox': [xmin, ymin, xmax, ymax]
            })
        
        return width, height, objects
    
    def parse_json_label(self, json_path: str) -> Tuple[int, int, List[Dict]]:
        """
        解析JSON格式的标注文件 (LabelMe格式)
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            (image_width, image_height, objects_list)
            objects_list: [{"name": str, "bbox": [xmin, ymin, xmax, ymax]}, ...]
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 获取图片尺寸
        width = data.get('imageWidth', 640)  # 默认值
        height = data.get('imageHeight', 480)  # 默认值
        
        # 解析所有对象
        objects = []
        for shape in data.get('shapes', []):
            if shape['shape_type'] == 'rectangle':
                name = shape['label']
                self.classes.add(name)
                
                # LabelMe的points格式是[[x1, y1], [x2, y2]]
                points = shape['points']
                x1, y1 = points[0]
                x2, y2 = points[1]
                
                # 确保坐标顺序正确
                xmin = min(x1, x2)
                ymin = min(y1, y2)
                xmax = max(x1, x2)
                ymax = max(y1, y2)
                
                objects.append({
                    'name': name,
                    'bbox': [xmin, ymin, xmax, ymax]
                })
        
        return width, height, objects
    
    def convert_bbox_to_yolo(self, bbox: List[float], img_width: int, img_height: int) -> List[float]:
        """
        将边界框转换为YOLO格式 (归一化的中心坐标和宽高)
        
        Args:
            bbox: [xmin, ymin, xmax, ymax]
            img_width: 图片宽度
            img_height: 图片高度
            
        Returns:
            [x_center, y_center, width, height] (归一化到0-1)
        """
        xmin, ymin, xmax, ymax = bbox
        
        # 计算中心坐标和宽高
        x_center = (xmin + xmax) / 2.0
        y_center = (ymin + ymax) / 2.0
        width = xmax - xmin
        height = ymax - ymin
        
        # 归一化
        x_center /= img_width
        y_center /= img_height
        width /= img_width
        height /= img_height
        
        return [x_center, y_center, width, height]
    
    def convert_label_file(self, label_path: str, label_format: str, output_txt_path: str):
        """
        转换单个标注文件为YOLO格式
        
        Args:
            label_path: 标注文件路径
            label_format: 标注格式 ('xml' 或 'json')
            output_txt_path: 输出的YOLO格式文件路径
        """
        if label_format == 'xml':
            img_width, img_height, objects = self.parse_xml_label(label_path)
        elif label_format == 'json':
            img_width, img_height, objects = self.parse_json_label(label_path)
        else:
            raise ValueError(f"不支持的标注格式: {label_format}")
        
        # 转换为YOLO格式
        yolo_lines = []
        for obj in objects:
            name = obj['name']
            bbox = obj['bbox']
            
            # 转换边界框
            yolo_bbox = self.convert_bbox_to_yolo(bbox, img_width, img_height)
            
            # 获取类别ID (稍后会统一分配)
            class_id = name  # 临时使用类别名称
            
            yolo_line = f"{class_id} {yolo_bbox[0]:.6f} {yolo_bbox[1]:.6f} {yolo_bbox[2]:.6f} {yolo_bbox[3]:.6f}"
            yolo_lines.append(yolo_line)
        
        # 写入文件
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(yolo_lines))
    
    def convert_group(self, group_name: str, output_dir: str):
        """
        转换整个组的标注文件
        
        Args:
            group_name: 组名
            output_dir: 输出目录
        """
        group_info = self.groups_info[group_name]
        images_dir = group_info['images_dir']
        labels_dir = group_info['labels_dir']
        label_format = group_info['label_format']
        
        if not os.path.exists(labels_dir):
            print(f"警告: {labels_dir} 不存在，跳过")
            return
        
        if not os.path.exists(images_dir):
            print(f"警告: {images_dir} 不存在，跳过")
            return
        
        # 创建输出目录
        group_output_dir = os.path.join(output_dir, group_name)
        os.makedirs(group_output_dir, exist_ok=True)
        
        # 创建图片和标签子目录
        output_images_dir = os.path.join(group_output_dir, 'images')
        output_labels_dir = os.path.join(group_output_dir, 'labels')
        os.makedirs(output_images_dir, exist_ok=True)
        os.makedirs(output_labels_dir, exist_ok=True)
        
        # 处理每个标注文件
        label_files = [f for f in os.listdir(labels_dir) if f.endswith(f'.{label_format}')]
        
        converted_count = 0
        for label_file in label_files:
            label_path = os.path.join(labels_dir, label_file)
            base_name = label_file[:-len(f'.{label_format}')]
            
            # 查找对应的图片文件
            image_file = None
            for ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                potential_image = os.path.join(images_dir, base_name + ext)
                if os.path.exists(potential_image):
                    image_file = potential_image
                    break
            
            if image_file is None:
                print(f"警告: 找不到对应的图片文件: {base_name}")
                continue
            
            # 转换标注文件
            output_txt_path = os.path.join(output_labels_dir, base_name + '.txt')
            try:
                self.convert_label_file(label_path, label_format, output_txt_path)
                
                # 复制图片文件
                output_image_path = os.path.join(output_images_dir, os.path.basename(image_file))
                shutil.copy2(image_file, output_image_path)
                
                converted_count += 1
            except Exception as e:
                print(f"错误: 转换文件 {label_file} 失败: {e}")
        
        print(f"{group_name}: 转换了 {converted_count} 个文件")
    
    def convert_all_groups(self, output_dir: str):
        """
        转换所有组的标注文件
        
        Args:
            output_dir: 输出目录
        """
        print("开始转换标注文件...")
        print("=" * 50)
        
        # 转换每个组
        for group_name in self.groups_info.keys():
            self.convert_group(group_name, output_dir)
        
        print("=" * 50)
        print(f"总共发现 {len(self.classes)} 个类别")
        
        # 创建类别文件 - 使用正确的类别顺序（如果提供）
        if self.correct_classes:
            sorted_classes = self.correct_classes
            print("使用正确的类别顺序")
        else:
            sorted_classes = sorted(list(self.classes))
            print("使用字母排序的类别顺序")
        
        classes_file = os.path.join(output_dir, 'classes.txt')
        with open(classes_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted_classes))
        
        print(f"类别文件已保存到: {classes_file}")
        print("\n类别列表:")
        for i, class_name in enumerate(sorted_classes):
            print(f"  {i}: {class_name}")
        
        # 现在需要更新所有的标注文件，将类别名称替换为类别ID
        print("\n更新标注文件中的类别ID...")
        self.update_class_ids(output_dir, sorted_classes)
        
        print("转换完成！")
    
    def update_class_ids(self, output_dir: str, class_list: List[str]):
        """
        将标注文件中的类别名称替换为类别ID
        
        Args:
            output_dir: 输出目录
            class_list: 类别列表
        """
        class_to_id = {name: idx for idx, name in enumerate(class_list)}
        
        for group_name in self.groups_info.keys():
            labels_dir = os.path.join(output_dir, group_name, 'labels')
            if not os.path.exists(labels_dir):
                continue
            
            for txt_file in os.listdir(labels_dir):
                if txt_file.endswith('.txt'):
                    txt_path = os.path.join(labels_dir, txt_file)
                    
                    # 读取文件
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # 替换类别名称为类别ID
                    updated_lines = []
                    for line in lines:
                        parts = line.strip().split()
                        if parts:
                            class_name = parts[0]
                            if class_name in class_to_id:
                                class_id = class_to_id[class_name]
                                updated_line = f"{class_id} {' '.join(parts[1:])}\n"
                                updated_lines.append(updated_line)
                            else:
                                print(f"警告: 未知的类别 {class_name} 在文件 {txt_file}")
                                updated_lines.append(line)
                    
                    # 写回文件
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.writelines(updated_lines)

def main():
    # 项目根目录
    base_dir = r"d:\项目\zsf"
    
    # 输出目录
    output_dir = os.path.join(base_dir, 'yolo_dataset')
    
    # 正确的类别文件
    correct_classes_file = os.path.join(base_dir, 'classes.txt')
    
    # 创建转换器，传入正确的类别文件
    converter = LabelConverter(base_dir, correct_classes_file=correct_classes_file)
    
    # 转换所有组
    converter.convert_all_groups(output_dir)
    
    print(f"\nYOLO格式数据集已保存到: {output_dir}")
    print("目录结构:")
    print("  yolo_dataset/")
    print("    classes.txt")
    print("    group1/")
    print("      images/")
    print("      labels/")
    print("    group2/")
    print("      images/")
    print("      labels/")
    print("    group3/")
    print("      images/")
    print("      labels/")

if __name__ == "__main__":
    main()
