"""debate_agent_lite: 正反方多角色辩论，规则辩手走完整流程；有 LLM 用 LLM。"""
from .debate import Debate, RuleDebater, Judge
from .llm import llm_take_turn

__all__ = ["Debate", "RuleDebater", "Judge", "llm_take_turn"]
__version__ = "0.1.0"
