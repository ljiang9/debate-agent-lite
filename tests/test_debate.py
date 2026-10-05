import os, sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from debate_agent_lite.debate import Debate, RuleDebater, Judge, Turn
from debate_agent_lite.llm import llm_take_turn


class TestDebate(unittest.TestCase):
    def test_rule_debater_open(self):
        text = RuleDebater("正方", "pro").open_statement("AI 是否好", 1)
        self.assertIn("正方", text); self.assertIn("AI 是否好", text)
    def test_rule_debater_rebuttal(self):
        text = RuleDebater("反方", "con").rebuttal("话题", Turn(speaker="正方", text="x", round=1), 1)
        self.assertIn("反方", text); self.assertIn("回应", text)
    def test_debate_run_complete(self):
        turns = Debate.new("AI 会不会取代程序员").run(rounds=2)
        self.assertEqual(len(turns), 4)
        self.assertEqual([t.speaker for t in turns], ["正方", "反方", "正方", "反方"])
        self.assertEqual([t.round for t in turns], [1, 1, 2, 2])
    def test_judge_summary(self):
        deb = Debate.new("测试辩题"); deb.run(rounds=2)
        s = deb.judge()
        self.assertIn("测试辩题", s); self.assertIn("总结", s)
    def test_judge_handles_empty(self):
        self.assertIsInstance(Judge().summarize("空题", []), str)
    def test_llm_no_key_returns_none(self):
        old = os.environ.pop("OPENAI_API_KEY", None)
        try: self.assertIsNone(llm_take_turn("正方", "支持", "话题"))
        finally:
            if old: os.environ["OPENAI_API_KEY"] = old


if __name__ == "__main__": unittest.main()
