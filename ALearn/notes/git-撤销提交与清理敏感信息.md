# Git 撤销提交 & 清理敏感信息

## 方法一：回退最近 n 个提交（推荐，适用于个人分支）

```powershell
# 1. 软撤销最近 n 个提交（改动保留在工作区，不丢代码）
git reset --soft HEAD~n
#    HEAD~1  → 撤销最后 1 个提交
#    HEAD~3  → 撤销最后 3 个提交

# 2. 创建 .env 文件，把 API Key 移进去
# 3. 修改代码，把硬编码 key 改为读环境变量

# 4. 重新添加并提交
git add .
git commit -m "你的提交信息"

# 5. 强制推送到远程（个人分支用 --force-with-lease）
git push --force-with-lease origin 分支名
```

> `reset --soft` 只撤销提交本身，**不改动工作区的文件内容**，所有改动还保留在暂存区。
> `--force-with-lease` 比 `--force` 安全：推送前会检查远端是否有别人推了新提交，有则拒绝覆盖。

### 这个方法有什么局限？

`git reset --soft HEAD~n` 回退的是**最近连续的 n 个提交**。但如果：

- 敏感信息是**很久以前**提交的（比如 HEAD~20）
- 中间有很多正常的提交不想动

那回退 20 个提交会把正常的改动也撤销掉，不太合适。

---

## 方法二：单独修改某一个历史提交（cherry-pick 方式）

适用于"敏感信息是很久以前提交的，不想回退中间其他正常提交"。

```powershell
# 1. 找到敏感信息所在提交的前一个提交的 hash
#    比如：A - B - C - D
#          B 提交了 API Key，C 和 D 是正常提交
#          A 是 B 的上一个提交

# 2. 从 A 创建临时分支
git checkout -b cleanup-temp A的hash

# 3. 把 C 和 D 的改动"复制"过来（cherry-pick）
git cherry-pick C的hash
git cherry-pick D的hash

# 如果有冲突，解决后 git add . && git cherry-pick --continue

# 4. 再 cherry-pick B，然后修掉 key
git cherry-pick B的hash
# 修改代码，把硬编码 key → env 变量
git add .
git commit --amend --no-edit

# 5. 切回原分支，替换成清理后的历史
git switch 原分支名
git reset --hard cleanup-temp

# 6. 强制推送
git push --force-with-lease origin 分支名

# 7. 删除临时分支
git branch -D cleanup-temp
```

### 原理说明

```
原始历史：A - B(含key) - C - D
                     ↓
cherry-pick 后：A - C' - D' - B'(已清理)
                     ↑
            跳过有 key 的 B，最后才 cherry-pick 它并修掉 key
```

这样 C 和 D 的正常改动保持不变，只有 B 被修正。

---

## 方法三：全量清理历史（最深度的清理）

如果 key 已经暴露很久，或者涉及多个提交、多个分支：

```powershell
# 使用 git filter-repo 工具在整个仓库历史中替换掉指定字符串
```

> 此方法会重写全部分支历史，需要团队所有成员重新 clone。

---

## 如何预防

- 使用 `.env` + `python-dotenv` 管理密钥，`.env` 加入 `.gitignore`
- 安装 `pre-commit` 钩子自动扫描敏感信息
- CI 中加入密钥扫描（truffleHog、git-secrets）
