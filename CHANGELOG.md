# 更新日志

本文档记录项目的重要变更、算法优化与可复现性改进。

## [1.1.0] - 2026-10-16

### 新增
- 新增 `docs/` 技术文档（原理、安装、使用、数据、评估、API）
- 新增官方 Demo：`run_demo.py` + `demo/sample.png`
- 新增 `verify_dataset.py` 数据集校验脚本
- 新增 `reproduce.py` 异地一键复现脚本（可选 `--eval` 核对指标）
- 新增 `tests/` 自动化测试
- 在 README / docs 中补充性能指标（mAP / Precision / Recall）与引用方式

### 变更
- `data.yaml` 改为相对路径 `dataset/`，去除本机绝对路径
- `config.py` / `train.py` / `predict_simple.py` 对齐可复现默认路径
- 统一类别为 17 类，与发布权重一致
- 完善 `LICENSE` / `CONTRIBUTING.md` / `FAQ.md` / CI 工作流

### 算法与工程优化点
- 明确视觉检测与机械臂规划的模块边界，避免指标误导
- 指标复现增加 ±0.02 容差说明，降低异地环境波动误判
- CI 改为执行文档存在性检查、数据集配置校验、Demo 与 pytest

## [1.0.0] - 2026-09-20

### 新增
- 初始版本发布
- 支持 17 个工业组件类别目标检测
- 完整数据处理流程（XML/JSON 转换与划分）
- YOLOv11 训练与多模式预测（图片/视频/摄像头/批量）
- MIT 开源许可

### 支持的类别
- button, boardback, box-battery-g, box-battery-w, box-dispanel
- box-screen, box-screen2, screen, burner, burner-inside
- pcb, dispanel, boardback-f, cover, cover-e
- metalpallet, metalpallet-inside

### 技术特性
- 基于 Ultralytics YOLOv11
- 支持 PyTorch 2.0+

## 计划功能

### [1.2.0] - 计划中
- [ ] 模型导出（ONNX / TensorRT）
- [ ] 更多数据增强选项
- [ ] 推理速度专项优化

### [2.0.0] - 计划中
- [ ] Web / API 接口
- [ ] 与外部机械臂规划系统的示例对接文档

## 版本说明

- **新增**: 新功能  
- **变更**: 现有行为调整  
- **修复**: Bug 修复  
- **文档**: 文档更新  
