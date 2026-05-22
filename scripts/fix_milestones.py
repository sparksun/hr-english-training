#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import urllib.request
import urllib.error
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
        raise RuntimeError(f"GitHub API 请求失败 (HTTP {e.code}): {err_body}")

def main():
    print("====================================================")
    print("🛠 修复 GitHub 里程碑配置并关联现有 Issue")
    print("====================================================")
    
    try:
        env = read_env()
        token = env.get('GITHUB_TOKEN')
        username = env.get('GITHUB_USERNAME')
        if not token or not username:
            raise ValueError(".env 中缺少 GITHUB_TOKEN 或 GITHUB_USERNAME")
    except Exception as e:
        print(f"❌ 读取 .env 失败: {e}")
        return

    repo_name = "hr-english-training"
    milestone_url = f"https://api.github.com/repos/{username}/{repo_name}/milestones"
    
    milestones_def = [
        {
            "title": "Week 1: 认知重塑与 HR 专业叙事 (Confidence & Pitch)",
            "description": "目标：重塑英文表达信心，克服口语焦虑；攻克 3 分钟黄金自我介绍 (Elevator Pitch)；精练战略 HR 高频英文词汇与地道发音。"
        },
        {
            "title": "Week 2: STAR 深度行为面试实战 (STAR Achievements)",
            "description": "目标：精通高管级 STAR 故事线写法；整理出组织发展 (OD)、员工关系 (ER) 及人才发展三大核心 HR 维度的量化成果案例。"
        },
        {
            "title": "Week 3: 跨文化沟通与全球领导力 (Intercultural Influence)",
            "description": "目标：掌握向上管理、优雅坚定的 Pushback 话术；掌握出海招聘与合规表达；完美应对“待业空白期”、“离职原因”等敏感难题。"
        },
        {
            "title": "Week 4: 压力面试模拟与战略宣讲 (Mock Stress & Offer)",
            "description": "目标：撰写展示即战力的英文“30-60-90天工作计划”；掌握反问面试官的高层级问题；精进英文薪资谈判与 Offer 最终敲定。"
        }
    ]

    # 1. 创建里程碑（省略 due_on 以免 API 报错）
    milestone_mapping = {}
    for m in milestones_def:
        try:
            res_m = make_github_request(milestone_url, data=m, token=token, method='POST')
            m_number = res_m.get('number')
            milestone_mapping[m['title']] = m_number
            print(f"✅ 成功创建里程碑: {m['title']} (Milestone #{m_number})")
        except Exception as e:
            # 如果已经存在，尝试拉取
            print(f"ℹ️ 里程碑可能已存在，尝试检索: {m['title']}")
            try:
                list_url = f"https://api.github.com/repos/{username}/{repo_name}/milestones"
                existing = make_github_request(list_url, token=token, method='GET')
                found = False
                for ext_m in existing:
                    if ext_m['title'] == m['title']:
                        milestone_mapping[m['title']] = ext_m['number']
                        print(f"✅ 找到已有里程碑: {m['title']} (Milestone #{ext_m['number']})")
                        found = True
                        break
                if not found:
                    print(f"❌ 无法创建或找到里程碑: {m['title']}. 错误: {e}")
            except Exception as ex:
                print(f"❌ 获取里程碑列表失败: {ex}")
        time.sleep(0.5)

    # 2. 关联 Issues 1 到 12
    # Issue #1-3 -> Milestone Week 1
    # Issue #4-6 -> Milestone Week 2
    # Issue #7-9 -> Milestone Week 3
    # Issue #10-12 -> Milestone Week 4
    
    issue_to_milestone = {}
    m1 = milestone_mapping.get("Week 1: 认知重塑与 HR 专业叙事 (Confidence & Pitch)")
    m2 = milestone_mapping.get("Week 2: STAR 深度行为面试实战 (STAR Achievements)")
    m3 = milestone_mapping.get("Week 3: 跨文化沟通与全球领导力 (Intercultural Influence)")
    m4 = milestone_mapping.get("Week 4: 压力面试模拟与战略宣讲 (Mock Stress & Offer)")
    
    for i in range(1, 4):
        if m1: issue_to_milestone[i] = m1
    for i in range(4, 7):
        if m2: issue_to_milestone[i] = m2
    for i in range(7, 10):
        if m3: issue_to_milestone[i] = m3
    for i in range(10, 13):
        if m4: issue_to_milestone[i] = m4

    print("\n--- 开始将现有 Issue 绑定至相应里程碑 ---")
    for issue_num, m_num in issue_to_milestone.items():
        update_url = f"https://api.github.com/repos/{username}/{repo_name}/issues/{issue_num}"
        patch_data = {"milestone": m_num}
        try:
            make_github_request(update_url, data=patch_data, token=token, method='PATCH')
            print(f"✅ 成功将 Issue #{issue_num} 关联至里程碑 #{m_num}")
            time.sleep(0.5)
        except Exception as e:
            print(f"❌ 关联 Issue #{issue_num} 失败: {e}")

    print("\n====================================================")
    print("🎉 里程碑修复及 Issue 绑定工作全部顺利完成！")
    print("====================================================")

if __name__ == "__main__":
    main()
