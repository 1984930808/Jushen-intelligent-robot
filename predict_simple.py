#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的YOLO预测示例脚本
用于快速测试模型
"""

from ultralytics import YOLO

# 加载模型
model = YOLO("best.pt")

# 测试图片预测
image_path = "test.jpg"  # 替换为你的测试图片路径
results = model(image_path, conf=0.25)

# 显示结果
for result in results:
    result.show()  # 显示结果
    result.save("result.jpg")  # 保存结果
    
    # 打印检测到的物体
    print(f"检测到 {len(result)} 个物体:")
    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = result.names[class_id]
        confidence = float(box.conf[0])
        print(f"  {class_name}: {confidence:.2f}")