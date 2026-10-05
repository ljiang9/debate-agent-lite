"""辩论核心：两个/多个 mock 立场轮流陈述，裁判总结。"""
from __future__ import annotations
from dataclasses import dataclass, field


ARGUMENTS_PRO = [
    "我方认为应当如此：这是经过长期实践验证的方向，能够带来整体效率的提升。",
    "从成本收益角度看，这样做的长期收益远大于短期投入。",
    "已有多个类似案例表明该方向是可行且稳健的。",
]
ARGUMENTS_CON = [
    "我方持反对意见：该方案在现实约束下风险被严重低估。",
    "从长期看，这样做会牺牲灵活性与可持续性。",
    "反对理由在于：执行成本与维护负担会随规模非线性增长。",
]
REBUTTAL_PRO = [
    "对方的担忧可以通过分阶段实施与指标监控来化解，而不是整体否定方向。",
    "我们承认风险存在，但因噎废食的代价更大。",
]
REBUTTAL_CON = [
    "对方提到的收益在当前数据条件下并不可靠，属于乐观假设。",
    "我们并非反对改进，而是反对在没有充分验证前就全面铺开。",
]


@dataclass
class Turn:
    speaker: str
    text: str
    round: int


class RuleDebater:
    def __init__(self, name, side):
        self.name = name; self.side = side
    def open_statement(self, topic, round_no):
        pool = ARGUMENTS_PRO if self.side == "pro" else ARGUMENTS_CON
        return f"[{self.name}] 关于「{topic}」，{pool[(round_no - 1) % len(pool)]}"
    def rebuttal(self, topic, prev_turn, round_no):
        pool = REBUTTAL_PRO if self.side == "pro" else REBUTTAL_CON
        return f"[{self.name}] 回应「{prev_turn.speaker}」：{pool[(round_no - 1) % len(pool)]}"


class Judge:
    def summarize(self, topic, turns):
        if not turns: return f"# 辩论总结：{topic}\n\n（双方均未发言）"
        pro = [t for t in turns if "正方" in t.speaker]
        con = [t for t in turns if "反方" in t.speaker]
        out = [f"# 辩论总结：{topic}", "",
               f"共进行 {max(t.round for t in turns)} 轮，{len(turns)} 次发言。",
               f"- 正方发言 {len(pro)} 次，核心立场：应当推进、重视长期收益。",
               f"- 反方发言 {len(con)} 次，核心立场：谨慎推进、重视风险与成本。", "",
               "裁判点评：双方在「方向价值」与「执行风险」之间形成了典型的权衡。",
               "建议：以小规模试点 + 指标监控的方式折中推进。"]
        return "\n".join(out)


@dataclass
class Debate:
    topic: str
    pro: RuleDebater
    con: RuleDebater
    turns: list = field(default_factory=list)

    @classmethod
    def new(cls, topic, pro_name="正方", con_name="反方"):
        return cls(topic=topic, pro=RuleDebater(pro_name, "pro"), con=RuleDebater(con_name, "con"))

    def run(self, rounds=2):
        self.turns = []; prev = None
        for r in range(1, rounds + 1):
            pro_text = self.pro.open_statement(self.topic, r) if prev is None else self.pro.rebuttal(self.topic, prev, r)
            prev = Turn(speaker=self.pro.name, text=pro_text, round=r); self.turns.append(prev)
            con_text = self.con.rebuttal(self.topic, prev, r)
            prev = Turn(speaker=self.con.name, text=con_text, round=r); self.turns.append(prev)
        return self.turns

    def judge(self):
        return Judge().summarize(self.topic, self.turns)
