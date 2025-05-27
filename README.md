# 🔍 Ollama Web Search

A sophisticated AI-powered web search assistant that combines the intelligence of Ollama with comprehensive web search capabilities.

## ✨ Features

- 🧠 **AI-Powered Query Optimization** - Automatically converts natural language questions into effective search queries
- 🌐 **Multiple Search Engine Fallbacks** - Uses multiple SearxNG instances for reliable search results
- 📄 **Smart Content Extraction** - Retrieves and processes webpage content using Jina Reader API
- 💾 **Search History Tracking** - Automatically saves and manages your search history
- 🎨 **Beautiful Terminal Interface** - Rich colors and formatting for excellent user experience
- ⚡ **Streaming Responses** - Real-time AI responses with typing effect
- 🔧 **Configurable Settings** - Easy customization through config.json
- 🛡️ **Robust Error Handling** - Graceful handling of network issues and API failures

## 🚀 Quick Start

### Installation

1. Clone the repository:

```bash
git clone https://github.com/garyku0/ollama-web-search.git
cd ollama-web-search
```

2. Run the setup script:

```bash
python3 setup.py
```

3. Make sure Ollama is running:

```bash
ollama serve
```

### Usage

**Interactive Mode (Recommended):**

```bash
python3 main.py
```

**View Search History:**

```bash
python3 main.py --history
```

**View Configuration:**

```bash
python3 main.py --config
```

**Single Query Mode:**

```bash
python3 main.py --query "What is Python programming?"
```

**Use Different Model:**

```bash
python3 main.py --model llama2
```

**Get Help:**

```bash
python3 main.py --help
```

## 💡 Example Questions to Try

- "What are the latest developments in artificial intelligence?"
- "How do I install Docker on macOS?"
- "Best practices for Python web development 2025"
- "What is the difference between React and Vue.js?"
- "How to optimize PostgreSQL performance?"

## ⚙️ Configuration

Edit `config.json` to customize settings:

```json
{
  "model": "llama3", // Ollama model to use
  "searxng_instances": [
    // Search engines (fallback order)
    "https://search.inetol.net/search",
    "https://searx.be/search"
  ],
  "max_results": 8, // Number of search results to process
  "timeout": 10, // Request timeout in seconds
  "max_retries": 3, // Retry attempts for failed requests
  "history_file": "search_history.json", // Search history storage
  "enable_colors": true, // Terminal colors
  "streaming_delay": 0.02 // Typing effect speed
}
```

## 🔧 Troubleshooting

**"Cannot connect to Ollama"**

```bash
# Make sure Ollama is running
ollama serve

# Check if your model is available
ollama list

# Pull the model if needed
ollama pull llama3
```

**"All search instances failed"**

- Check your internet connection
- Try updating SearxNG instances in config.json
- Some instances may be temporarily down

**Colors not showing properly**

- Set `"enable_colors": false` in config.json
- Some terminals don't support ANSI colors

## 📊 Search History

Your searches are automatically saved to `search_history.json`:

- View with `python3 main.py --history`
- Or type `history` in interactive mode
- Automatically keeps last 50 searches
- Includes timestamps and results

## 🔒 Privacy & Security

- **Local Processing**: All AI processing happens locally via Ollama
- **No API Keys**: No external AI service API keys required
- **Search Privacy**: Uses privacy-focused SearxNG instances
- **Data Control**: All data stays on your machine

## 🛠️ Requirements

- Python 3.7+
- Ollama (running locally)
- Internet connection
- Required packages (installed via setup.py):
  - `ollama>=0.2.0`
  - `requests>=2.31.0`

## 💡 Tips for Best Results

1. **Be Specific**: More detailed questions get better results
2. **Use Keywords**: Include relevant technical terms
3. **Ask Follow-ups**: Use the interactive mode for related questions
4. **Check History**: Review past searches to avoid duplicates
5. **Experiment with Models**: Try different Ollama models for variety

## 🤝 Contributing

Feel free to open issues or submit pull requests for:

- Bug fixes
- New features
- Documentation improvements
- Additional SearxNG instances
- UI/UX enhancements

## 📄 License

This project is licensed under the MIT License.

[![Star History Chart](https://api.star-history.com/svg?repos=GaryKu0/ollama-web-search&type=Date)](https://www.star-history.com/#GaryKu0/ollama-web-search&Date)
