# 贡献指南

感谢您对YOLO目标检测项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告问题

如果您发现了bug或有功能建议，请：

1. 检查现有的Issues，确保问题没有被报告过
2. 创建新的Issue，详细描述问题
3. 提供复现步骤和相关信息
4. 如果可能，附上截图或日志

### 提交代码

1. **Fork 本仓库**
   ```bash
   # 在GitHub上点击Fork按钮
   ```

2. **克隆您的Fork**
   ```bash
   git clone https://github.com/your-username/yolo-detection.git
   cd yolo-detection
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **进行更改**
   - 遵循现有的代码风格
   - 添加必要的注释
   - 确保代码通过测试

5. **提交更改**
   ```bash
   git add .
   git commit -m "描述您的更改"
   ```

6. **推送到您的Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建Pull Request**
   - 在GitHub上创建Pull Request
   - 详细描述您的更改
   - 等待代码审查

## 代码规范

### Python代码风格

- 遵循PEP 8规范
- 使用有意义的变量名和函数名
- 添加必要的文档字符串
- 保持函数简洁，单一职责

### 提交信息规范

使用清晰的提交信息格式：

```
类型: 简短描述

详细描述（可选）
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例：
```
feat: 添加视频预测功能

支持对视频文件进行实时目标检测，可以保存检测结果
```

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/yolo-detection.git
cd yolo-detection
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行测试

```bash
python -m pytest tests/
```

## 测试指南

在提交代码前，请确保：

1. 代码能够正常运行
2. 不破坏现有功能
3. 添加适当的测试用例
4. 通过所有测试

## 文档贡献

如果您想改进文档：

1. Fork仓库
2. 修改相应的Markdown文件
3. 提交Pull Request
4. 说明文档改进的内容

## 行为准则

- 尊重所有贡献者
- 使用友好的语言
- 接受建设性的批评
- 关注对社区最有利的事情

## 许可证

通过贡献代码，您同意您的贡献将在MIT许可证下发布。

## 联系方式

如有疑问，请通过以下方式联系：

- 提交Issue
- 发送邮件至 [your-email@example.com]

感谢您的贡献！