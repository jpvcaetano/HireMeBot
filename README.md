# HireMeBot

An intelligent LinkedIn chatbot that automatically handles recruiter conversations and analyzes job opportunities based on your criteria.

## Features

- 🤖 Automated responses to LinkedIn messages using GPT-4
- 📊 Job opportunity analysis based on custom criteria
- 📝 Conversation history tracking
- 🔔 Desktop notifications for new messages and matching opportunities
- 🎯 Customizable response templates and job preferences
- 🔄 Version control for conversation templates
- 🛡️ SSL certificate handling

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/HireMeBot.git
cd HireMeBot
```

2. Install dependencies:

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

3. Configure your environment:
    - Copy `.env.example` to `.env` and fill in your credentials:
      ```bash
      cp .env.example .env
      ```
    - Copy the job criteria template and customize it:
      ```bash
      cp config/prompts/custom_criteria.py.example config/prompts/custom_criteria.py
      ```

4. Configure your preferences:
    - Edit `config/prompts/custom_criteria.py` with your job preferences
    - Customize conversation templates in `config/prompts/conversation_prompts.py`
    - Adjust job analysis templates in `config/prompts/job_analysis_prompts.py`
    - Configure required job details in `config/prompts/required_job_details.py`

## Usage

Run the bot:

```bash
# Make sure you're in the poetry shell
poetry shell

python main.py
```

The bot will:
- Monitor your LinkedIn messages
- Respond to recruiters automatically
- Analyze job opportunities
- Send desktop notifications for important events
- Store conversation history in JSON format
- Track both incoming and outgoing messages

## Configuration

### Environment Variables

```env
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_linkedin_password
OPENAI_API_KEY=your_openai_api_key
CHECK_INTERVAL=30  # Time between checks in seconds
SELENIUM_TIMEOUT=10
```

### Job Criteria

Edit `config/prompts/custom_criteria.py`:
```python
JOB_CRITERIA = {
    "required_skills": ["Python", "Machine Learning"],
    "preferred_location": ["Remote", "New York"],
    "minimum_experience": 3,
    "minimum_salary": 120000,
    "deal_breakers": ["Required onsite 5 days/week"],
    "preferred_industries": ["Technology", "Finance"]
}
```

### Required Job Details

Edit `config/prompts/required_job_details.py`:
```python
CONVERSATION_CRITERIA = {
    "required_position_info": [
        "Job title",
        "Company name",
        "Location/Remote policy",
        "Salary range",
        "Required experience",
        "Main responsibilities",
        "Tech stack/Required skills"
    ],
    "preferred_communication": [
        "Direct information in messages",
        "No external links in initial contact",
        "Clear job requirements"
    ]
}
```

## Project Structure

```
linkedin-chatbot/
├── config/
│   ├── settings.py           # Configuration settings
│   └── prompts/
│       ├── conversation_prompts.py  # Chat templates
│       ├── job_analysis_prompts.py  # Analysis templates
│       ├── custom_criteria.py       # Your job preferences
│       └── required_job_details.py  # Required job information
├── src/
│   ├── linkedin_client.py    # LinkedIn automation
│   ├── chat_handler.py       # GPT integration
│   ├── message_store.py      # Conversation management
│   ├── job_analyzer.py       # Opportunity analysis
│   └── notifier.py           # Desktop notifications
├── data/
│   └── conversations.json    # Stored conversation history
└── main.py                   # Main application
```

## Security Notes

- Never commit your `.env` file or `custom_criteria.py`
- Keep your LinkedIn credentials and OpenAI API key secure
- Review automated responses before enabling auto-send
- SSL certificate verification can be configured in chat_handler.py

## Disclaimer

This bot is for educational purposes. Be sure to comply with LinkedIn's terms of service and implement appropriate rate limiting.