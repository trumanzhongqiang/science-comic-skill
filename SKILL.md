---
name: science-comic-skill
description: "给自媒体一键生成科普漫画：选题理解、事实核查、分镜脚本、角色卡锚定一致性、逐格出图、气泡留空后期填字。触发词：'启动科普漫画'、'科普漫画'、相关自然语言请求。"
version: 1.1.0
allowed-tools: Bash, Read, Write, Edit
compatibility: Windows/macOS/Linux. Requires WorkBuddy.
metadata:
  emoji: "🎨"
---

# 科普漫画一键生成

收到本 SKILL.md 意味着用户想把一个科普选题变成一套可发布的漫画图片。核心工作流：选题理解 → 事实核查 → 角色卡锚定 → 分镜脚本 → 逐格出图 → 气泡文字后期合成 → 装读者四查（发布前质检）。

详细执行指令见 `skill/science-comic-skill/SKILL.md`，打包加载请使用根目录的 `science-comic-skill.skill` 文件。

## 快速使用

1. 在 WorkBuddy 中加载 `science-comic-skill.skill`
2. 对助手说「启动科普漫画」或直接给出选题，例如「把『为什么天空是蓝色的』做成 6 格漫画」
3. 助手会依次产出：知识卡 → 角色卡 → 分镜脚本 → 逐格图片 → 合成成品
