#!/usr/bin/env python3
"""
Ollama Web Search - A sophisticated web search assistant
Powered by Ollama and SearxNG for intelligent information retrieval
"""

import ollama
import requests
import json
import time
import sys
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse
import argparse

# Configuration
def load_config():
    """Load configuration from file with fallback to defaults"""
    default_config = {
        'model': 'llama3',
        'searxng_instances': [
            'https://search.inetol.net/search',
            'https://searx.be/search',
            'https://search.brave4u.com/search',
            'https://priv.au/search'
        ],
        'max_results': 8,
        'timeout': 10,
        'max_retries': 3,
        'history_file': 'search_history.json',
        'enable_colors': True,
        'streaming_delay': 0.02
    }
    
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
    except Exception as e:
        print(f"Warning: Could not load config.json, using defaults: {e}")
    
    return default_config

CONFIG = load_config()

class Colors:
    """ANSI color codes for beautiful terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        return f"{color}{text}{Colors.END}"

class WebSearchAssistant:
    def __init__(self):
        self.search_history = self.load_history()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def print_banner(self):
        """Display a beautiful welcome banner"""
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    🔍 OLLAMA WEB SEARCH 🔍                    ║
║              Intelligent Information Retrieval               ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.YELLOW}✨ Features:{Colors.END}
• 🧠 AI-powered query optimization
• 🌐 Multiple search engine fallbacks  
• 📄 Smart content extraction
• 💾 Search history tracking
• 🎨 Beautiful terminal interface

"""
        print(banner)

    def model_response(self, model: str, message: str, max_retries: int = 3) -> Optional[str]:
        """Get response from Ollama model with error handling"""
        for attempt in range(max_retries):
            try:
                response = ollama.chat(model=model, messages=[{
                    'role': 'user',
                    'content': message,
                }])
                return response['message']['content']
            except Exception as e:
                print(f"{Colors.RED}⚠️  Attempt {attempt + 1} failed: {str(e)}{Colors.END}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"{Colors.RED}❌ Failed to get model response after {max_retries} attempts{Colors.END}")
                    return None

    def streaming_model_response(self, model: str, message: str) -> str:
        """Stream model response with typing effect"""
        response = ""
        try:
            print(f"{Colors.GREEN}🤖 Assistant:{Colors.END}", end=" ")
            for chunk in ollama.chat(model=model, messages=[{
                'role': 'user',
                'content': message,
            }], stream=True):
                content = chunk['message']['content']
                print(content, end='', flush=True)
                response += content
                time.sleep(CONFIG.get('streaming_delay', 0.02))  # Slight delay for better reading experience
            print()  # New line after streaming
            return response
        except Exception as e:
            print(f"\n{Colors.RED}❌ Error during streaming: {str(e)}{Colors.END}")
            return ""

    def retrieve_page_information(self, url: str) -> Optional[str]:
        """Retrieve and clean webpage content using Jina Reader API"""
        try:
            print(f"{Colors.BLUE}📄 Extracting content from webpage...{Colors.END}")
            
            # Clean URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            base_url = "https://r.jina.ai/"
            response = self.session.get(
                base_url + url, 
                timeout=CONFIG['timeout'],
                headers={'Accept': 'text/plain'}
            )
            response.raise_for_status()
            
            content = response.text.strip()
            if len(content) > 10000:  # Limit content size
                content = content[:10000] + "\n... (content truncated)"
                
            return content
            
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to retrieve page content: {str(e)}{Colors.END}")
            return None

    def browse_web(self, query: str) -> Optional[List[Dict]]:
        """Search the web using multiple SearxNG instances with fallback"""
        print(f"{Colors.BLUE}🔍 Searching the web for: {Colors.BOLD}{query}{Colors.END}")
        
        for instance in CONFIG['searxng_instances']:
            try:
                search_url = f"{instance}?q={query}&format=json&categories=general"
                
                response = self.session.get(search_url, timeout=CONFIG['timeout'])
                response.raise_for_status()
                
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    print(f"{Colors.GREEN}✅ Found {len(results)} results{Colors.END}")
                    return results[:CONFIG['max_results']]
                    
            except Exception as e:
                print(f"{Colors.YELLOW}⚠️  Search instance failed, trying next...{Colors.END}")
                continue
                
        print(f"{Colors.RED}❌ All search instances failed{Colors.END}")
        return None

    def save_search_to_history(self, query: str, question: str, result: Dict):
        """Save search to history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'query': query,
            'result': result
        }
        
        self.search_history.append(entry)
        
        # Keep only last 50 searches
        if len(self.search_history) > 50:
            self.search_history = self.search_history[-50:]
            
        try:
            with open(CONFIG['history_file'], 'w') as f:
                json.dump(self.search_history, f, indent=2)
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Could not save history: {e}{Colors.END}")

    def load_history(self) -> List[Dict]:
        """Load search history"""
        try:
            if os.path.exists(CONFIG['history_file']):
                with open(CONFIG['history_file'], 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []

    def show_history(self):
        """Display recent search history"""
        if not self.search_history:
            print(f"{Colors.YELLOW}📝 No search history found{Colors.END}")
            return
            
        print(f"\n{Colors.CYAN}📚 Recent Search History:{Colors.END}")
        print("═" * 60)
        
        for i, entry in enumerate(self.search_history[-10:], 1):  # Show last 10
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%m/%d %H:%M')
            print(f"{Colors.PURPLE}{i:2d}.{Colors.END} [{timestamp}] {entry['question'][:50]}...")

    def generate_search_query(self, question: str) -> Optional[str]:
        """Generate optimized search query from user question"""
        prompt = """You are an expert at creating precise web search queries. Convert the user's question into an optimal search query that will find the most relevant results.

Guidelines:
- Use specific keywords and terms
- Remove unnecessary words like "what", "how", "can you"
- Include important context
- Keep it concise but comprehensive

Examples:
Question: "What is the capital of France?"
Query: capital France

Question: "How do I install Docker on Ubuntu?"
Query: install Docker Ubuntu tutorial

Question: "What are the latest developments in AI?"
Query: latest AI developments 2024

User's question: """ + question

        print(f"{Colors.BLUE}🧠 Optimizing search query...{Colors.END}")
        return self.model_response(CONFIG['model'], prompt)

    def select_best_result(self, question: str, query: str, results: List[Dict]) -> Optional[Tuple[str, str]]:
        """Let AI select the most relevant search result"""
        results_text = "\n".join([
            f"{i+1}. {result.get('title', 'No title')} - {result.get('url', 'No URL')}\n   {result.get('content', 'No description')[:200]}..."
            for i, result in enumerate(results)
        ])
        
        prompt = f"""You are an expert at evaluating search results. Based on the original question, select the MOST RELEVANT result.

Original Question: {question}
Search Query: {query}

Search Results:
{results_text}

Respond with ONLY the title and URL in this exact format:
Title: [exact title from results]
URL: [exact URL from results]"""

        print(f"{Colors.BLUE}🎯 AI is selecting the best result...{Colors.END}")
        response = self.model_response(CONFIG['model'], prompt)
        
        if not response:
            return None
            
        try:
            lines = [line.strip() for line in response.strip().split('\n') if line.strip()]
            title = next((line.split(':', 1)[1].strip() for line in lines if line.startswith('Title:')), None)
            url = next((line.split(':', 1)[1].strip() for line in lines if line.startswith('URL:')), None)
            
            if title and url:
                return title, url
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Error parsing result selection: {e}{Colors.END}")
            
        # Fallback to first result
        if results:
            return results[0].get('title', 'Unknown'), results[0].get('url', '')
        return None

    def generate_final_answer(self, question: str, query: str, title: str, content: str) -> None:
        """Generate comprehensive answer based on retrieved content"""
        prompt = f"""You are a knowledgeable assistant providing accurate information based on web content.

Original Question: {question}
Search Query: {query}
Source: {title}

Retrieved Content:
{content}

Instructions:
- Provide a comprehensive but concise answer to the user's question
- Use information from the retrieved content
- Cite specific details when relevant
- If the content doesn't fully answer the question, mention what information is available
- Format your response clearly with bullet points or sections when appropriate
- Be helpful and informative"""

        print(f"\n{Colors.PURPLE}{'='*60}{Colors.END}")
        self.streaming_model_response(CONFIG['model'], prompt)
        print(f"{Colors.PURPLE}{'='*60}{Colors.END}")

    def interactive_search(self):
        """Main interactive search function"""
        while True:
            try:
                print(f"\n{Colors.CYAN}💭 What would you like to know?{Colors.END}")
                print(f"{Colors.WHITE}(Type 'history' to see recent searches, 'config' to see settings, 'quit' to exit){Colors.END}")
                
                question = input(f"{Colors.GREEN}❓ Your question: {Colors.END}").strip()
                
                if not question:
                    continue
                    
                if question.lower() in ['quit', 'exit', 'q']:
                    print(f"{Colors.YELLOW}👋 Thank you for using Ollama Web Search!{Colors.END}")
                    break
                    
                if question.lower() == 'history':
                    self.show_history()
                    continue
                    
                if question.lower() == 'config':
                    self.show_config()
                    continue
                
                if question.lower() == 'config':
                    self.show_config()
                    continue
                
                # Generate optimized search query
                search_query = self.generate_search_query(question)
                if not search_query:
                    print(f"{Colors.RED}❌ Failed to generate search query{Colors.END}")
                    continue
                
                print(f"{Colors.GREEN}🔍 Search Query: {Colors.BOLD}{search_query}{Colors.END}")
                
                # Search the web
                results = self.browse_web(search_query)
                if not results:
                    print(f"{Colors.RED}❌ No search results found{Colors.END}")
                    continue
                
                # Select best result
                result = self.select_best_result(question, search_query, results)
                if not result:
                    print(f"{Colors.RED}❌ Could not select a result{Colors.END}")
                    continue
                    
                title, url = result
                print(f"\n{Colors.GREEN}📌 Selected: {Colors.BOLD}{title}{Colors.END}")
                print(f"{Colors.BLUE}🔗 URL: {url}{Colors.END}")
                
                # Retrieve page content
                content = self.retrieve_page_information(url)
                if not content:
                    print(f"{Colors.RED}❌ Could not retrieve page content{Colors.END}")
                    continue
                
                # Save to history
                self.save_search_to_history(search_query, question, {
                    'title': title, 
                    'url': url
                })
                
                # Generate final answer
                self.generate_final_answer(question, search_query, title, content)
                
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.END}")
                break
            except Exception as e:
                print(f"{Colors.RED}❌ Unexpected error: {str(e)}{Colors.END}")

    def show_config(self):
        """Display current configuration settings"""
        print(f"\n{Colors.CYAN}⚙️  Current Configuration:{Colors.END}")
        print("═" * 50)
        print(f"{Colors.BLUE}Model:{Colors.END} {CONFIG['model']}")
        print(f"{Colors.BLUE}Max Results:{Colors.END} {CONFIG['max_results']}")
        print(f"{Colors.BLUE}Timeout:{Colors.END} {CONFIG['timeout']}s")
        print(f"{Colors.BLUE}Search Engines:{Colors.END} {len(CONFIG['searxng_instances'])} instances")
        print(f"{Colors.BLUE}History File:{Colors.END} {CONFIG['history_file']}")
        print(f"{Colors.BLUE}Colors Enabled:{Colors.END} {CONFIG['enable_colors']}")
        print("═" * 50)

