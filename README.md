# HumanUpdate

**HumanUpdate** is a Django-based platform designed to help people consciously version and improve themselves—just like software—through structured, intentional reflection.

---

## 🚀 Preview

![Dashboard Screenshot](screenshots/dashboard.png)
*Add your own screenshot above!*

---

## ✨ Features

| Feature                | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| User Auth             | Register, login, and secure your account                                     |
| Version Updates       | Create, edit, delete, and reflect on your personal growth                    |
| Dashboard             | See all your updates, motivational quotes, and your current level            |
| Timeline              | Visualize your journey as a vertical timeline                                |
| Profile & Stats       | View your stats, latest update, and analytics                                |
| Leveling System       | Level up as you grow: Seed, Grower, Refiner, Architect, Master Builder       |
| Export                | Download all your updates as PDF or Markdown                                 |
| AI Suggestions        | Get supportive, personalized update ideas from GPT-3.5-turbo                 |
| Dark Mode             | Switch between light and dark themes                                         |
| Toast Notifications   | Get instant feedback for your actions                                        |
| Admin Panel           | Manage everything with Django admin                                          |

---

## 🔗 Quick Links
- [GitHub Issues](https://github.com/denisgoga/HumanUpdate/issues)
- [Live Demo](#) *(add your deployment link here!)*
- [Contributing](#contributing)

---

## 🤖 How to Use the AI Feature
- On the "Add Update" page, click **Ask AI for help**.
- The AI will suggest a version, summary, and highlights for your reflection.
- Click **Copy to form** to use the suggestion, or edit as you wish.
- Powered by OpenAI GPT-3.5-turbo (API key required in `.env`).

---

## 🛠️ Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/denisgoga/HumanUpdate.git
   cd HumanUpdate\ v0.1
   ```
2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
5. **Run migrations**
   ```bash
   python3 manage.py migrate
   ```
6. **Start the development server**
   ```bash
   python3 manage.py runserver
   ```
7. **Access the app**
   - Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🏆 Leveling System
- **Seed**: 1–3 updates
- **Grower**: 4–7 updates
- **Refiner**: 8–12 updates
- **Architect**: 13–20 updates
- **Master Builder**: 21+ updates

---

## 👤 Credits
- **Author:** Denis Goga
- [GitHub](https://github.com/denisgoga/HumanUpdate)
- [LinkedIn](#) *(add your LinkedIn!)*

---

## 📄 License
MIT

---

*This project is a digital foundation for a new era of conscious human growth. Join the movement!* 