# 性能指标与复现评估

## 参考指标（验证集）

基于仓库发布权重 `best.pt`（YOLOv11n，输入 640×640）在验证集上的结果：

| 指标 | 数值 |
|------|------|
| mAP@0.5 | **0.994** |
| mAP@0.5:0.95 | **0.935** |
| Precision | **0.992** |
| Recall | **0.993** |

说明：

1. 上述数值来自训练曲线与 PR 曲线（见 `docs/assets/`）。  
2. 异地复现允许 **±0.02** 容差（硬件、依赖小版本差异可能导致轻微波动）。  
3. **本仓库不包含机械臂规划模块**，因此不提供“机械臂规划成功率”指标；视觉检测结果可作为下游规划系统的输入。  

## 曲线资产

- `docs/assets/results.png`：训练/验证损失与 mAP 曲线  
- `docs/assets/PR_curve.png`：各类别 Precision-Recall  
- `docs/assets/P_curve.png` / `R_curve.png`：精度/召回曲线  

## 复现命令

```bash
# 不跑完整评估（推荐首次验证）
python reproduce.py

# 跑验证集并与参考指标对比（需 dataset/）
python reproduce.py --eval
```

或手动评估：

```bash
yolo val model=best.pt data=data.yaml split=val
```
