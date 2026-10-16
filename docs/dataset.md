# 数据集说明

## 目录结构

```text
dataset/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

配置文件 `data.yaml` 使用**相对路径** `path: dataset`，保证异地克隆后可直接使用。

## 当前规模（本地发布数据）

| 子集 | 图片数 |
|------|--------|
| train | 4915 |
| val | 1053 |
| test | 1054 |
| **合计** | **7022** |

## 类别（17）

`button`, `boardback`, `box-battery-g`, `box-battery-w`, `box-dispanel`, `box-screen`, `box-screen2`, `screen`, `burner`, `burner-inside`, `pcb`, `dispanel`, `boardback-f`, `cover`, `cover-e`, `metalpallet`, `metalpallet-inside`

## 获取方式

因体积较大，完整数据集通过网盘分发（见 README）。下载后解压到项目根目录，使路径满足上述结构。

## 校验

```bash
python verify_dataset.py
```

将检查：

- `classes.txt` 与 `data.yaml` 是否一致  
- train/val/test 是否存在图片  
- 图片/标注数量是否大致匹配  
