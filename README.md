# Social Pro Dashboard

A premium content distribution and analytics platform built with **FastAPI** and **Vanilla JS**.

## Features
- **Multi-Platform Publishing**: One-click publishing to Instagram, Facebook, LinkedIn, and YouTube.
- **Live Preview**: Real-time mockup visualization for each platform.
- **Executive Analytics**: Dynamic charts for reach and engagement tracking.
- **Persistence**: Auto-save drafts including media (images/videos) to survive refreshes.
- **Nocturne Glass UI**: High-performance 120fps glassmorphism design.

## Tech Stack
- **Frontend**: HTML5, CSS3 (Tailwind CSS), JavaScript (Vanilla).
- **Backend**: Python 3.10+, FastAPI, Uvicorn.
- **Icons**: Lucide Icons.
- **Charts**: Chart.js.

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd social-pro
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory (refer to the provided template or ask the team for tokens):
```env
# Platform Tokens
INSTAGRAM_TOKEN=your_token
FACEBOOK_TOKEN=your_token
LINKEDIN_TOKEN=your_token
YOUTUBE_TOKEN=your_token

# Platform IPs/Endpoints
INSTAGRAM_IP=api.instagram.com
...
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Backend
```bash
python main.py
```

### 5. Open the Dashboard
Open `index.html` in your favorite browser.

## Contributing
Please ensure you do not commit your `.env` file. It is already included in `.gitignore`.

---
*Built with ❤️ for Social Pro Teams*
