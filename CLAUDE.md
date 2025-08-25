# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
- **Development**: `python main.py` or `python3 main.py`
- **Docker**: `docker-compose up` (requires `.env` file configuration)
- **Production**: `gunicorn main:app` (gunicorn is installed in requirements.txt)

### Environment Setup
- Create virtual environment: `python3 -m venv env`
- Activate virtual environment: `source env/bin/activate` (Linux/Mac) or `.\env\Scripts\activate` (Windows)
- Install dependencies: `pip install -r requirements.txt`
- Configure environment: Copy `.env.example` to `.env` and fill in required values

### Excel Integration Setup
The application includes PHP-based Excel import/export functionality:
```bash
cd excelinterop
composer install
cd ..
```

## Architecture Overview

### Core Application Structure
This is a Flask web application with a modular route handler architecture:

- **main.py**: Entry point and Flask app configuration
- **route_handlers/**: Modular request handlers organized by functionality
  - **Auth/**: Authentication-related handlers (login, register, password reset)
  - **SaveHandler.py**: Spreadsheet save functionality
  - **ImportHandler.py**: File import processing
  - **HTMLToPDFHandler.py**: PDF conversion
- **templates/**: Jinja2 HTML templates
- **static/**: Frontend assets including SocialCalc spreadsheet library
- **cloud/**: AWS integration modules (authentication and storage)

### Database Configuration
- Uses SQLAlchemy ORM with MySQL backend
- Database connection configured via environment variables
- Docker setup includes MySQL 8.0 container

### Key Technologies
- **Backend**: Flask, SQLAlchemy, PyMySQL
- **Frontend**: SocialCalc (JavaScript spreadsheet library), jQuery, Highcharts
- **Authentication**: Session-based with password hashing (passlib)
- **Cloud Storage**: AWS S3 integration (boto3)
- **Excel Processing**: PHP-based with PHPSpreadsheet library
- **PDF Generation**: pdfkit library

### Session Management
The application uses a BaseHandler class providing:
- Database access via `g.handler.db`
- User session management via `get_current_user()` and `set_current_user()`
- Authentication state persisted in Flask sessions

### Development Notes
- The application requires both Python and PHP environments
- Excel import/export functionality bridges Python Flask with PHP processing
- Frontend heavily relies on SocialCalc for spreadsheet functionality
- Cloud integration supports AWS S3 for file storage
- Docker setup provides full-stack development environment with MySQL

### File Structure Highlights
- **excelinterop/**: PHP-based Excel processing with Composer dependencies
- **static/**: Contains extensive JavaScript libraries and SocialCalc implementation
- **configs/**: Nginx configuration for production deployment