<!DOCTYPE html>
<html lang="en">
<body>
  <div class="container">
    <h1 align="center">🔍Ollama Web Search</h1>
    <p align="center">A chatbot that performs web searches and retrieves information based on user queries.</p>
    <h2>Features</h2>
    <ul>
      <li>Generates precise search queries from user questions.</li>
      <li>Retrieves top web search results.</li>
      <li>Extracts and displays relevant information from chosen web pages.</li>
      <li>Supports streaming responses for real-time feedback.</li>
    </ul>
    <h2>Requirements</h2>
    <ul>
      <li>Python 3.x</li>
      <li><code>ollama</code> library</li>
      <li><code>requests</code> library</li>
    </ul>
    <h2>Installation</h2>
    <p>1. Clone the repository:</p>
    <pre><code>git clone https://github.com/&lt;your-username&gt;/ChatBot-WebSearch.git
cd ChatBot-WebSearch
    </code></pre>
    <p>2. Install the required libraries:</p>
    <pre><code>pip install ollama requests
    </code></pre>
    <h2>Usage</h2>
    <p>Run the chatbot:</p>
    <pre><code>python main.py
    </code></pre>
    <p>Enter your query when prompted, and the chatbot will provide web search results and retrieve information from the selected result.</p>
    <h2>Configuration</h2>
    <p>Before running the chatbot, set your SearxNG instance URL in the <code>BrowseWeb</code> function:</p>
    <pre><code>EngineURL = "https://YOUR-SEARXNG-INSTANCE/search?q={query}&format=json".format(query=query)
    </code></pre>
    <p>You can find a list of SearxNG instances <a href="https://searx.space/">here</a> or search for "SearxNG instances" online.</p>
    <h2>Contributing</h2>
    <p>Feel free to open issues or submit pull requests for any enhancements or bug fixes.</p>
    <h2>License</h2>
    <p>This project is licensed under the MIT License.</p>
  </div>
</body>
</html>
