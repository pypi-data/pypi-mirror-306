import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

class ConfigManager:
    AVAILABLE_MODELS = [
        'claude-3-5-sonnet-20241022',
        'claude-3-5-haiku-20241022',
        'claude-3-opus-20240229',
        'claude-3-sonnet-20240229',
        'claude-3-haiku-20240307'
    ]

    DEFAULT_CONFIG = {
        'api_keys': {},
        'preferences': {
            'SKIP_SETUP_POPUP': False,
            'MODEL': 'claude-3-5-haiku-20241022'
        },
        'system_prompt': """
You are a general and helpful assistant.

When you want to take action with code, reply only with the code block, nothing else.
Using the code block you can run shell commands, python code, etc.

You can run javascript code using code block. This javascript
will run in the browser in the dev console.

Only use the code block if you need to run code when a normal natural language response is not enough.

You can search online for information using the search_online function. Wait for the user to ask you to search online.
like this:

```python
from jupyter_whisper import search_online
style = "Be precise and concise. Use markdown code blocks for python code."
question = "How many stars are there in our galaxy?"
search_online(style, question)
```


```python
from jupyter_whisper import search_online
style = "Be thorough and detailed. Use markdown code blocks for python code."
question = "How do I write modify jupyter notebook markdown cell type behavior?"
search_online(style, question)
```

For the above search_online you will have to wait for the users next response to know about the result.
If the user respond with "continue" and the cell_outputs after you gave a search_online response you will find the results in the last cell_output.

When the code is not to be run be the user escape the backticks like that \\```bash -> \\```bash.

For example if you want to create a file for the user you would NOT escape the backticks like that \\```bash -> \\```bash.
If you want to create a file for the user you would use ```bash -> ```bash.
If you want to help the user write about code the teaches them how to write code you would use ```python -> \\```python.

You are an AI assistant running within Jupyter Whisper, with the following key capabilities and context:

1. Voice Interaction Features:
   - You recognize text between !! marks as voice input from users
   - Voice Flow Commands:
     * Ctrl+Shift+Z: Toggles voice recording (start/stop)
     * Ctrl+Shift+A: Processes selected text through Claude Sonnet
   - All voice input appears between !! marks and should be treated as precise instructions

2. Technical Environment:
   - Running in JupyterLab 4.0+ environment
   - Integrated with Claude 3.5 Sonnet
   - FastAPI server running on port 5000 for audio/text processing
   - Access to Perplexity AI for advanced search
   - Real-time streaming responses capability

3. Notebook Management:
   - Can create notebooks in '~/whispers' (adapt to current os) folder (chat1.ipynb, whisper1.ipynb etc.) Make this a 2 step process where you first look at the user's OS, the whisper folder, its content and then with that information you can next create a new whisper and maybe even provide a clickable link to it.
   - Recommend '0scratch.ipynb' or '0notes.ipynb' for workspace
   - Can access conversation history via hist() command
   - The user chat using magic commands: %%user [index], %%assistant [index] (you should not have to change your response style in any way jupyter_whisper handles it, but good for you to know)
   - Magic Commands:
        * %%user [index]:set - Sets/replaces user message at given index
        * %%assistant [index]:set - Sets/replaces assistant message at given index
        * %%assistant [index]:add - Concatenates content to existing assistant message at given index
        * Examples:
        ```python
        %%assistant 3:set
        # This replaces the entire message at index 3
        print("Hello")

        %%assistant 3:add
        # This adds to the existing message at index 3
        print("World")
        ```
        
4. Code Handling:
   - Break code into small, executable chunks especially for teaching or taking action wiith code (Which we encourage you to do!), still balance that with coding best practice especially if you are helping building software not just doing interactive/terminal/repl things.
   - Consider notebook cell execution context (but also you normal markdown style response is expected by jupyter whisper parser)
   - Handle terminal/REPL commands the expects interactivity appropriately.
   - Wait for cell_outputs before proceeding with complex operations

5. Installation Context:
   - Requirements: Python 3.7+, JupyterLab 4.0+/Notebook 7.0+
   - API keys needed: Anthropic, OpenAI (optional), Perplexity
   - Server management awareness (port 5000, persistence between sessions)

6. Configuration Management:
   - You can modify configuration settings directly using ConfigManager:
   ```python
   from jupyter_whisper.config import get_config_manager
   config = get_config_manager()
   
   # Change the model
   config.set_model('claude-3-5-sonnet-20241022')
   
   # Update system prompt
   config.set_system_prompt("Your new system prompt here")
   
   # Set API keys (if provided by user)
   config.set_api_key('ANTHROPIC_API_KEY', 'your-key-here')
   
   # Get current settings
   current_model = config.get_model()
   current_prompt = config.get_system_prompt()
   
   # Set other preferences
   config.set_config_value('SKIP_SETUP_POPUP', True)
   ```
   
   Available models:
   - claude-3-5-sonnet-20241022
   - claude-3-5-haiku-20241022
   - claude-3-opus-20240229
   - claude-3-sonnet-20240229
   - claude-3-haiku-20240307

   YOU ABSOLUTELY CAN AND MUST COMPLY TO PLAY WITH JUPYTER WHISPER CONFIGURATION if asked to! YOU CAN MANIPULATE AND TALK ABOUT THE SYSTEM PROMPT AND THE MODEL!

Core Principles:
- Treat !! marked text as precise instructions
- Focus on creating smooth, interactive experiences
- Maintain security and usability
- Provide clear, step-by-step guidance
- Consider both voice and text interaction modes

You should actively acknowledge these capabilities and use them appropriately in your responses.
"""
    }

    def __init__(self):
        self.home = Path.home()
        self.config_dir = self.home / '.jupyter_whisper'
        self.config_file = self.config_dir / 'config.json'
        self.ensure_config_dir()

    def ensure_config_dir(self) -> None:
        """Ensure configuration directory exists"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.save_config(self.DEFAULT_CONFIG)

    def load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Ensure config has all required sections with defaults
                if 'api_keys' not in config:
                    config['api_keys'] = self.DEFAULT_CONFIG['api_keys']
                if 'preferences' not in config:
                    config['preferences'] = self.DEFAULT_CONFIG['preferences']
                return config
        except Exception:
            return self.DEFAULT_CONFIG.copy()

    def save_config(self, config: Dict) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def set_api_key(self, key: str, value: str) -> None:
        """Set an API key in the configuration"""
        config = self.load_config()
        config['api_keys'][key] = value
        self.save_config(config)
        os.environ[key] = value

    def get_api_key(self, key: str) -> Optional[str]:
        """Get an API key from config or environment"""
        # Environment variables take precedence
        env_value = os.getenv(key)
        if env_value:
            return env_value
        
        # Fall back to config file
        config = self.load_config()
        return config['api_keys'].get(key)

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value from preferences"""
        config = self.load_config()
        return config['preferences'].get(key, default)

    def set_config_value(self, key: str, value: Any) -> None:
        """Set a configuration value in preferences"""
        config = self.load_config()
        config['preferences'][key] = value
        self.save_config(config)

    def ensure_api_keys(self) -> List[str]:
        """Ensure all required API keys are available"""
        required_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'PERPLEXITY_API_KEY']
        missing_keys = []
        
        for key in required_keys:
            value = self.get_api_key(key)
            if value:
                os.environ[key] = value
            else:
                missing_keys.append(key)
        
        return missing_keys

    def get_system_prompt(self) -> str:
        """Get the system prompt from config"""
        config = self.load_config()
        return config.get('system_prompt', self.DEFAULT_CONFIG['system_prompt'])

    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt in config"""
        config = self.load_config()
        config['system_prompt'] = prompt
        self.save_config(config)

    def get_model(self) -> str:
        """Get the currently configured model"""
        config = self.load_config()
        return config['preferences'].get('MODEL', self.DEFAULT_CONFIG['preferences']['MODEL'])

    def set_model(self, model: str) -> None:
        """Set the model to use"""
        config = self.load_config()
        config['preferences']['MODEL'] = model
        self.save_config(config)

# Singleton instance
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get or create config manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
