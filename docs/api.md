# 脚本与配置接口

## 核心脚本

| 脚本 | 作用 |
|------|------|
| `run_demo.py` | 官方 Demo 推理入口 |
| `predict.py` | 图片/视频/摄像头/批量预测 |
| `predict_simple.py` | 最小预测示例 |
| `train.py` | 模型训练 |
| `verify_dataset.py` | 数据集结构校验 |
| `reproduce.py` | 一键复现（依赖/Demo/测试/可选评估） |
| `convert_to_yolo.py` | 标注格式转换 |
| `split_dataset.py` | 数据集划分 |

## `config.py`

常用常量：

- `ROOT`：项目根目录  
- `DATASET_DIR`：`dataset/`  
- `DATA_YAML`：`data.yaml`  
- `MODEL_PATH`：`best.pt`  
- `DEMO_IMAGE`：`demo/sample.png`  
- `REFERENCE_METRICS`：README/文档中的参考指标  
- `NUM_CLASSES`：17  

```python
from config import get_config
print(get_config())
```

## `data.yaml`

```yaml
path: dataset
train: train/images
val: val/images
test: test/images
nc: 17
names: [...]
```

注意：`path` 必须保持相对路径，避免写死本机绝对路径。
