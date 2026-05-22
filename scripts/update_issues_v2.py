#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_issues_v2.py
批量将 AI 工具辅助学习板块（Tiny Lesson Prompt / NotebookLM 指引 / YouTube Shadowing 任务 / 即时自测题）
PATCH 更新到 GitHub 上的 12 个现有 Issues。
"""

import os
import json
import urllib.request
import urllib.error
import time

def read_env(env_path='.env'):
    env = {}
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"未找到 {env_path}")
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    env[parts[0].strip()] = parts[1].strip()
    return env

def make_github_request(url, data=None, token=None, method='PATCH'):
    req = urllib.request.Request(url, method=method)
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    req.add_header('User-Agent', 'HR-English-Training-Bot-v2')
    if data is not None:
        req.add_header('Content-Type', 'application/json')
        json_data = json.dumps(data).encode('utf-8')
    else:
        json_data = None
    try:
        with urllib.request.urlopen(req, data=json_data) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"GitHub API 错误 (HTTP {e.code}): {e.read().decode('utf-8')}")

# ─── AI 工具板块附加内容（追加到每个 Issue 现有 body 末尾） ───

AI_BLOCKS = {
    # ── WEEK 1 ──────────────────────────────────────────────────────────────
    1: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
将以下内容复制到 [Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson) 输入框，即时获得词汇 + 语法 + 发音：
```
Introducing myself as a senior HR director to a CEO in a first-round executive job interview
```

### 📔 NotebookLM 快速指引
1. 打开 [NotebookLM](https://notebooklm.google.com/)，新建笔记本"HR English Week 1"
2. 上传 `docs/week1_confidence_pitch.md` 全文
3. 点击 **Studio → Audio Overview → Generate**，生成通勤播客
4. 点击 **Studio → Flashcards**，每日复习 10 张词卡

### 🎬 YouTube Shadowing 任务
在 YouTube 搜索：`Linda Raynier "Tell Me About Yourself" senior executive`
精听目标：她如何用"I am known for..."开场，以及收尾时的语调变化。
跟读 1 个段落 5 次后，将该段落英文发在下方评论。

### 🧠 即时自测（回答后发在下方评论区）
1. 高管 Elevator Pitch 的三个阶段是？
   - A) Opening / Main / Closing
   - B) Who I Am / Proven Value / Future Fit ✅
   - C) Experience / Skills / Motivation

2. 以下哪个最具高管气场？
   - A) "I manage staff and do recruitment."
   - B) "I spearhead organizational transformation and enable talent at scale." ✅
   - C) "I handle HR operations."

3. "Pausing for Presence"的核心目的是？
   - A) 争取时间查字典
   - B) 展现沉着冷静的执行气场 ✅
   - C) 让面试官觉得你在背稿子
""",

    2: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Describing the strategic value I bring as an HRD or HRBP Leader in a multinational company
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

### 📔 NotebookLM 快速指引
上传 `week1_confidence_pitch.md` 后，在 Chat 框输入：
> *"Generate 5 quiz questions about the Elevator Pitch framework and executive HR vocabulary."*

收到问题后在下方评论区作答，AI 导师会为你批改！

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`Linda Raynier "Tell Me About Yourself" senior executive`
选择视频中**Phase 3 (Future Fit)** 部分的 1 个段落，跟读 5 次，然后把你**自己的 Elevator Pitch 草稿**发在下方评论区。

### 🧠 即时自测（发评论作答）
1. "Future Fit" 阶段的核心目的是？
   - A) 解释薪资期望
   - B) 清晰阐述你是该公司战略层面的最佳人选 ✅
   - C) 重复工作经历

2. "To spearhead" 的含义是？
   - A) 跟随别人的决定
   - B) 主动带头主导某项举措 ✅
   - C) 汇报给上级

3. 在自我介绍的 "Proven Value" 阶段，必须包含什么？
   - A) 学历背景
   - B) 量化的业务成果（如百分比、财务数据）✅
   - C) 个人兴趣爱好
