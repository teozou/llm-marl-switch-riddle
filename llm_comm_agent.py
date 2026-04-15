from openai import OpenAI
import json
from switch_riddle import SwitchRiddleEnv


client = OpenAI(
    base_url="https://api.mistral.ai/v1",
    api_key="YOUR_MISTRAL_API_KEY"cd ~/Desktop/KURF
)

def ask_llm(agent_id, light, n_agents, message_history):

    if message_history:
        messages_text = "\n".join(message_history)
    else:
        messages_text = "No messages yet — you are the first agent this episode."

    prompt = f"""You are playing the Switch Riddle. You are one of the prisoners.

Rules:
- 3 prisoners are brought one at a time into a room with a light switch
- The light starts OFF
- Each prisoner can only see: the light (ON or OFF) and their own ID (0, 1, or 2)
- Each prisoner can do one of 3 actions: do nothing (0), toggle the light (1), or declare that all 3 prisoners have visited the room (2)
- If a prisoner declares and all 3 have visited: everyone is freed
- If a prisoner declares but NOT all 3 have visited: everyone is imprisoned
- You can leave messages for other prisoners


Current situation:
- You are agent {agent_id}
- The light is {'ON' if light else 'OFF'}
- Messages from previous agents:
{messages_text}

You must choose an action NOW. What do you do?
THE STRATEGY YOU MUST FOLLOW:
- Agent 0 is the COUNTER.
- If you are NOT agent 0: toggle the light ON only if the light is OFF AND you have never toggled before. Otherwise do nothing.
- If you ARE agent 0: if the light is ON, toggle it OFF and count +1 in your reasoning. If your count reaches {n_agents - 1}, declare. Otherwise do nothing.

Reply ONLY with JSON, nothing else: {{"action": 0, "reasoning": "why"}}"""

    response = client.chat.completions.create(
        model="mistral-small-latest",
        messages=[
            {"role": "system", "content": "You are a game-playing AI. You MUST reply with ONLY a JSON object, no other text. Format: {\"action\": 0, \"reasoning\": \"why\"}"},
            {"role": "user", "content": prompt}
        ],
    )

    answer = response.choices[0].message.content
    answer = answer.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(answer)
        action = int(parsed["action"])
        reasoning = parsed["reasoning"]
    except:
        action = 0
        reasoning = "Could not parse LLM response"

    return action, reasoning

    response = client.chat.completions.create(
    model="mistral-small-latest",
    messages=[{"role": "user", "content": prompt}],
)

    answer = response.choices[0].message.content
    answer = answer.replace("```json", "").replace("```", "").strip()
 
    

    try:
        parsed = json.loads(answer)
        action = int(parsed["action"])
        reasoning = parsed["reasoning"]
    except:
        action = 0
        reasoning = "Could not parse LLM response"

    return action, reasoning



wins = 0
n_games = 100

for game in range(n_games):
    env = SwitchRiddleEnv(n_agents=3)
    obs = env.reset()
    done = False
    message_history = []

    while not done:
        light = obs[0]
        agent_id = obs[1]
        
        # Ask LLM what to do
        action, reasoning = ask_llm(agent_id, light, 3, message_history)
        
        # Add message to history
        message_history.append(f"Agent {agent_id} (light was {'ON' if light else 'OFF'}): {reasoning}")
        # Take action
        obs, reward, done, info = env.step(action)

    if reward == 1:
        wins += 1
        print("WIN!")
    else:
        print("LOSE")
print(f"\nLLM Success rate: {wins}/{n_games} = {(wins/n_games)*100}%")