def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description='Ollama Web Search Assistant')
    parser.add_argument('--model', default=CONFIG['model'], help=f'Ollama model to use (default: {CONFIG["model"]})')
    parser.add_argument('--query', help='Direct query instead of interactive mode (e.g., --query "What is Python?")')
    parser.add_argument('--history', action='store_true', help='Show search history and exit')
    parser.add_argument('--config', action='store_true', help='Show current configuration and exit')
    
    args = parser.parse_args()
    
    # Update config with command line arguments if explicitly provided
    if args.model != CONFIG['model']:  # Only update if user explicitly provided a different model
        CONFIG['model'] = args.model
    
    assistant = WebSearchAssistant()
    
    if args.history:
        assistant.show_history()
        return
        
    if args.config:
        assistant.show_config()
        return
    
    assistant.print_banner()
    
    # Check if Ollama is available
    try:
        ollama.list()
        print(f"{Colors.GREEN}✅ Ollama connection successful{Colors.END}")
        print(f"{Colors.BLUE}🤖 Using model: {Colors.BOLD}{CONFIG['model']}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Cannot connect to Ollama: {e}{Colors.END}")
        print(f"{Colors.YELLOW}💡 Make sure Ollama is running: ollama serve{Colors.END}")
        return
    
    if args.query:
        # Single query mode
        print(f"{Colors.CYAN}🔍 Single query mode: {args.query}{Colors.END}")
        try:
            # Generate optimized search query
            search_query = assistant.generate_search_query(args.query)
            if not search_query:
                print(f"{Colors.RED}❌ Failed to generate search query{Colors.END}")
                return
            
            print(f"{Colors.GREEN}🔍 Search Query: {Colors.BOLD}{search_query}{Colors.END}")
            
            # Search the web
            results = assistant.browse_web(search_query)
            if not results:
                print(f"{Colors.RED}❌ No search results found{Colors.END}")
                return
            
            # Select best result
            result = assistant.select_best_result(args.query, search_query, results)
            if not result:
                print(f"{Colors.RED}❌ Could not select a result{Colors.END}")
                return
                
            title, url = result
            print(f"\n{Colors.GREEN}📌 Selected: {Colors.BOLD}{title}{Colors.END}")
            print(f"{Colors.BLUE}🔗 URL: {url}{Colors.END}")
            
            # Retrieve page content
            content = assistant.retrieve_page_information(url)
            if not content:
                print(f"{Colors.RED}❌ Could not retrieve page content{Colors.END}")
                return
            
            # Save to history
            assistant.save_search_to_history(search_query, args.query, {
                'title': title, 
                'url': url
            })
            
            # Generate final answer
            assistant.generate_final_answer(args.query, search_query, title, content)
            
        except Exception as e:
            print(f"{Colors.RED}❌ Error in single query mode: {str(e)}{Colors.END}")
    else:
        # Interactive mode
        assistant.interactive_search()

if __name__ == "__main__":
    main()