""",

    3: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Using executive-level business vocabulary to describe 15 years of organizational HR experience
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

特别关注生成结果中的 **"Grammar Tips"** 部分——了解哪些时态和句型最适合描述多年经验。

### 📔 NotebookLM 快速指引
上传 `week1_confidence_pitch.md` 的**词汇表**部分（第三节"战略级 HR 核心词汇库"），生成 Flashcards，重点记忆以下 5 组对比词汇：
- Recruitment → Talent Acquisition
- Manage workers → Enable Talent
- C&B Design → Total Rewards Strategy
- Company changes → Change Management
- Find next boss → Succession Planning

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`HBR "Executive Presence How to Project Confidence"`
精听目标：注意高管们如何在回答问题**前**用思考停顿句（如 *"That's a great question..."*）争取组织语言的时间。跟读 1 个停顿句 + 后续 2 句，发在评论区。

### 🧠 即时自测（发评论作答）
1. "Talent Pipeline" 对应哪个 HR 专业概念？
   - A) 招聘渠道管理
   - B) 人才梯队建设 ✅
   - C) 薪酬体系设计

2. "To overhaul" 最接近哪个中文表达？
   - A) 小幅调整
   - B) 全面彻底改革 ✅
   - C) 暂时搁置

3. 在描述成就时，哪类信息最能提升说服力？
   - A) 主观感受（"I felt proud"）
   - B) 量化数据（百分比 / 财务收益 / 时间节点）✅
   - C) 团队规模
""",

    # ── WEEK 2 ──────────────────────────────────────────────────────────────
    4: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Presenting a successful organizational restructuring and headcount optimization to a CEO using executive-level English
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

### 📔 NotebookLM 快速指引
上传 `week2_behavioral_star.md`，生成 **Audio Overview（Debate 模式）**，让 AI 主播模拟"面试官"和"候选人"就 OD 重组话题展开对话，观察高分答法的语言结构。

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`Self Made Millennial Madeline Mann "STAR Method" senior interview`
精听目标：她如何用"First... Then... Finally..."让 Action 段落层次分明。
跟读 Action 段落 1 遍，然后用这个结构写出你自己某次 OD 变革的 3 个行动步骤（发在评论区）。

### 🧠 即时自测（发评论作答）
1. STAR 中 Action 部分应占回答总时长的大约多少？
   - A) 30%
   - B) 60% ✅
   - C) 80%

2. "Competency mapping matrix" 用于哪个 HR 场景？
   - A) 薪资对标
   - B) 组织重组中识别能力与消除重复岗位 ✅
   - C) 绩效评分

3. STAR 故事中 Situation 的理想篇幅是？
   - A) 占一半以上的时间详细描述背景
   - B) 2-3 句话快速点明商业痛点 ✅
   - C) 不需要描述背景，直接说结果
""",

    5: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Explaining how I resolved a complex labor dispute and protected the company from litigation in English
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

### 📔 NotebookLM 快速指引
上传你在本 Issue 评论区提交的 STAR 草稿（复制粘贴进 NotebookLM），在 Chat 框输入：
> *"What executive-level vocabulary can I use to make this STAR story more compelling and strategic?"*

将 AI 给出的词汇建议用到你的第二稿中，对比修改前后。

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`Self Made Millennial Madeline Mann "STAR Method" senior interview`
精听 Result 部分：她如何用停顿强调关键数据？跟读 Result 段落后，在评论区发出你自己案例的英文 Result（需含量化数据）。

### 🧠 即时自测（发评论作答）
1. "Empathic Exit process" 体现了哪种 HR 能力？
   - A) 成本控制
   - B) 员工关怀与法律风险管理 ✅
   - C) 薪酬设计

2. "Zero labor disputes, zero litigation" 这个 Result 展示了什么核心价值？
   - A) 高效裁员
   - B) 合规管理与雇主品牌保护 ✅
   - C) 节省招聘成本

3. 在员工关系 STAR 故事中，Action 部分最应重点强调？
   - A) 具体的合规步骤、谈判技巧与危机应对动作 ✅
   - B) 受影响员工的数量
   - C) 公司裁员的财务原因
""",

    6: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Presenting talent succession planning results and internal promotion metrics to a global CHRO
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

