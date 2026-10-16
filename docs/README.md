# 技术文档

本目录提供 YOLO 工业目标检测开源包的技术说明，便于二次开发与异地复现。

## 文档索引

| 文档 | 说明 |
|------|------|
| [algorithm.md](algorithm.md) | 算法原理与流程 |
| [install.md](install.md) | 环境安装与依赖 |
| [usage.md](usage.md) | 训练、预测、Demo 使用 |
| [dataset.md](dataset.md) | 数据集结构与准备 |
| [evaluation.md](evaluation.md) | 性能指标与复现评估 |
| [api.md](api.md) | 主要脚本与配置接口 |

## 快速入口

```bash
# 安装
pip install -r requirements.txt

# 一键复现（Demo + 测试）
python reproduce.py

# 含验证集指标核对（需先准备 dataset/）
python reproduce.py --eval
```

## 指标曲线

训练/验证曲线与 PR 曲线见 [`assets/`](assets/)：

- `results.png`
- `PR_curve.png`
- `P_curve.png`
- `R_curve.png`
