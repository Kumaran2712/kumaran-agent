# 🤖 KumaranCage - AI Agent with Chain-of-Thought Reasoning

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991.svg)

An intelligent CLI agent that transparently solves complex tasks using chain-of-thought prompting and autonomous tool execution.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Examples](#-examples)

</div>

---

## ✨ Features

- 🧠 **Transparent Reasoning**: Watch the AI think through problems step-by-step
- 🔧 **Tool Integration**: Built-in weather API and system command execution
- 💬 **Multi-turn Conversations**: Maintains context across follow-up questions
- 🎨 **Beautiful CLI**: Color-coded output for different reasoning stages
- 🔌 **Extensible**: Easy to add custom tools and capabilities
- 📦 **Installable**: Works as a global CLI command

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Option 1: Install from GitHub (Recommended)
```bash
pip install git+https://github.com/yourusername/kumaran-agent.git
```

### Option 2: Install from Source
```bash
git clone https://github.com/Kumaran2712/kumaran-agent.git
cd kumaran-agent
pip install -e .
```

### Option 3: Run Without Installing
```bash
git clone https://github.com/Kumaran2712/kumaran-agent.git
cd kumaran-agent
pip install -r requirements.txt
python3 agent.py
```

## 🔑 Configuration

Create a `.env` file in your working directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Or set it as an environment variable:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

## 💻 Usage

After installation, simply run:
```bash
kumaran-agent
```

### Commands

- Type your query and press Enter
- Type `exit`, `quit`, or `q` to quit the agent

## 📚 Examples

### Example 1: Mathematical Reasoning
```
👉🏻 What is 15% of 240?

🔥 User has asked to calculate 15% of 240

🗓️  I need to calculate the percentage
🗓️  15% means 15/100 = 0.15
🗓️  Multiply 240 by 0.15
🗓️  240 × 0.15 = 36

✅ 15% of 240 is 36
```

### Example 2: Weather Information
```
👉🏻 What's the weather in Tokyo?

🔥 User wants weather information for Tokyo

🗓️  I'll use the get_weather tool
🛠️  get_weather(Tokyo)
📊 Result: Exit code: 0
Output: The current weather in Tokyo is: Clear ☀️ +18°C

✅ The current weather in Tokyo is clear and sunny at 18°C
```

### Example 3: System Commands
```
👉🏻 Create a new directory called "projects"

🔥 User wants to create a directory

🗓️  I'll use the run_cmd tool to create the directory
🛠️  run_cmd(mkdir projects)
📊 Result: Exit code: 0
Output: 

✅ Successfully created directory 'projects'
```

### Example 4: Multi-step Reasoning
```
👉🏻 I need to know the weather in Paris and London, then tell me which is warmer

🔥 User wants to compare weather in two cities

🗓️  First, I'll check Paris weather
🛠️  get_weather(Paris)
📊 Result: The current weather in Paris is: Clear ☀️ +22°C

🗓️  Now checking London weather
🛠️  get_weather(London)
📊 Result: The current weather in London is: Cloudy ☁️ +16°C

🗓️  Comparing temperatures: Paris (22°C) vs London (16°C)

✅ Paris is warmer at 22°C compared to London at 16°C. 
   The temperature difference is 6°C.
```

## 🏗️ Architecture

### Chain-of-Thought Process

The agent follows a structured reasoning pipeline:
```
┌─────────┐
│  START  │  Parse user intent
└────┬────┘
     │
     ▼
┌─────────┐
│  PLAN   │  Break down into steps (can loop)
└────┬────┘
     │
     ▼
┌─────────┐
│  TOOL   │  Execute tools if needed (optional)
└────┬────┘
     │
     ▼
┌─────────┐
│ OBSERVE │  Process tool results (optional)
└────┬────┘
     │
     ▼
┌─────────┐
│ OUTPUT  │  Deliver final answer
└─────────┘
```

### System Components

- **Agent Core**: Main reasoning loop with conversation state management
- **Tool System**: Modular tool registry for easy extension
- **Structured Output**: Pydantic models ensure consistent JSON responses
- **Color-coded CLI**: Enhanced user experience with visual feedback

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| LLM | OpenAI GPT-4o-mini |
| Structured Output | Pydantic V2 |
| Command Execution | Python subprocess |
| Environment Config | python-dotenv |
| HTTP Requests | requests |

## 🔧 Available Tools

### Current Tools

- **get_weather(city: str)**: Fetches current weather for any city
- **run_cmd(cmd: str)**: Executes shell commands with output capture

### Adding Custom Tools

Extend functionality by adding new tools to `agent.py`:
```python
def your_custom_tool(param: str):
    """Your tool description"""
    # Your implementation
    return result

# Register the tool
available_tools = {
    "get_weather": get_weather,
    "run_cmd": run_cmd,
    "your_custom_tool": your_custom_tool,  # Add here
}

# Update SYSTEM_PROMPT with tool description
```

## 📊 How It Works

### 1. Chain-of-Thought Prompting

The agent uses explicit reasoning steps instead of jumping to conclusions:
- Increases transparency
- Enables debugging of AI logic
- Improves accuracy for complex tasks

### 2. Structured Outputs

Pydantic models enforce consistent JSON responses:
```python
class MyOutputFormat(BaseModel):
    step: str  # START, PLAN, OUTPUT, TOOL, OBSERVE
    content: Optional[str]
    tool: Optional[str]
    input: Optional[str]
```

### 3. Tool Orchestration

Dynamic tool selection and execution based on task requirements:
- Agent decides which tools to use
- Observes tool outputs
- Incorporates results into reasoning

## 🔮 Future Improvements

- [ ] **Sandboxed Execution**: Docker containers for safer command execution
- [ ] **File Operations**: Dedicated tools for create/read/modify files
- [ ] **Web Search**: Integration with search APIs for real-time information
- [ ] **Memory System**: Persistent context across sessions
- [ ] **Domain-Specific Tools**: Chemistry calculations, data analysis, etc.
- [ ] **Streaming Output**: Real-time token streaming for better UX
- [ ] **Error Recovery**: Automatic retry logic for failed operations
- [ ] **Logging**: Comprehensive conversation and tool execution logs

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions

- Add new tools (web scraping, database queries, file operations)
- Improve error handling
- Add unit tests
- Enhance documentation
- Create example use cases



## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini API
- wttr.in for weather data
- Piyush Sir(https://x.com/piyushgarg_dev)
- The open-source community

## 👨‍💻 Author

**Kumaran Sundarrajan**


- GitHub: [@kumaran2712](https://github.com/Kumaran2712)
- LinkedIn: [Kumaran S](https://www.linkedin.com/in/kumaran-sundarrajan96/)
-Twitter: [@Here_To_Code](https://x.com/Here_To_Code)
- Email: kumaran271296@gmail.com

## 📖 Learn More



### Blog Posts

- Coming soon: "Building an AI Agent with Chain-of-Thought Reasoning"

---

<div align="center">

**Built with ❤️ to explore autonomous agents and reasoning patterns**

⭐ Star this repo if you find it useful!

</div>