### 📔 NotebookLM 快速指引
上传 `week2_behavioral_star.md` 中的"战役三"内容，点击 **Studio → Quiz** 生成自动测验。完成后截图分数，发在评论区！

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`Harvard Business Review "How to Tell a Story in a Job Interview"`
精听：讲者如何用 *"This resulted in..."* / *"The impact was..."* 宣告成果。
跟读该句型 5 次，然后写出你自己的人才盘点 Result 段落（含数字）发在评论区。

### 🧠 即时自测（发评论作答）
1. "9-Box Grid framework" 是什么工具？
   - A) 薪酬对标矩阵
   - B) 评估员工绩效与潜力的人才盘点工具 ✅
   - C) 组织架构图

2. "Succession Pipeline" 的建立主要解决什么问题？
   - A) 降低当期人力成本
   - B) 减少对外部猎头的依赖，培养内部领导梯队 ✅
   - C) 提高员工日常满意度

3. 在 Result 中提到"节省猎头费用 $Y"属于哪类量化维度？
   - A) 效率指标
   - B) 财务 ROI 指标 ✅
   - C) 员工满意度指标
""",

    # ── WEEK 3 ──────────────────────────────────────────────────────────────
    7: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Diplomatically but firmly pushing back on a global HQ HR policy that conflicts with local Chinese labor laws
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

重点关注 Tiny Lesson 生成的 **Buffer 缓冲句型**，抄录在笔记本上熟记。

### 📔 NotebookLM 快速指引
上传 `week3_global_leadership.md`，生成 **Audio Overview（Debate 模式）**：让 AI 模拟"外籍总部 HR VP"与"本地 HRD"之间的 Pushback 对话，深度感受 BLS 公式的实际应用节奏。

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`"managing across cultures" HBR Harvard Business Review leadership`
精听：讲者如何用 *"from a different perspective..."* 或 *"on the other hand..."* 优雅表达不同意见。
跟读 1 段后，在评论区用英文写出你自己的一个 BLS Pushback 草稿（3句话即可）。

### 🧠 即时自测（发评论作答）
1. BLS 公式的三步是？
   - A) Brief / Listen / Solve
   - B) Buffer / Logic / Solution ✅
   - C) Build / Link / Sustain

2. Pushback 时最佳的开场白是？
   - A) "That won't work here."
   - B) "I completely understand and share your vision... however..." ✅
   - C) "I disagree with HQ's decision."

3. "A phased-in localization strategy" 的含义是？
   - A) 立刻全球统一执行
   - B) 分阶段将全球政策本地化合规适配 ✅
   - C) 拒绝总部政策
""",

    8: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Discussing global expansion challenges including cross-border hiring compliance in Southeast Asia with a VP
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

### 📔 NotebookLM 快速指引
上传 `week3_global_leadership.md`，在 Chat 框输入：
> *"Create a flashcard set for the global HR terminology: Localization, Cross-border Recruitment, Compliance Audit, Cultural Integration, Expatriate Management."*

用这 5 张闪卡每天复习，直到能在 3 秒内给出中英对照。

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`"cross-cultural management" executive leadership multinational`
精听：讲者如何描述在跨文化环境中建立信任的具体行动。
跟读 1 段后，在评论区写出你过去经历过的 1 个跨文化 HR 挑战，以及你采取的核心解决动作（英文 2-3 句）。

### 🧠 即时自测（发评论作答）
1. "Expatriate Management" 主要涉及哪类 HR 工作？
   - A) 本地员工日常管理
   - B) 跨国外派人员的薪酬、签证、生活支持等综合管理 ✅
   - C) 校园招聘

2. "Cultural Integration" 在出海企业 HR 中最核心的挑战是？
   - A) 建立本地薪酬体系
   - B) 弥合总部外派员工与本地员工之间的文化与沟通隔阂 ✅
   - C) 申请劳动许可证

3. "Compliance Audit" 在跨境建点时的作用是？
   - A) 对员工进行年度绩效评估
   - B) 全面审查当地劳动法律法规，规避用工合规风险 ✅
   - C) 统计员工满意度
