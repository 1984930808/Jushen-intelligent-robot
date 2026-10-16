# 贡献指南

感谢关注本 YOLO 工业目标检测项目。我们欢迎报告问题、修复 Bug 与提交新功能。

## 报告问题

1. 先搜索 Issues，避免重复  
2. 新建 Issue，说明环境（OS / Python / GPU）  
3. 给出最小复现步骤与日志/截图  

## 提交代码

1. Fork 本仓库并克隆到本地  
2. 创建特性分支：`git checkout -b feature/your-feature-name`  
3. 创建虚拟环境并安装依赖：

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

4. 修改代码，保持风格一致并补充必要注释  
5. 本地验证：

```bash
python verify_dataset.py   # 若已准备 dataset/
python run_demo.py
python -m pytest tests -q
# 或一键
python reproduce.py
```

6. 提交并推送，再创建 Pull Request，说明动机、改动点与测试结果  

## 代码规范

- 遵循 PEP 8  
- 函数保持单一职责，必要时补充 docstring  
- 不要把本机绝对路径写入 `data.yaml` 或其他配置  
- 不要提交大数据集、临时视频、密钥文件  

### 提交信息

```text
类型: 简短描述

详细说明（可选）
```

类型：`feat` / `fix` / `docs` / `style` / `refactor` / `test` / `chore`

示例：

```text
fix: 修正 data.yaml 相对路径以便异地复现
```

## 测试要求

提交前至少保证：

1. `python run_demo.py` 无报错  
2. `python -m pytest tests -q` 全部通过  
3. 若改动数据管线，需 `python verify_dataset.py` 通过  

## 文档贡献

文档位于：

- `README.md`  
- `docs/`  
- `FAQ.md` / `CHANGELOG.md`  

文档改动请同步更新 `CHANGELOG.md`。

## 行为准则

- 尊重贡献者，使用友善措辞  
- 接受建设性反馈，以可维护性与可复现性优先  

## 许可证

贡献代码即表示同意以 MIT 许可证发布。详见 [LICENSE](LICENSE)。

## 联系方式

- GitHub Issue  
- 邮件：1984930808@qq.com  
