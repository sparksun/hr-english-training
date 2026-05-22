#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import urllib.request
import urllib.error
import subprocess
import time

def read_env(env_path='.env'):
    env = {}
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"未找到环境配置文件 {env_path}")
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    env[parts[0].strip()] = parts[1].strip()
    return env

def run_cmd(cmd, cwd=None):
    print(f"执行命令: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, cwd=cwd, shell=True if isinstance(cmd, str) else False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"命令执行失败，错误输出:\n{res.stderr}")
    else:
        print(f"命令成功执行:\n{res.stdout.strip()}")
    return res

def make_github_request(url, data=None, token=None, method='POST'):
    req = urllib.request.Request(url, method=method)
    req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    req.add_header('User-Agent', 'HR-English-Training-Bot')
    
    if data is not None:
        req.add_header('Content-Type', 'application/json')
        json_data = json.dumps(data).encode('utf-8')
    else:
        json_data = None
        
    try:
        with urllib.request.urlopen(req, data=json_data) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        try:
            err_json = json.loads(err_body)
            message = err_json.get('message', '')
            errors = err_json.get('errors', [])
            # 捕获仓库已存在的错误
            if e.code == 422 and any("already exists" in str(err) or "already exists" in message for err in errors + [message]):
                print("目标 GitHub 仓库已存在，将直接使用现有仓库。")
                return {"already_exists": True}
        except:
            pass
        raise RuntimeError(f"GitHub API 请求失败 (HTTP {e.code}): {err_body}")

def main():
    print("====================================================")
    print("🚀 启动 30天高管级 HR 英语突破计划 GitHub 自动化配置")
    print("====================================================")
    
    # 1. 读取 .env
    try:
        env = read_env()
        token = env.get('GITHUB_TOKEN')
        username = env.get('GITHUB_USERNAME')
        if not token or not username:
            raise ValueError(".env 中缺少 GITHUB_TOKEN 或 GITHUB_USERNAME")
        print(f"成功读取配置：GitHub 账号 = {username}")
    except Exception as e:
        print(f"❌ 读取 .env 失败: {e}")
        return

    repo_name = "hr-english-training"
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"项目本地根目录: {workspace_dir}")

    # 2. 初始化本地 Git 仓库
    print("\n--- [步骤 1/5] 初始化本地 Git 仓库 ---")
    if not os.path.exists(os.path.join(workspace_dir, '.git')):
        run_cmd(["git", "init"], cwd=workspace_dir)
    
    run_cmd(["git", "add", "."], cwd=workspace_dir)
    run_cmd(["git", "commit", "-m", "Initialize 30-Day Executive HR English Training program"], cwd=workspace_dir)

    # 3. 在 GitHub 上创建远程仓库
    print("\n--- [步骤 2/5] 在 GitHub 上创建远程仓库 ---")
    create_repo_url = "https://api.github.com/user/repos"
    repo_data = {
        "name": repo_name,
        "description": "30-Day Executive HR English Training Program designed for senior HR professionals transitioning to HRD/HRBP Leader roles.",
        "private": True,  # 默认创建私有仓库以彻底保护学生个人隐私
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
    
    try:
        res_repo = make_github_request(create_repo_url, data=repo_data, token=token, method='POST')
    except Exception as e:
        print(f"❌ 创建仓库失败: {e}")
        return

    # 4. 关联远程仓库并推送代码
    print("\n--- [步骤 3/5] 关联远程仓库并推送代码 ---")
    # 移除现有 remote origin 以免冲突
    run_cmd(["git", "remote", "remove", "origin"], cwd=workspace_dir)
    
    # 组装带 Token 的远程 URL 以免除 SSH 或输入密码交互
    remote_url = f"https://{token}@github.com/{username}/{repo_name}.git"
    run_cmd(["git", "remote", "add", "origin", remote_url], cwd=workspace_dir)
    run_cmd(["git", "branch", "-M", "main"], cwd=workspace_dir)
    
    # 推送代码至远程仓库
    run_cmd(["git", "push", "-u", "origin", "main"], cwd=workspace_dir)

    # 5. 创建 4 个里程碑
    print("\n--- [步骤 4/5] 创建每周学习里程碑 (Milestones) ---")
    milestone_url = f"https://api.github.com/repos/{username}/{repo_name}/milestones"
    
    milestones_def = [
        {
            "title": "Week 1: 认知重塑与 HR 专业叙事 (Confidence & Pitch)",
            "description": "目标：重塑英文表达信心，克服口语焦虑；攻克 3 分钟黄金自我介绍 (Elevator Pitch)；精练战略 HR 高频英文词汇与地道发音。",
            "due_on": None  # 可由学生手动在网页端配置具体日期
        },
        {
            "title": "Week 2: STAR 深度行为面试实战 (STAR Achievements)",
            "description": "目标：精通高管级 STAR 故事线写法；整理出组织发展 (OD)、员工关系 (ER) 及人才发展三大核心 HR 维度的量化成果案例。",
            "due_on": None
        },
        {
            "title": "Week 3: 跨文化沟通与全球领导力 (Intercultural Influence)",
            "description": "目标：掌握向上管理、优雅坚定的 Pushback 话术；掌握出海招聘与合规表达；完美应对“待业空白期”、“离职原因”等敏感难题。",
            "due_on": None
        },
        {
            "title": "Week 4: 压力面试模拟与战略宣讲 (Mock Stress & Offer)",
            "description": "目标：撰写展示即战力的英文“30-60-90天工作计划”；掌握反问面试官的高层级问题；精进英文薪资谈判与 Offer 最终敲定。",
            "due_on": None
        }
    ]

    milestone_mapping = {}  # 记录里程碑标题 -> 编号 (number) 的映射
    for m in milestones_def:
        try:
            res_m = make_github_request(milestone_url, data=m, token=token, method='POST')
            m_number = res_m.get('number')
            milestone_mapping[m['title']] = m_number
            print(f"✅ 成功创建里程碑: {m['title']} (Milestone #{m_number})")
        except Exception as e:
            print(f"⚠️ 创建里程碑失败 {m['title']}: {e}")
            # 如果里程碑已经存在，尝试通过 GET 获取已有的里程碑编号
            try:
                list_url = f"https://api.github.com/repos/{username}/{repo_name}/milestones"
                existing = make_github_request(list_url, token=token, method='GET')
                for ext_m in existing:
                    if ext_m['title'] == m['title']:
                        milestone_mapping[m['title']] = ext_m['number']
                        print(f"ℹ️ 找到已有里程碑: {m['title']} (Milestone #{ext_m['number']})")
                        break
            except Exception as ex:
                print(f"❌ 检索已有里程碑失败: {ex}")

    # 6. 创建 12 个 Issue
    print("\n--- [步骤 5/5] 自动派发 30 天每日学习与打卡任务 (Issues) ---")
    issue_url = f"https://api.github.com/repos/{username}/{repo_name}/issues"
    
    issues_def = [
        # WEEK 1 ISSUES
        {
            "title": "Issue #1: 【第1-2天】认知重塑：克服英语口语焦虑与重建高管英文气场",
            "body": """## 🎯 任务背景与核心挑战
作为有 15 年以上丰富 HR 管理积淀的资深候选人，面对外企或中资出海企业高管时，最核心的障碍是口语焦虑与“追求完美语法”的心理负担。本任务将带你重塑认知，以结果为导向重新建立你的 **Executive Presence (执行气场)**。

## 📝 本期学习要点 (README & docs 查阅)
- 详细阅读并学习：`docs/week1_confidence_pitch.md` 中的“认知调频三法则”及“高管顿挫与留白”。
- 掌握 **以商业结果为中心** 的心法，将英文看作单纯传递你 HR 战略价值的桥梁。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请用**中文或英文**写下你在过往英文交流中最容易产生焦虑的 3 个具体瞬间（例如：被外籍高管突然提问、找不到合适的高级词汇等）。你的 AI 导师会针对性地提供“抗焦虑口语缓冲套路”，帮助你在终面中从容化解尴尬！""",
            "milestone_title": "Week 1: 认知重塑与 HR 专业叙事 (Confidence & Pitch)"
        },
        {
            "title": "Issue #2: 【第3-4天】黄金自我介绍：打磨你的 3 分钟 HRD / HRBP Leader 专属 Elevator Pitch",
            "body": """## 🎯 任务背景与核心挑战
自我介绍是整个面试的基调。一个顶尖的 HRD 或 HRBP Leader 的英文介绍，绝不是机械地复述简历，而是要通过**“战略定位 - 核心成果量化 - 角色完美匹配”**三部曲来打动面试官。

## 📝 本期学习要点 (README & docs 查阅)
- 仔细研读 `docs/week1_confidence_pitch.md` 中的“黄金 3 分钟高管 Elevator Pitch 模板”。
- 挑选**模板一（战略HRD）**或**模板二（业务BP Leader）**作为你的起草骨架。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
1. **书面打卡**：根据模版，将占位符（如 `[Name]`, `[X%]`, `[Specialty]`）替换为你个人的真实战略历程，并在下方评论区贴出你撰写好的 3 分钟英文自我介绍草稿。
2. **口语打卡（选做）**：对着镜子大声朗读你的英文介绍，录制音频上传至网盘或免注册录音工具，将链接贴在评论区。

> **AI 导师承诺**：收到你的草稿后，我将亲自为你修改润色，剔除不符合高管身份的底层词汇，融入更具魄力与商业高度的词汇（如 spearhead, overhaul, optimize），让你在面试的第一分钟就牢牢抓住面试官！""",
            "milestone_title": "Week 1: 认知重塑与 HR 专业叙事 (Confidence & Pitch)"
        },
        {
            "title": "Issue #3: 【第5-7天】战略 HR 核心英语词汇与高管级发音练习",
            "body": """## 🎯 任务背景与核心挑战
很多资深 HR 习惯使用 "I recruit employees" 或 "I manage labor problems" 这样较为被动的日常英语。本任务将带你彻底升级词汇库，换上外企 CXO 们每天都在高频使用的战略级词汇。

## 📝 本期学习要点 (README & docs 查阅)
- 精读 `docs/week1_confidence_pitch.md` 中的“战略级 HR 核心词汇对照表”。
- 特别熟练掌握以下动作词汇：`spearhead`（主导）、`bridge the gap`（搭建桥梁）、`optimize`（优化）、`enable`（赋能）。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请挑选词汇表中的任意 3 个“升级版战略级 HR 表达”（例如：*Talent Pipeline*, *Change Management*, *Drive Organizational Alignment*），并结合你自己过去的成功经历，各造一个英文句子。

*造句参考示例*：
> *"I spearheaded the Change Management process to bridge the gap between global strategy and local team capability."*""",
            "milestone_title": "Week 1: 认知重塑与 HR 专业叙事 (Confidence & Pitch)"
        },
        
        # WEEK 2 ISSUES
        {
            "title": "Issue #4: 【第8-9天】STAR 战役一：组织发展 (OD) 与架构变革的英文叙事",
            "body": """## 🎯 任务背景与核心挑战
组织发展 (OD) 与架构调整是体现 HRD 战略高度的终极战役。在英文描述重组和变革时，必须清晰体现出你的**商业出发点、变革阻力克服过程以及最终的财务/效率量化结果**。

## 📝 本期学习要点 (README & docs 查阅)
- 深入阅读 `docs/week2_behavioral_star.md` 中的“战役一：组织发展 (OD) 与架构调整”案例模板。
- 掌握如何用英文分配 STAR 的时间比例（Action 占 60%，Result 占 25%）。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请根据你的真实经历，将“战役一”模板中的数据与情境进行替换，起草一份你自己的 **OD变革 STAR 英文故事草稿**。

> **AI 导师润色重点**：我将着重帮您润色 Action 部分，确保展现出您作为领导者在变革管理中强大的跨部门影响力（Stakeholder alignment）与变革推进力！""",
            "milestone_title": "Week 2: STAR 深度行为面试实战 (STAR Achievements)"
        },
        {
            "title": "Issue #5: 【第10-11天】STAR 战役二：危机处理与重难点员工关系 (ER) 英文谈判",
            "body": """## 🎯 任务背景与核心挑战
员工关系谈判、重大裁员纠纷或工会危机处理，是对 HR 候选人情商、法务严谨度与现场控制力的巨大考验。在英文叙述中，如何体现你的“有原则的共情力”与“零法律纠纷的商业安全意识”至关重要。

## 📝 本期学习要点 (README & docs 查阅)
- 精读 `docs/week2_behavioral_star.md` 中的“战役二：危机处理与重难点员工关系谈判”。
- 特别记忆表达合规性与危机化解的短语：`empathic exit`（共情式离职）、`zero litigation`（零诉讼）、`labor regulation compliance`（符合劳动法规范）。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请回忆你过去 15 年经历中**最艰难、或最成功的一次员工关系危机处理/裁员谈判**案例。在下方用英文（或中英双语）尝试写出你当时采取的 3 个最核心动作（Actions）以及量化的安全过渡结果（Results）。AI 导师会全力协助你打磨出一段充满张力与说服力的故事。""",
            "milestone_title": "Week 2: STAR 深度行为面试实战 (STAR Achievements)"
        },
        {
            "title": "Issue #6: 【第12-14天】STAR 战役三：人才盘点、继任者计划与绩效变革英文呈现",
            "body": """## 🎯 任务背景与核心挑战
面试官常问：*"How do you ensure the organization has a continuous talent pipeline?"*（你如何确保组织拥有持续的人才梯队？）。作为资深 HR 领导者，你需要用系统化的工具（如九宫格 9-Box Grid）和量化数据（内部晋升率、猎头费节省）来展现你的专业成果。

## 📝 本期学习要点 (README & docs 查阅)
- 仔细学习 `docs/week2_behavioral_star.md` 中的“战役三：人才盘点与继任计划”。
- 掌握诸如 `9-Box Grid framework`（九宫格框架）、`succession pipeline`（继任梯队）、`accelerated development programs`（加速培养计划）等专业术语。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请根据你的实际经验，在下方贴出你的“人才盘点与梯队建设”英文 STAR 故事。在 Result 中，请务必尝试包含一个量化的数据（例如：*“内部晋升率提升了 [X%]”*，或 *“节省了猎头招聘费用 $[Y]”*）。这将使你的专业说服力提升十倍！""",
            "milestone_title": "Week 2: STAR 深度行为面试实战 (STAR Achievements)"
        },
        
        # WEEK 3 ISSUES
        {
            "title": "Issue #7: 【第15-16天】向上管理与总部对接：跨文化英文影响力与坚定的 Pushback 艺术",
            "body": """## 🎯 任务背景与核心挑战
无论是外企还是出海企业，HRD 经常面临全球总部（HQ）不切实际的要求。面试官会极力探寻：*"当总部政策在本地行不通时，你该如何沟通？"*

## 📝 本期学习要点 (README & docs 查阅)
- 精读并背诵 `docs/week3_global_leadership.md` 中的 **BLS 沟通公式 (Buffer-Logic-Solution)**。
- 深刻理解如何用极其职业且委婉的句型（如 *"To mitigate this, I propose a phased-in localization strategy..."*）表达异议。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请设想一个经典冲突情境：**“总部要求立即执行全球统一的薪酬框架，但该框架在本地严重缺乏招聘竞争力，且有合规隐患”**。
请尝试使用 BLS 公式，在下方评论区用英文写出你的 Pushback 话术草稿。导师会从语意分寸感和高管说服力上为您进行保驾护航！""",
            "milestone_title": "Week 3: 跨文化沟通与全球领导力 (Intercultural Influence)"
        },
        {
            "title": "Issue #8: 【第17-18天】中资出海与全球化HR挑战：海外建点招聘合规与多元文化融合",
            "body": """## 🎯 任务背景与核心挑战
面对出海热潮，面试官极度关注 HR 领导者对于跨国/跨境业务的适应能力，包括海外建点招聘、异国劳动法合规、外派干部管理及中外团队文化融合等。

## 📝 本期学习要点 (README & docs 查阅)
- 精读 `docs/week3_global_leadership.md` 中的“全球化管理英文术语库”。
- 掌握 `Localization`（本土化）、`Cross-border Recruitment`（跨境招聘）、`Compliance Audit`（合规审计）等高频词汇。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请在下方发表评论，阐述你对以下问题的英文核心观点（两到三句话即可）：
*"How do you handle cultural integration when a Chinese expanding company hires senior local executives in a European or Southeast Asian market?"*
（当中资出海企业在欧洲或东南亚市场聘请资深当地高管时，你如何处理文化融合问题？）""",
            "milestone_title": "Week 3: 跨文化沟通与全球领导力 (Intercultural Influence)"
        },
        {
            "title": "Issue #9: 【第19-21天】敏感情境应对：如何体面战略性地解释“待业空白期”与“跳槽动机”",
            "body": """## 🎯 任务背景与核心挑战
对于有一定待业空白期的优秀经理人，如何自信、体面、且极具战略意义地阐述这一段过渡期，是赢得面试官信任的胜负手。我们必须摆脱“弱势解释”姿态，转化为“主动掌控、自我增值”的高管格局。

## 📝 本期学习要点 (README & docs 查阅)
- 精读并背诵 `docs/week3_global_leadership.md` 中针对**“职业空白期 (Gap Period)”**的黄金高管答复。
- 深刻理解如何将空白期包装为有计划的“Strategic career transition phase”（战略性职业转型期），并强调期间的主动充电与增值。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请将 `docs/week3_global_leadership.md` 中关于空白期的英文模板复制下来，根据你最近的学习方向（如出海合规、英语学习、高管教练等）进行个性化替换，并将你的专属答复草稿发在下方评论区。导师将亲自为你把关，确保回答听起来极具力量感与自信心！""",
            "milestone_title": "Week 3: 跨文化沟通与全球领导力 (Intercultural Influence)"
        },
        
        # WEEK 4 ISSUES
        {
            "title": "Issue #10: 【第22-24天】战略入职规划：撰写英文 30-60-90 天工作计划大纲",
            "body": """## 🎯 任务背景与核心挑战
终面面对 CEO 级别面试官时，光被动回答问题是不够的。主动拿出一份 **30-60-90 天的入职框架**，能瞬间让面试官对你入职后的即战力产生具体画面感。

## 📝 本期学习要点 (README & docs 查阅)
- 详细阅读 `docs/week4_mock_stress.md` 中的 “30-60-90天入职规划英文架构”。
- 掌握三大核心步骤的命名：
  - *First 30 Days: "Listen, Learn & Align"*
  - *Next 30 Days: "Assess, Propose & Quick Wins"*
  - *Last 30 Days: "Optimize, Scale & Enable"*

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请设想你即将入职一家正处于快速变革或全球化扩张期的企业。请尝试为这三个阶段各写出一项你作为 HRD/HRBP Leader 会立即驱动的英文具体行动（Actions）。导师会帮助你对齐表述，使其听起来极具可落地性与战略广度！""",
            "milestone_title": "Week 4: 压力面试模拟与战略宣讲 (Mock Stress & Offer)"
        },
        {
            "title": "Issue #11: 【第25-27天】逆向掌控：如何在面试尾声向高管提出高水准的业务反问",
            "body": """## 🎯 任务背景与核心挑战
当面试官问出 *"Do you have any questions for us?"* 时，是整场面试的黄金收尾期。这是一个你向面试官展示商业嗅觉和探寻组织底细的绝佳主动机会。

## 📝 本期学习要点 (README & docs 查阅)
- 学习 `docs/week4_mock_stress.md` 中的“高管反问黄金问题推荐”。
- 掌握反问组织期望、战略协同以及文化包容度的高级句式。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请从推荐问题中挑选出你个人最喜欢的 2 个英文反问问题贴在下方。写下你在终面中面对 CEO 时会选择哪两个问题，并说明你的考虑（中文即可）。导师会帮你纠正临场发音的抑扬顿挫，确保反问听起来非常自信、得体。""",
            "milestone_title": "Week 4: 压力面试模拟与战略宣讲 (Mock Stress & Offer)"
        },
        {
            "title": "Issue #12: 【第28-30天】极限压力面试模拟与英文薪酬谈判话术实战",
            "body": """## 🎯 任务背景与核心挑战
恭喜你进入了突破计划的最后一环！拿到 Offer 后的薪资谈判，是关乎职业尊严与实际回报的终极博弈。如何优雅、坚定、有理有据地通过英文争取最高薪资，是我们的核心目标。

## 📝 本期学习要点 (README & docs 查阅)
- 精读并背诵 `docs/week4_mock_stress.md` 中的两个高管英文薪资谈判实战场景。
- 掌握强调自身 15 年溢价能力的话术短语：`proven track record`（经证实的优异往绩）、`yield a significant organizational return`（带来显著的组织回报）。

## ✍️ 本期打卡作业 (直接在下方发表 Comment)
请根据你的实际目标期望，在下方贴出一段你模拟与外企 HR 进行英文薪酬拉锯谈判的话术。
你可以这样开始：
> *"Thank you very much for this offer... However, looking at the complete scope of responsibilities..."*

AI 导师将亲自为你打磨这篇极具说服力的“要价话术”，协助你完美斩获高管级别的丰厚 Offer！""",
            "milestone_title": "Week 4: 压力面试模拟与战略宣讲 (Mock Stress & Offer)"
        }
    ]

    for issue in issues_def:
        m_title = issue['milestone_title']
        m_num = milestone_mapping.get(m_title)
        
        issue_data = {
            "title": issue['title'],
            "body": issue['body']
        }
        if m_num is not None:
            issue_data["milestone"] = m_num
            
        try:
            res_issue = make_github_request(issue_url, data=issue_data, token=token, method='POST')
            issue_num = res_issue.get('number')
            print(f"✅ 成功发布任务卡: {issue['title']} (Issue #{issue_num}) 并关联至里程碑 #{m_num}")
            # 适当休眠，避免触发 GitHub API 速率限制
            time.sleep(1)
        except Exception as e:
            print(f"❌ 发布任务卡失败 {issue['title']}: {e}")

    print("\n====================================================")
    print("🎉 自动化部署圆满完成！")
    print(f"👉 您的交互式 HR 英语学习项目地址：")
    print(f"👉 https://github.com/{username}/{repo_name}")
    print("====================================================")

if __name__ == "__main__":
    main()