""",

    9: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Strategically explaining a career transition gap to a skeptical CEO at a multinational company interview
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

### 📔 NotebookLM 快速指引
上传 `week3_global_leadership.md` 中"敏感情境应对"部分，在 Chat 框输入：
> *"Help me practice answering 'Why should we hire you?' as a senior HR professional with 15 years of experience. Give me 3 different executive-level response starters."*

选择你最喜欢的开场白，在下方评论区写出完整回答。

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`Stacy Mayer "executive women interview confidence gaps"`
精听：她如何把"空白期"重新框架为"战略性充电期"。
在评论区发出你自己的"空白期战略化解"英文答复（3-5 句话）。

### 🧠 即时自测（发评论作答）
1. 应对"职业空白期"的核心策略是？
   - A) 解释市场行情不好
   - B) 主动重构为"战略性职业转型期"，强调期间的主动增值行为 ✅
   - C) 避免谈论空白期

2. 在回答离职原因时，最应该避免什么？
   - A) 描述自己寻求更大挑战
   - B) 负面评价前任雇主或公司 ✅
   - C) 提及职业发展方向

3. "Career transition phase" vs "unemployment"，哪个表述对面试官更有说服力？
   - A) unemployment（更直接诚实）
   - B) career transition phase（主动掌控，增值导向）✅
   - C) 两者效果相同
""",

    # ── WEEK 4 ──────────────────────────────────────────────────────────────
    10: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Presenting a 30-60-90 day transition plan to a CEO in a final-round executive interview for an HRD position
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

### 📔 NotebookLM 快速指引
上传 `week4_mock_stress.md`，在 Chat 框输入：
> *"Generate a structured 30-60-90 day plan outline for an HRD joining a rapidly scaling company, using executive-level language."*

参考 AI 生成的框架，在下方评论区写出你的个人版 30-60-90 天规划大纲（英文，每阶段 2-3 个核心行动）。

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`"30 60 90 day plan executive" job interview presentation`
精听：候选人如何用 *"In my first 30 days, I plan to..."* 引出每个阶段的战略重点。跟读该句型结构并填入你自己的内容，发在评论区。

### 🧠 即时自测（发评论作答）
1. 30-60-90 天规划中，第一个 30 天的核心主题是？
   - A) 立即推动变革
   - B) Listen, Learn & Align（倾听、学习与对齐）✅
   - C) 裁减低效人员

2. 什么情况下主动拿出 30-60-90 天规划最有战略价值？
   - A) 第一轮电话面试时
   - B) 终面与 CEO 或业务负责人会谈时 ✅
   - C) 薪资谈判时

3. "Assess, Propose & Quick Wins" 对应哪个阶段？
   - A) 第一个 30 天
   - B) 第二个 30 天（Day 31-60）✅
   - C) 最后 30 天
