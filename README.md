# Git助手 (Git Helper)

一个简单易用的Git图形界面工具，专为不熟悉Git命令行的用户设计。通过简单的点击操作，即可完成Git版本控制的基本功能。

## 功能特点

- 图形化界面，操作简单直观
- 支持SSH和HTTPS两种远程仓库连接方式
- 自动处理分支创建和切换
- 智能错误提示和处理
- 支持多次提交和远程仓库URL更改
- 可指定任意分支名（不存在则自动创建）

## 安装要求

- Python 3.6 或更高版本
- Git 客户端
- 必需的Python包：
  ```bash
  pip install gitpython tkinter
  ```

## 使用前准备

1. **安装Git**：
   - Windows: 从 [Git官网](https://git-scm.com/download/win) 下载并安装
   - Linux: `sudo apt-get install git` (Ubuntu/Debian)
   - macOS: `brew install git` (使用Homebrew)

2. **配置SSH密钥**（如果使用SSH方式）：
   ```bash
   ssh-keygen -t rsa -b 4096 -C "你的邮箱"
   ```
   将生成的公钥（.pub文件）添加到GitHub账户设置中。

## 使用说明

1. **启动程序**：
   ```bash
   python git_helper.py
   ```

2. **基本操作流程**：

   a. **选择代码文件夹**
   - 点击"选择代码文件夹"按钮
   - 选择要进行版本控制的文件夹

   b. **初始化Git仓库**
   - 点击"初始化Git仓库"按钮
   - 如果文件夹已经是Git仓库，会提示"无需重新初始化"

   c. **设置远程仓库**
   - 在输入框中输入远程仓库URL
   - 支持SSH格式：`git@github.com:用户名/仓库名.git`
   - 支持HTTPS格式：`https://github.com/用户名/仓库名.git`
   - 点击"设置远程仓库"按钮

   d. **添加文件**
   - 点击"添加所有更改"按钮，将添加所有新文件和修改

   e. **提交更改**
   - 在提交信息输入框中输入描述性的提交信息
   - 点击"提交更改"按钮

   f. **推送到远程仓库**
   - 在分支输入框中输入目标分支名（默认为main）
   - 点击"推送到GitHub"按钮

## 常见问题解决

1. **推送失败**：
   - 检查网络连接
   - 确认SSH密钥配置正确
   - 确保远程仓库URL正确

2. **权限被拒绝**：
   - 检查SSH密钥是否正确添加到GitHub
   - 确认有仓库的写入权限

3. **分支冲突**：
   - 程序会自动尝试合并不相关的历史
   - 如果有冲突，需要手动解决后重新提交

## 注意事项

- 首次使用建议选择空文件夹开始
- 确保提交前已保存所有文件更改
- 推荐使用SSH方式连接GitHub，更安全便捷
- 定期提交和推送以保持代码同步

## 技术支持

如果遇到问题，请检查以下内容：
1. Git是否正确安装（在终端运行 `git --version`）
2. Python环境是否正确配置
3. 必需的Python包是否已安装
4. SSH密钥是否正确配置（如果使用SSH）

## 贡献指南

欢迎提交问题和建议！可以通过以下方式参与：
1. 提交Issue
2. 提交Pull Request
3. 分享使用经验

## 许可证

MIT License

## 使用SSH方式的前提

使用SSH形式的远程仓库URL（如 `git@github.com:ZHYsfl/xxxxxxxx.git`）前提是：

1. **配置SSH密钥**：
   - 在本地生成SSH密钥对（公钥和私钥）：
   ```bash
   ssh-keygen -t rsa -b 4096 -C "你的邮箱"
   ```
   - 生成的文件通常在：
     - Windows: `C:\Users\你的用户名\.ssh\`
     - Linux/Mac: `~/.ssh/`
   - 会生成两个文件：
     - `id_rsa`（私钥）
     - `id_rsa.pub`（公钥）

2. **将公钥添加到GitHub**：
   - 复制 `id_rsa.pub` 文件的内容
   - 登录GitHub
   - 进入Settings -> SSH and GPG keys
   - 点击"New SSH key"
   - 粘贴公钥内容并保存

3. **测试SSH连接**：
   ```bash
   ssh -T git@github.com
   ```
   如果看到 "Hi username! You've successfully authenticated" 就说明配置成功。

如果没有完成这些步骤，使用SSH形式的URL会报错"Permission denied"。 