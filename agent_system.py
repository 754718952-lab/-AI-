#!/usr/bin/env python3
"""
小米百万亿Token激励计划 - 多智能体自动编程系统
====================================================
多Agent架构：架构师 → 程序员 → 测试员 → 修复循环
充分使用长上下文和多次API调用，展现Token消耗能力。

运行前请设置环境变量：
export MIMO_API_KEY="your_key"
export MIMO_BASE_URL="https://api.xiaomimimo.com/v1"   # 请替换为实际端点
"""
import os
import time
import json
import openai

# ---------- 配置 ----------
client = openai.OpenAI(
    api_key=os.environ.get("MIMO_API_KEY", "your-api-key-here"),
    base_url=os.environ.get("MIMO_BASE_URL", "https://api.mimomodel.com/v1")
)
MODEL = "mimo-v2.5-pro"  # 根据实际情况修改

token_usage = {"total_tokens": 0}

def log_usage(usage):
    if usage:
        token_usage["total_tokens"] += usage.total_tokens

# ---------- Agent 角色 ----------
class Architect:
    """架构师：输出技术方案"""
    def design(self, requirement: str) -> str:
        prompt = f"""你是一名资深软件架构师。针对以下需求设计一个完整的软件方案，输出应包含：
- 推荐技术栈
- 项目文件结构
- 各模块职责
需求：{requirement}"""
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是一个严谨的软件架构师。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1024
        )
        log_usage(resp.usage)
        return resp.choices[0].message.content.strip()

class Coder:
    """程序员：生成代码"""
    def generate(self, arch: str, filename: str, description: str) -> str:
        prompt = f"""架构设计：
{arch}

请生成文件 {filename}，功能：{description}
直接输出完整代码（含注释），不要任何解释。"""
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是一名高级程序员。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=2048
        )
        log_usage(resp.usage)
        return resp.choices[0].message.content.strip()

class Tester:
    """测试员：审查代码"""
    def review(self, filename: str, code: str) -> str:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是资深测试工程师。找出代码BUG、安全漏洞、边界条件缺失等，给出修复建议。"},
                {"role": "user", "content": f"审查文件 {filename}:\n```\n{code}\n```"}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        log_usage(resp.usage)
        return resp.choices[0].message.content.strip()

class Fixer:
    """修复员：根据审查意见改进代码"""
    def fix(self, filename: str, original_code: str, review: str) -> str:
        prompt = f"""根据审查意见修复 {filename} 的代码。
审查意见：{review}

原始代码：
{original_code}
输出完整的修复后代码。"""
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是代码修复专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=2048
        )
        log_usage(resp.usage)
        return resp.choices[0].message.content.strip()

# ---------- 主流程 ----------
def main():
    print("🚀 多智能体自动编程系统启动（目标：待办事项Web应用）")
    start = time.time()

    # 1. 架构设计
    arch = Architect().design("一个简单的待办事项Web应用，支持添加、删除、标记完成，使用Python Flask后端，前端纯HTML/JS/CSS")
    print("\n=== 架构方案 ===")
    print(arch[:400] + "..." if len(arch) > 400 else arch)

    # 2. 代码生成
    coder = Coder()
    files = {
        "app.py": "Flask 后端，REST API，内存存储待办事项",
        "index.html": "前端页面，包括输入框、待办列表、删除和完成按钮",
        "styles.css": "简洁美观的样式",
        "requirements.txt": "Python依赖 Flask==2.3.2"
    }
    generated = {}
    for fname, desc in files.items():
        print(f"\n[程序员] 生成 {fname} ...")
        code = coder.generate(arch, fname, desc)
        generated[fname] = code
        with open(fname, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"  生成 {len(code)} 字符")

    # 3. 测试审查
    tester = Tester()
    reviews = {}
    for fname in generated:
        print(f"\n[测试员] 审查 {fname} ...")
        rev = tester.review(fname, generated[fname])
        reviews[fname] = rev
        print(f"  发现 {len(rev.splitlines())} 条意见")

    # 4. 修复（一次迭代）
    fixer = Fixer()
    for fname in generated:
        print(f"\n[修复员] 修复 {fname} ...")
        improved = fixer.fix(fname, generated[fname], reviews[fname])
        with open(fname, "w", encoding="utf-8") as f:
            f.write(improved)
        print(f"  已更新文件")

    elapsed = time.time() - start
    print("\n✅ 所有任务完成！")
    print(f"⏱ 总耗时 {elapsed:.1f} 秒")
    print(f"💰 总 Token 消耗: {token_usage['total_tokens']}")
    print("文件已生成在当前目录，可运行: python app.py")

if __name__ == "__main__":
    main()