""",

    11: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Asking high-level strategic business questions to a CEO or business leader at the end of a job interview
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

### 📔 NotebookLM 快速指引
上传 `week4_mock_stress.md`，在 Chat 框输入：
> *"Give me 5 high-impact questions that a senior HRD candidate should ask a CEO during a final-round interview to demonstrate strategic business acumen."*

从 AI 的建议中选出你最认同的 2-3 个，在评论区发出（英文），并说明你的选择理由（中文即可）。

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`Stacy Mayer "executive interview tips women leaders"`
精听：她如何用"I see myself as..."或"I am known for..."定义自己的领导力标签。
在评论区写出你自己的"**领导力身份宣言 (Leadership Identity Statement)**"（英文 1-2 句话）。

### 🧠 即时自测（发评论作答）
1. 面试结尾问"How many vacation days do I get?" 会给面试官什么印象？
   - A) 关注工作生活平衡，是优点
   - B) 重点放在个人福利而非战略贡献，印象负面 ✅
   - C) 显示你非常认真考虑这份工作

2. 以下哪个反问最能体现 HRD 的战略思维？
   - A) "When can I expect to hear back from you?"
   - B) "What is the biggest organizational barrier to your expansion goals, and how do you envision HR solving it?" ✅
   - C) "What does a typical workday look like in this role?"

3. 高端反问的核心目的是？
   - A) 获取更多 Offer 信息
   - B) 展示你对业务痛点的洞察力，并逆向掌控面试节奏 ✅
   - C) 表现礼貌
""",

    12: """
---

## 🤖 AI 工具实战加速

### 🔬 Tiny Lesson 即用 Prompt
```
Negotiating a senior executive salary package with an HR Director after receiving an initial job offer
```
[→ 打开 Tiny Lesson](https://labs.google/lll/en/experiments/tiny-lesson)

同时也试试 **Slang Hang** 功能，看看外企高管在非正式场合如何轻松讨论 *total package* / *ballpark figure* 等薪资词汇。

### 📔 NotebookLM 快速指引
上传本周所有 Issues 评论中你写的英文草稿（复制粘贴进去），在 Chat 框输入：
> *"Review my English writing samples and suggest 5 ways to make my language sound more executive, confident, and high-impact."*

将建议用到你的面试锦囊文档中！

### 🎬 YouTube Shadowing 任务
YouTube 搜索：`"salary negotiation executive" OR "how to negotiate salary offer senior manager" English coach`
精听：教练如何用 *"I was thinking more in the range of..."* 或 *"Based on the scope of this role and my track record..."* 优雅开口谈数字。
跟读该句型，在评论区模拟写出你的薪资谈判开场白（英文 2-3 句）。

### 🏆 30天闯关完成 · 终极冲刺自测（在评论区完成）
1. "Win-Win Negotiation" 最核心的原则是？
   - A) 坚持自己的底线不让步
   - B) 先展示对公司的战略价值，再提出基于市场数据的期望数字 ✅
   - C) 尽量少说话

2. "Proven track record" 在薪资谈判中的作用是？
   - A) 介绍学历背景
   - B) 用可量化的历史成果为自己的高薪要求提供有力背书 ✅
   - C) 表示对公司的忠诚

3. 30天学习结束后，你最大的英文口语突破是什么？（开放题，中英文均可，发在评论区）

> 🎉 **恭喜完成 30 天高管级 HR 英语突破计划！你已经准备好了。**
"""
}

def main():
    print("=" * 55)
    print("🚀 批量更新 12 个 GitHub Issues（注入 AI 工具板块）")
    print("=" * 55)

    try:
        env = read_env()
        token = env.get('GITHUB_TOKEN')
        username = env.get('GITHUB_USERNAME')
        if not token or not username:
            raise ValueError(".env 缺少 GITHUB_TOKEN 或 GITHUB_USERNAME")
        print(f"✅ 已读取配置：账号 = {username}")
    except Exception as e:
        print(f"❌ 读取 .env 失败: {e}")
        return

    repo_name = "hr-english-training"
    success_count = 0

    for issue_num in range(1, 13):
        ai_block = AI_BLOCKS.get(issue_num, "")
        if not ai_block:
            print(f"⚠️ Issue #{issue_num} 无对应 AI 板块，跳过")
            continue

        # 先 GET 原始 body
        get_url = f"https://api.github.com/repos/{username}/{repo_name}/issues/{issue_num}"
        try:
            existing = make_github_request(get_url, token=token, method='GET')
            original_body = existing.get('body') or ''
        except Exception as e:
            print(f"❌ 获取 Issue #{issue_num} 失败: {e}")
            continue

        # 若已包含 AI 板块则跳过（幂等保护）
        if '## 🤖 AI 工具实战加速' in original_body:
            print(f"ℹ️ Issue #{issue_num} 已含 AI 板块，跳过")
            continue

        new_body = original_body + ai_block

        patch_data = {"body": new_body}
        try:
            make_github_request(get_url, data=patch_data, token=token, method='PATCH')
            print(f"✅ Issue #{issue_num} 更新成功")
            success_count += 1
            time.sleep(1.2)  # 避免触发 GitHub API 速率限制
        except Exception as e:
            print(f"❌ Issue #{issue_num} 更新失败: {e}")

    print("\n" + "=" * 55)
    print(f"🎉 完成！成功更新 {success_count}/12 个 Issues")
    print(f"👉 https://github.com/{username}/{repo_name}/issues")
    print("=" * 55)

if __name__ == "__main__":
    main()
