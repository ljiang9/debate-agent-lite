"""可选 LLM 发言：仅用 urllib；无 key 时返回 None。"""
from __future__ import annotations
import json, os, urllib.request

SYSTEM_TMPL = ("你是辩论赛中的{side}辩手，立场：{stance}。"
               "请用中文写一段 80~120 字的发言，直接陈述观点，不要前缀。")


def llm_take_turn(side, stance, topic, history=None):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key: return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    messages = [{"role": "system", "content": SYSTEM_TMPL.format(side=side, stance=stance)}, {"role": "user", "content": f"辩题：{topic}\n请发言。"}]
    for h in (history or [])[-4:]: messages.append({"role": "assistant", "content": h["text"]})
    payload = {"model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"), "messages": messages, "temperature": 0.7}
    req = urllib.request.Request(f"{base}/chat/completions", data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None
