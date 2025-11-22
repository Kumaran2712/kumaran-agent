import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import Field
from typing import Optional
import os
import subprocess

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GOLD = "\033[38;5;214m"
    GRAY = "\033[90m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"

def print_banner():
    """Display the startup banner"""
    print(f"""{Colors.BOLD}{Colors.GOLD}
_|    _|                                                                            _|_|_|                _|          
_|  _|    _|    _|  _|_|_|  _|_|      _|_|_|  _|  _|_|    _|_|_|  _|_|_|      _|          _|_|_|    _|_|_|    _|_|  
_|_|      _|    _|  _|    _|    _|  _|    _|  _|_|      _|    _|  _|    _|    _|        _|    _|  _|    _|  _|_|_|_|
_|  _|    _|    _|  _|    _|    _|  _|    _|  _|        _|    _|  _|    _|    _|        _|    _|  _|    _|  _|      
_|    _|    _|_|_|  _|    _|    _|    _|_|_|  _|          _|_|_|  _|    _|      _|_|_|    _|_|_|    _|_|_|    _|_|_|
{Colors.RESET}""")
    print(f"{Colors.GRAY}   >> Architecting Intelligence. Automating Reality. <<{Colors.RESET}")
    print("\n")

def get_weather(city: str):
    """Get current weather for a city"""
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The current weather in {city} is: {response.text}"
    else:
        return "Sorry, I couldn't retrieve the weather information right now."

def run_cmd(cmd: str):
    """Execute a shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        output = result.stdout + result.stderr
        return f"Exit code: {result.returncode}\nOutput: {output}"
    except Exception as e:
        return f"Error running command: {str(e)}"

available_tools = {
    "get_weather": get_weather,
    "run_cmd": run_cmd
}

SYSTEM_PROMPT = """
You are an expert AI Assistant in resolving user queries using chain of thoughts.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give and OUTPUT.
You can call a tool if required from the available list of tools.
For every tool call, you need to use the TOOL step to invoke the tool and then wait for the OBSERVE step to get the tool output.

Rules:
1. Strictly follow the given JSON output format.
2. Only run one step at a time.
3. The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and  finally OUTPUT(which is going to be displayed to the user).

OUTPUT JSON Format:
{"step": "START" | "PLAN" | "OUTPUT" | "TOOL,
"content": "string", "tool":"string","input":"string"}

Available Tools:
-get_weather(city:str): Takes a city name as input string and returns the current weather information for that city.
- run_cmd (cmd: str): Takes a command as input string and runs it on the local system and returns the output from that command.

Example 1:
Q:Hey, can you solve 2+3*5/10?
START: {"step": "START", "content": "User has asked to solve a math problem 2+3*5/10"}
PLAN: {"step": "PLAN", "content": "Seems like user is interested in math problem"}
PLAN: {"step": "PLAN", "content": "According to BODMAS, first I need to do multiplication and division before addition."}
PLAN: {"step": "PLAN", "content": "So first I will do 3*5=15"}
PLAN: {"step": "PLAN", "content": "Next I will do 15/10=1.5"}
PLAN: {"step": "PLAN", "content": "Finally I will do 2+1.5=3.5"}
OUTPUT: {"step": "OUTPUT", "content": "The final answer is 3.5"}

Example 2:
Q:What is the weather of Delhi?
START: {"step": "START", "content": "User has asked about the weather of Delhi"}
PLAN: {"step": "PLAN", "content": "Lets see if any tool is available in the list of available tools"}
PLAN: {"step": "PLAN", "content": "Great! get_weather tool is available to get the weather information"}
PLAN: {"step": "TOOL","tool":"get_weather, "input": "Invoking get_weather tool with Delhi as input"}
PLAN: {"step": "OBSERVE","tool":"get_weather", "content": "The current weather in Delhi is: Sunny +30°C"}
PLAN: {"step": "PLAN", "content": "Based on the tool output, I can now prepare the final answer for the user"}
OUTPUT: {"step": "OUTPUT", "content": "The current weather in Delhi is: Sunny +30°C"}
"""

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Examples: START, PLAN, OUTPUT, TOOL, OBSERVE")
    content: Optional[str] = Field(None, description="The content of the step.")
    tool: Optional[str] = Field(None, description="The tool to be called, if step is TOOL.")
    input: Optional[str] = Field(None, description="The input to the tool, if step is TOOL.")

def main():
    """Main entry point for the agent"""
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{Colors.BOLD}Error: OPENAI_API_KEY not found in environment variables.{Colors.RESET}")
        print("Please create a .env file with your OpenAI API key.")
        return
    
    print_banner()
    
    client = OpenAI()
    
    message_history = [
        {"role": "system", "content": SYSTEM_PROMPT}, 
    ]

    while True:
        user_query = input("\n👉🏻 ")
        
        if user_query.lower() in ['exit', 'quit', 'q']:
            print(f"\n{Colors.GOLD}Goodbye!{Colors.RESET}\n")
            break
        
        message_history.append({"role": "user", "content": user_query})

        while True:
            response = client.chat.completions.parse(
                model="gpt-4o-mini",
                response_format=MyOutputFormat,
                messages=message_history
            )

            parsed_result = response.choices[0].message.parsed
            message_history.append({"role": "assistant", "content": json.dumps(parsed_result.model_dump())})
            
            if parsed_result.step == "START":
                print("\n")
                print(f"{Colors.MAGENTA}🔥 {parsed_result.content}{Colors.RESET}")
                print("\n")
                continue

            if parsed_result.step == "TOOL":
                tool_to_call = parsed_result.tool
                tool_input = parsed_result.input
                print(f"{Colors.BLUE}🛠️  {tool_to_call}({tool_input}){Colors.RESET}")
                tool_response = available_tools[tool_to_call](tool_input)
                print(f"{Colors.BLUE}📊 Result: {tool_response}{Colors.RESET}")
                message_history.append({"role": "developer",
                    "content": json.dumps(
                        {"step": "OBSERVE",
                        "tool": tool_to_call,
                        "content": tool_response}
                    )})
                continue

            if parsed_result.step == "PLAN":
                print(f"{Colors.CYAN}🗓️  {parsed_result.content}{Colors.RESET}")
                continue
                
            if parsed_result.step == "OUTPUT":
                print(f"\n{Colors.GREEN}✅ {parsed_result.content}{Colors.RESET}\n")
                break

    print("\n\n\n")

if __name__ == "__main__":
    main()