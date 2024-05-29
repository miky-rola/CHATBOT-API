## Chatbot API
This project implements a simple chatbot API using Django REST Framework. The chatbot is powered by a GPT-2 model from Hugging Face, providing conversational responses. The API supports user registration, login, chatting with the bot, and viewing conversation history.

### Features
- User Registration and Authentication
- Token-based Authentication
- Chatbot Interaction
- Conversation History Retrieval

### Requirements
- Python 3.8+
- Django 3.2+
- Django REST Framework
- Django REST Framework Authtoken
- Hugging Face Transformers
- Other dependencies listed in requirements.txt

Clone the repository:
`git clone https://github.com/yourusername/chatbot-api.git`

**Create a virtual environment and activate it:**
`python -m venv venv`
`source venv/bin/activate` # On Mac
`venv\Scripts\activate` # On Windows 

Install the dependencies:
`pip install -r requirements.txt`

`python manage.py migrate`

**Create a superuser (optional, for admin access):**
`python manage.py createsuperuser`

Run the development server:
`python manage.py runserver`