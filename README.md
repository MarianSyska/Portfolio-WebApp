# Portfolio-WebApp

Personal portfolio and CV website built with **Django 5.1** and **Wagtail CMS 7.2**. Live at [marian-syska.de](https://marian-syska.de).

## Features

- **CV page** - personal information, work experience, education, and a collapsible skills tree
- **Portfolio page** - project grid with images, descriptions, tags, and GitHub links
- **Wagtail CMS admin** - manage CV items, portfolio projects, and referral tokens through a clean UI
- **Responsive design** - Bootstrap 5 with custom SCSS; scroll-triggered animations (Anime.js)

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.1, Wagtail 7.2, Django REST Framework |
| Database | SQLite (dev), MySQL (production) |
| Frontend | Bootstrap 5, SCSS, jQuery, Anime.js |
| Infra | Gunicorn, nginx, GitHub Actions |

## Development Setup

```bash
# Clone and enter the project
git clone https://github.com/your-username/Portfolio-WebApp.git
cd Portfolio-WebApp

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
.\venv\Scripts\Activate    # Windows

# Install dependencies
pip install .

# Compile SCSS to CSS
python compile_scss.py

# Run migrations
python manage.py migrate

# (Optional) Create mock data for development
python manage.py create_mock_database

# Start the dev server
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** — the admin is at `/admin` (default mock credentials: username: `admin` | password: `admin`).

## Production Build

Settings are managed via **django-environ**. Copy the template and fill in your values:

```bash
cp .env.dist .env
# Then edit .env with your production credentials
```

The `.env` file is read automatically by `MySite/settings.py`. Set `USE_SECURE_CONNECTION=True` to enable HTTPS-only settings (secure cookies, SSL redirect, HSTS).

```bash
python compile_scss.py
python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn MySite.wsgi:application
```


## Project Structure

```
Portfolio-WebApp/
├── MySite/                        # Django project package
│   ├── settings.py                # Django settings file
│   ├── templates/                 # base.html, 404.html, 500.html
│   └── static/                    # Global static assets
├── home/                          # Core Django app
│   ├── models/                    # Page models, CV models, portfolio models
│   ├── templates/home/            # Page templates + components
│   ├── static/home/               # SCSS sources, compiled CSS, JS, images, fonts
│   ├── middleware.py              # TokenReferralMiddleware
│   ├── views.py                   # Wagtail SnippetViewSets
│   └── wagtail_hooks.py          # Admin registration
├── media/                         # User-uploaded images
├── requirements.txt               # Python dependencies
├── compile_scss.py                # SCSS compilation script
└── manage.py                      # Django management entry point
```

## Deployment

Trigger the **"Deploy to Production"** workflow manually via GitHub Actions. It SSH's into the DigitalOcean Droplet, pulls the latest code, runs migrations, compiles assets, and restarts the service behind nginx.

## License

Source code is publicly available for viewing and educational reference only. All rights reserved. You may not reproduce, distribute, modify, or use any part of this project without prior written permission.
