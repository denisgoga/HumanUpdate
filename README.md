# HumanUpdate

**HumanUpdate** is a Django-based platform designed to help people consciously version and improve themselves—just like software—through structured, intentional reflection.

## Features
- User registration, login, and authentication
- Create, edit, and delete personal "Version Updates" (with version, summary, highlights, and date)
- Dashboard with motivational quotes, leveling system, and progress bar
- Timeline view for visualizing your growth journey
- Profile page with stats and latest update
- Personal analytics (updates per month, most used words, average time between updates, etc.)
- Export all updates as PDF or Markdown
- AI-powered suggestions for summaries and highlights (GPT-4 integration)
- Clean, modern UI with Tailwind CSS

## Leveling System
- **Seed**: 1–3 updates
- **Grower**: 4–7 updates
- **Refiner**: 8–12 updates
- **Architect**: 13–20 updates
- **Master Builder**: 21+ updates

## Getting Started

### 1. Clone the repository
```bash
git clone <repo-url>
cd HumanUpdate\ v0.1
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Start the development server
```bash
python manage.py runserver
```

### 7. Access the app
Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Export & AI Features
- **Export**: On the dashboard, use the "Export My Human Updates" button to download your updates as PDF or Markdown.
- **AI Suggestions**: On the create update page, use "Ask AI for help" to get supportive, personalized suggestions for your reflection.

## Requirements
- Python 3.9+
- Django 4.2+
- Tailwind CSS (via CDN)
- xhtml2pdf, openai, python-dotenv, and other dependencies (see requirements.txt)

## License
MIT

---

*This project is a digital foundation for a new era of conscious human growth. Join the movement!* 