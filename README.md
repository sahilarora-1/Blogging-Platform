# Blogging Platform – Secure & Scalable Django Blog Website

A full-stack blogging platform built with Django, designed with security, scalability, and clean user experience in mind.

This platform allows authenticated users to create, edit, manage, search, and delete blog posts with featured image support, pagination, secure authentication, and production-aware configurations.

---

## Features

### Authentication & User Management
- User signup and login
- Secure logout functionality
- Session-based authentication
- Password hashing using Django's built-in authentication system
- Protected routes using `login_required`

---

## Blog Management (CRUD)
Authenticated users can:

- Create blog posts
- Edit their own blog posts
- Delete their own blog posts
- View published blog posts
- Upload featured images
- Replace images while editing posts
- View blog details with SEO-friendly URLs

---

## Search & Navigation
- Search blogs by title and content
- Homepage pagination
- Dashboard pagination
- Newest posts shown first
- Custom 404 page

---

## Security Features
- CSRF protection
- Authorization checks to prevent unauthorized edits/deletes
- Secret key stored securely using environment variables (`.env`)
- `.gitignore` configured to protect sensitive files
- Delete confirmation prompts
- Backend input validation for required fields
- Protected user-specific dashboard access

---

## Scalability Features
- Modular Django architecture (`accounts`, `posts`)
- Efficient Django ORM queries
- Pagination to reduce database load
- Search implemented using Django `Q` objects
- Slug uniqueness handling for SEO-friendly URLs
- Relational database design using foreign keys

---

## Deployment Considerations
- WhiteNoise configured for static file serving
- Environment-based configuration using `python-decouple`
- Static and media file handling setup
- `requirements.txt` included
- `ALLOWED_HOSTS` configuration awareness

---

## Tech Stack

### Backend
- Python
- Django

### Frontend
- HTML
- CSS
- Django Templates

### Database
- SQLite

### Libraries Used
- Pillow
- WhiteNoise
- python-decouple

---

## Project Structure

```bash
blogsite/
│
├── accounts/
├── posts/
├── templates/
├── static/
├── blogsite/
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation & Setup

### Clone Repository
```bash
git clone https://github.com/sahilarora-1/Blogging-Platform.git
cd blogsite
```

### Create Virtual Environment
```bash
python -m venv env
```

### Activate Virtual Environment

Windows:
```bash
env\Scripts\activate
```

Mac/Linux:
```bash
source env/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Create `.env` File
Create a `.env` file in the root directory:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Start Development Server
```bash
python manage.py runserver
```

Visit:

```bash
http://127.0.0.1:8000/
```

---

## Future Improvements

- Blog categories and tags
- Comment system
- User profile pages
- Cloud storage for media files
- Public deployment

---

## Learning Outcomes
This project helped strengthen my understanding of:

- Django authentication
- Session management
- CRUD architecture
- File uploads
- Django ORM
- Security best practices
- Static and media file handling
- Production-aware configuration management
- Scalable web application design

---

## Author
**Sahil Arora**  


GitHub: https://github.com/sahilarora-1