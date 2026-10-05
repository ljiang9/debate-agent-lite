"""命令行：python -m debate_agent_lite "AI 会不会取代程序员" --rounds 2。"""
from __future__ import annotations
import argparse, sys
from .debate import Debate, Turn
from .llm import llm_take_turn


def main(argv=None):
    ap = argparse.ArgumentParser(prog="debate-agent", description="正反方多角色辩论 + 裁判总结")
    ap.add_argument("topic"); ap.add_argument("--rounds", type=int, default=2); ap.add_argument("--llm", action="store_true")
    args = ap.parse_args(argv)
    if args.llm:
        history = []
        for r in range(1, args.rounds + 1):
            for side, stance, debater in [("正方", "支持该观点", Debate.new(args.topic).pro), ("反方", "反对该观点", Debate.new(args.topic).con)]:
                text = llm_take_turn(side, stance, args.topic, history)
                if text is None:
                    print("（LLM 不可用，整体回退规则辩手）", file=sys.stderr); return _run_rule(args)
                history.append({"speaker": debater.name, "text": text})
        debate = Debate.new(args.topic)
        for h in history: debate.turns.append(Turn(speaker=h["speaker"], text=h["text"], round=1))
        for t in debate.turns: print(f"【第{t.round}轮·{t.speaker}】{t.text}\n")
        print(debate.judge()); return 0
    return _run_rule(args)


def _run_rule(args):
    debate = Debate.new(args.topic)
    for t in debate.run(rounds=args.rounds): print(f"【第{t.round}轮·{t.speaker}】{t.text}\n")
    print(debate.judge()); return 0


if __name__ == "__main__": raise SystemExit(main())
