# AI Agent: Cryptocurrency Price Fetching and Language Translation

This project is an AI assistant built with Streamlit and Together AI API, designed to:
- Fetch real-time cryptocurrency prices
- Handle language translation requests while maintaining English as the response language

## Features
1. **Show Price of Cryptocurrency**: Retrieves the latest price for a specified cryptocurrency.
2. **Change Language of Prompt**: Allows users to change the language for their prompt, which the assistant translates and processes in English.
3. **General Query Regarding Cryptocurrency**: Handles miscellaneous queries related to cryptocurrencies.

## Setup Instructions
1. **Clone the Repository**:
   git clone https://github.com/Shashankm886/AI-Agent-Project.git
   cd AI-Agent-Project
2. **Install Dependencies**:
   Ensure Python 3.8+ is installed, then install the required libraries:
   pip install -r requirements.txt
3. **Configure API Key**:
   Create a config.py file in the root directory with your Together API key:
   TOGETHER_API_KEY = 'your_api_key_here'
4. **Run the Application**:
   streamlit run app.py
  