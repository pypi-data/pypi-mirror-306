
# ApeAgent

**ApeAgent** is a framework created by Macaque Consulting to develop intelligent agents capable of executing specific functions (tools) sequentially or in parallel, while maintaining conversation context. This multi-agent approach is ideal for complex systems requiring efficient token usage and detailed process control..

## Installation

```bash
pip install apeagent
```

## Multi-Agent System Advantages

The multi-agent orchestration in **ApeAgent** optimizes token usage and enhances model accuracy in complex environments. Key benefits include:

- **Token consumption reduction**: Each agent uses only the necessary context for each query, optimizing costs and speed.
- **Detailed process control**: Specialized agents enable granular control and easy debugging, perfect for systems that require precise task management.
- **Reduced hallucinations**: By dividing tasks into specialized agents, the system minimizes incoherent or inaccurate responses.
- **Capability for self-supervision or "judge" systems**: You can include an agent to verify responses from other agents before presenting them to the user.
- **Efficiency and parallelism**: Agents can execute tasks in parallel and maintain context in long conversations.

## Agent Configuration Parameters

When configuring an agent in **ApeAgent**, you can adjust its behavior through several parameters:

- **`name`**: Agent name, without spaces.
- **`instructions`**: System role message that guides the agent (defines its purpose).
- **`functions`**: Tools or agents the agent can access, listed as a list.
- **`model`**: Model to use (currently integrates with OpenAI models).
- **`temperature`**: Controls the agent's response creativity.
- **`parallel_tool_calls`**: Allows the agent to run tools in parallel.
- **`memory_enabled`**: Allows the agent to keep conversation context.
- **`memory_max_conversations`**: Max number of interactions the agent stores in memory.
- **`debug`**: Enables console output for debugging.

## Defining Tools

Tools are functions the agent can use to perform specific tasks. They must be defined with the `@Agent.tool` decorator and include **typing** and **descriptive comments** to help the model understand their purpose and use.

### Simple Tool Example

```python
from apeagent import Agent
from typing import Dict

@Agent.tool
def add(x: float, y: float) -> Dict[str, float]:
    """Adds two numbers and returns the result."""
    return {"result": x + y}
```

### Basic Agent Configuration

```python
calculator_agent = Agent(
    name="Calculator",
    instructions="You are an agent that can perform simple mathematical operations.",
    functions=[add],
    model="gpt-4o",
    temperature=0.0
)
```

## Advanced Example: Multi-Agent System with Hierarchy

### Tool for Weather Consultation

```python
@Agent.tool
def get_weather(city: str) -> Dict[str, str]:
    """Provides current weather information for a specific city using the OpenWeather API."""
    # Weather query implementation...
    ...
```

### Configuring Specialized Agents and Main Agent

```python
weather_agent = Agent(
    name="Weather_Agent",
    instructions="You are an agent specialized in providing weather information.",
    functions=[get_weather],
    model="gpt-4o",
    temperature=0.0
)

main_agent = Agent(
    name="Main_Agent",
    instructions="You are a versatile assistant that can: 1. Provide weather information. 2. Perform mathematical operations.",
    functions=[weather_agent, calculator_agent],
    model="gpt-4o",
    temperature=0.5,
    parallel_tool_calls=True,
    memory_enabled=True,
    memory_max_conversations=40,
    debug=True
)
```

## Using the Main Agent

```python
weather_query = "What's the weather like in Barcelona?"
weather_response = main_agent.call(weather_query)
print("Agent (weather):", weather_response)

add_query = "Add 7 and 5"
add_response = main_agent.call(add_query)
print("Agent (addition):", add_response)
```

## Output Example

```
Agent (weather): The temperature in Barcelona is 20°C with clear skies.
Agent (addition): The result is 12.
```
