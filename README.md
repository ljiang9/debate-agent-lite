# debate-agent-lite

零依赖的正反方多角色辩论小工具。给定一个辩题，两个 mock 立场（正方/反方）按轮次轮流陈述与反驳，最后由裁判输出总结。设置 OPENAI_API_KEY 后可选 LLM 发言，无 key 自动降级为规则辩手，规则辩手始终能跑完整流程。

## 快速开始

```bash
python -m debate_agent_lite "AI 会不会取代程序员" --rounds 2
```

## 无 API Key 如何运行

默认就是规则辩手模式，完全离线。加 --llm 但没设 OPENAI_API_KEY 时，会打印一行降级提示并继续用规则辩手跑完整流程。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## License

MIT © ljiang9
