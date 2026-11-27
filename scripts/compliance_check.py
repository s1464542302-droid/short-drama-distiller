#!/usr/bin/env python3
"""短剧解说脚本合规自检：检测剧透、替代式解说、照搬与绝对化用词风险。

用法: python compliance_check.py <脚本文件路径>
"""

import re
import sys
from pathlib import Path

REPLACEMENT_RULES = [
    ("代替原作", [r"\d+\s*分钟看完", r"几分钟看完", r"一口气看完", r"完整版", r"全剧", r"大结局"]),
    ("剧透结局", [r"最后.{0,12}(终于|还是|因此|所以).{0,20}(在一起|结婚|原谅|复仇|成功|死亡|破产)",
                  r"结局是", r"大结局", r"最终.{0,10}(结局|结果)", r"直到最后"]),
    ("照搬风险", [r"原声", r"原台词", r"直接截.{0,4}(片段|画面)", r"照搬", r"原片剪辑"]),
    ("绝对化用词", [r"最.{0,6}(好|狠|强|牛|可怕|精彩)", r"第一", r"绝对", r"百分百", r"100%"]),
    ("导流风险", [r"加微", r"微信", r"扫码", r"二维码", r"群聊", r"私信我"]),
]

OPINION_MARKERS = ["我认为", "在我看来", "这里妙在", "值得注意的是", "其实", "说白了",
                   "这一手", "问题在于", "讽刺的是", "换个角度看", "这其实", "在我看来"]

QUOTE_PATTERN = re.compile(r"[\u201c\u201d\"]([^\u201c\u201d\"]{8,})[\u201c\u201d\"]")


def check(text: str) -> list:
    findings = []
    for level, patterns in REPLACEMENT_RULES:
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                line = text[:match.start()].count("\n") + 1
                findings.append({
                    "level": level,
                    "line": line,
                    "matched": match.group(),
                    "pattern": pattern,
                })

    quotes = [q for q in QUOTE_PATTERN.findall(text) if len(q) >= 20]
    if quotes:
        findings.append({
            "level": "长引文风险",
            "line": 0,
            "matched": quotes[0][:30] + "...",
            "pattern": "单段引用 >= 20 字",
        })

    opinion_hits = sum(text.count(marker) for marker in OPINION_MARKERS)
    if opinion_hits < 3:
        findings.append({
            "level": "观点增量不足",
            "line": 0,
            "matched": f"仅检测到 {opinion_hits} 处观点标记",
            "pattern": "建议 >= 3 处明确观点表达",
        })
    return findings


def main() -> int:
    if len(sys.argv) != 2:
        print("用法: python compliance_check.py <脚本文件路径>")
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"文件不存在: {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    findings = check(text)

    print(f"检查文件: {path}")
    print(f"脚本字数: {len(text)}")
    print(f"发现问题: {len(findings)} 项")
    print("-" * 48)

    if not findings:
        print("通过：未检测到高风险项。仍需人工复核素材授权与观点占比。")
        return 0

    high = {"代替原作", "剧透结局"}
    for i, item in enumerate(findings, 1):
        tag = "高风险" if item["level"] in high else "提示"
        line = f"第 {item['line']} 行" if item["line"] else "全文"
        print(f"{i}. [{tag}] {item['level']} - {line}")
        print(f"   命中: {item['matched']}")
        print(f"   建议: {item['pattern']}")

    print("-" * 48)
    high_count = sum(1 for f in findings if f["level"] in high)
    if high_count:
        print(f"不通过：{high_count} 项高风险，必须修改后重跑。")
        return 1
    print("低风险：建议按提示优化后交付，并完成人工复核。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
