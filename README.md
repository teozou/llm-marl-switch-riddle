# LLM Communication in Multi-Agent Reinforcement Learning

Comparing independent Q-learning (no communication) against LLM-based agents (natural language communication) on the Switch Riddle, a cooperative multi-agent task under partial observability.

## Overview

The Switch Riddle (Foerster et al., 2016) is a cooperative game where n agents must determine when all of them have visited a room, using only a light switch as a communication channel. Each agent can only observe the light (ON/OFF) and their own ID.

This project implements two approaches:
- **Independent Q-learning**: agents learn a Q-table over 6 states (2 light × 3 agents) with no communication. Limited by partial observability, achieving ~50% success.
- **LLM-based agent**: agents communicate via natural language messages through a Mistral LLM. Each agent reads previous messages and decides an action, achieving higher coordination.

The Switch Riddle is formalised as a Dec-POMDP. See [docs/formalization.md](docs/formalization.md) for the full mathematical specification.

## Execution

```bash
pip3 install gymnasium numpy openai
```

Run Q-learning agent:
```bash
python3 independent_q.py
```

Run LLM agent (requires a [Mistral API key](https://console.mistral.ai/)):
```bash
python3 llm_comm_agent.py
```

## Results

| Approach | Communication | Success Rate |
|----------|--------------|-------------|
| Independent Q-learning | None | ~40-60% |
| LLM agent | Natural language | ~20-80% |

## Project Structure

```
├── switch_riddle.py        # Switch Riddle environment
├── independent_q.py        # Q-learning agent
├── llm_comm_agent.py       # LLM-based communicating agent
├── frozenLake.py           # Q-learning on FrozenLake (training exercise)
├── docs/
│   └── formalization.md    # Dec-POMDP formal specification
└── README.md
```

## References

- Foerster, J. et al. (2016). *Learning to Communicate with Deep Multi-Agent Reinforcement Learning*. NeurIPS.
- Sun, C. et al. (2024). *LLM-based Multi-Agent Reinforcement Learning: Current and Future Directions*. arXiv:2405.11106.