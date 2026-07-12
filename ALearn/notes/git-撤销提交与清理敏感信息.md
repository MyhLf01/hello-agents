# Git 撤销提交 & 清理敏感信息

## 场景：提交了含有 API Key 的代码怎么办？

### 方案一：重写最近提交历史（推荐，适用于个人分支）

```powershell
# 1. 把最近 n 个提交"软撤销"，改动保留在工作区
git reset --soft HEAD~n

# 2. 创建 .env 文件，把 API Key 移进去
# 内容格式：
#   TAVILY_API_KEY=tvly-xxx
#   DEEPSEEK_API_KEY=sk-xxx

# 3. 修改代码，把硬编码的 key 改为读环境变量
#   例：API_KEY = os.environ["DEEPSEEK_API_KEY"]

# 4. 把 .env 加入 .gitignore（确保不被提交）

# 5. 重新添加并提交
git add .
git commit -m "你的提交信息"

# 6. 强制推送到远程（因为是个人分支，用 --force-with-lease 更安全）
git push --force-with-lease origin 分支名
```

> ⚠️ `reset --soft` 只撤销提交、不删改代码。`--force-with-lease` 比 `--force` 安全，会先检查远端状态。

### 方案二：仅删除文件中的敏感信息（历史仍可查到）

```powershell
# 1. 修改文件，去掉 API Key
# 2. 提交修复
git add .
git commit -m "fix: remove hardcoded API keys"
git push origin 分支名
```

> ⚠️ 原始 API Key 仍存在于 git 历史中。如果仓库是公开的，**不推荐**此方案。

### 方案三：全量清理历史（最深度的清理）

如果 key 已经暴露很久，或者涉及多个提交：

```powershell
# 使用 git filter-repo 或 BFG Repo-Cleaner 工具
# 这会在整个仓库历史中替换掉指定字符串
```

---

## 如何预防

- 提交前用 `git diff --check` 检查
- 使用 `.env` + `python-dotenv` 管理密钥
- 使用 `pre-commit` 钩子自动扫描敏感信息
- CI 中加入密钥扫描（如 truffleHog、git-secrets）
