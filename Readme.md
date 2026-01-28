# SocialCalc Backend - Private Spreadsheet Engine

> A Flask-based backend for the **SocialCalc** enterprise spreadsheet engine, enabling organizations to self-host collaborative spreadsheets on private infrastructure using MinIO and MySQL.

**Developed at:** Code for GovTech | **Status:** Production-Ready

---

## Table of Contents

1. [About This Project](#about-this-project)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Quick Start](#quick-start)
6. [Setup Options](#setup-options)
7. [Access Points](#access-points)
8. [API Endpoints](#api-endpoints)
9. [Troubleshooting](#troubleshooting)

---

## About This Project

**SocialCalc Backend** is a Flask-based backend for the SocialCalc collaborative spreadsheet application—a mature, open-source JavaScript engine with 32,000+ lines of frontend code.

### Why This Project?
- **Private & Secure:** Self-host on your own servers, no cloud dependency
- **User Management:** Multi-user support with authentication & session management
- **Persistent Storage:** All spreadsheet data stored in MinIO (S3-compatible)
- **Rich Features:** Excel import/export, PDF export, real-time editing
- **Enterprise Ready:** Built for organizations requiring data privacy

### Perfect For:
- Government agencies and public sector organizations
- Enterprises with strict data residency requirements
- Teams needing collaborative spreadsheets without cloud storage

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Browser/Client                        │
│         (SocialCalc Frontend - 32k+ JS Lines)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP/REST API
                     │
┌────────────────────┴────────────────────────────────────┐
│              Flask Backend (Python)                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Route Handlers                                  │  │
│  │  - Authentication (Login/Register/Password Reset)│  │
│  │  - Spreadsheet Save/Load                         │  │
│  │  - Excel Import/Export                           │  │
│  │  - HTML to PDF Conversion                        │  │
│  │  - File Download/Upload                          │  │
│  └──────────────────────────────────────────────────┘  │
└────────────┬───────────────────────────┬────────────────┘
             │                           │
    ┌────────┴──────────┐      ┌─────────┴─────────┐
    │   MySQL Database  │      │  MinIO Storage    │
    │                   │      │  (S3-compatible)  │
    │ - User Accounts   │      │                   │
    │ - Auth Tokens     │      │ - Spreadsheet     │
    │ - Metadata        │      │   Files (JSON)    │
    │                   │      │ - User Isolation  │
    └───────────────────┘      └───────────────────┘
```

### Component Breakdown

| Component | Technology | Role |
|-----------|-----------|------|
| **Frontend** | JavaScript (32k+ lines) | Interactive spreadsheet UI, rendered from `static/` folder in browser |
| **Backend API** | Flask 3.0.3 + Python | Route handling, business logic, authentication |
| **Database** | MySQL 8.0 | User accounts, session management, metadata |
| **File Storage** | MinIO (S3-compatible) | Spreadsheet data storage, user file isolation |
| **Excel Support** | PHPSpreadsheet | Import/Export Excel files to/from spreadsheets |
| **PDF Export** | pdfkit | Convert spreadsheet HTML to PDF documents |

---

## Technology Stack

### Backend
- **Framework:** Flask 3.0.3
- **ORM:** SQLAlchemy 2.0.31
- **Server:** Gunicorn 22.0.0
- **Language:** Python 3.8+

### Database & Storage
- **Database:** MySQL 8.0
- **Object Storage:** MinIO (S3-compatible, open-source)
- **Storage Client:** boto3 (AWS SDK for Python)

### Frontend
- **Spreadsheet Library:** SocialCalc (JavaScript, 32k+ lines)
- **Charting:** Highcharts, Sparklines
- **DOM Utilities:** jQuery
- **Data Visualization:** Flot

### Additional Services
- **Excel Operations:** PHPSpreadsheet (PHP 7.4+)
- **Dependency Management:** Composer (for PHP)
- **Containerization:** Docker & Docker Compose
- **Web Server (optional):** Nginx

### Python Dependencies
See [requirements.txt](requirements.txt) for the complete list including:
- Flask & SQLAlchemy for the web framework and ORM
- boto3 for MinIO/S3 compatibility
- PyMySQL for MySQL connections
- passlib for secure password hashing
- pdfkit for PDF generation

---

## Project Structure

```
c4gt-website/
├── main.py                      # Flask application entry point
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Docker services configuration
├── Dockerfile                   # Container image definition
├── .env.example                 # Environment variables template
├── configs/
│   └── nginx.conf              # Nginx configuration (optional)
├── cloud/                       # Cloud infrastructure modules
│   ├── storage/
│   │   └── storage.py          # MinIO S3-compatible client
│   └── authenticate/
│       ├── user.py             # User model and management
│       └── authenticate.py     # Authentication utilities
├── route_handlers/             # Flask route handlers
│   ├── HomeHandler.py          # Home page / dashboard
│   ├── SaveHandler.py          # Save/load spreadsheet
│   ├── UserSheetHandler.py     # Spreadsheet management
│   ├── ImportHandler.py        # Excel import
│   ├── ExportHandler.py        # File download/export
│   ├── HTMLToPDFHandler.py     # PDF conversion
│   └── Auth/                   # Authentication routes
│       ├── UserLoginHandler.py
│       ├── UserRegisterHandler.py
│       ├── UserLostPasswordHandler.py
│       ├── UserLogoutHandler.py
│       └── PWResetHandler.py
├── templates/                  # Jinja2 HTML templates
├── static/                     # Frontend assets
│   ├── socialcalc-3.js        # Main SocialCalc engine (32k+ lines)
│   ├── socialcalcworkbook.js  # Workbook management
│   ├── jquery.min.js          # jQuery library
│   ├── Highcharts-2/          # Charting library
│   └── images/                # Images and assets
├── excelinterop/               # Excel import/export
│   ├── import.py              # Python wrapper
│   ├── import.php             # PHP import logic
│   ├── export.php             # PHP export logic
│   └── composer.json          # PHP dependencies
└── env/                        # Python virtual environment (local dev)
```

### Key Directories Explained

**cloud/storage/** - MinIO/S3-compatible storage operations
- Handles file upload, download, and management
- Uses boto3 to communicate with MinIO
- Organizes files by user: `home/users/{username}/{filename}`

**route_handlers/** - Request processing logic
- Implements MVC-style handlers for each route
- Each handler has `get()` and `post()` methods
- Manages user sessions and authentication

**static/** - Frontend SocialCalc engine
- 32,000+ lines of JavaScript providing the spreadsheet UI
- Automatically loaded in browser and rendered
- Handles all client-side spreadsheet operations
- Communicates with backend via REST API

---

## Quick Start

### Docker Setup (Recommended)

**1. Clone and navigate to project:**
```bash
cd c4gt-website-minio-integration
```

**2. Setup environment:**
```bash
cp .env.example .env
```

**3. Start services:**
```bash
# Stop local MySQL if running (optional)
sudo systemctl stop mysql 2>/dev/null || true

# Start Docker containers
docker compose up -d
```

**4. Setup Python and run app:**
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python main.py
```

**5. Access the application:**
- 🌐 **Spreadsheet:** http://localhost:5000
- 📦 **MinIO Console:** http://localhost:9001 (minioadmin / minioadmin)

---

## Setup Options

### Option A: Docker Setup (Recommended)

Uses Docker containers for MySQL and MinIO. Quickest way to get started.

**Requirements:**
- Docker & Docker Compose installed

**Services started:**
- MySQL on port 3307
- MinIO on ports 9000 (API) and 9001 (Web Console)

See [Quick Start](#quick-start) above.

---

### Option B: Manual Setup (No Docker)

Install services manually on your machine.

**Prerequisites:**
- Python 3.8+
- MySQL 8.0+
- PHP 7.4+ (for Excel import/export)
- Composer (for PHP dependencies)

**Setup steps:**

1. **Install MinIO locally:**
```bash
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/
mkdir ~/minio-data
minio server ~/minio-data --console-address ":9001" &
```

2. **Create MySQL database:**
```bash
mysql -u root -p -e "CREATE DATABASE c4gt_db;"
```

3. **Setup Python environment:**
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

4. **Install PHP dependencies (optional, for Excel):**
```bash
cd excelinterop && composer install && cd ..
```

5. **Configure environment:**

Update `.env` file:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-password
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:your-password@localhost:3306/c4gt_db
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

6. **Run the application:**
```bash
python main.py
```

Access at http://localhost:5000

---

## Access Points

| Service | URL | Default Credentials |
|---------|-----|-----------|
| **Spreadsheet App** | http://localhost:5000 | — |
| **MinIO Console** | http://localhost:9001 | minioadmin / minioadmin |
| **MinIO API** | http://localhost:9000 | minioadmin / minioadmin |
| **MySQL** | localhost:3307 (Docker) / 3306 (Local) | root / {password} |

---

## API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/login` | GET, POST | User login |
| `/register` | GET, POST | Create new account |
| `/logout` | GET, POST | Logout user |
| `/lostpw` | GET, POST | Password recovery |
| `/pwreset` | GET, POST | Reset password |

### Spreadsheet Operations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page / dashboard |
| `/save` | GET, POST | List and save spreadsheets |
| `/usersheet` | POST | Edit/delete spreadsheet |
| `/downloadfile` | POST | Download spreadsheet |

### File Conversion
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/import` | GET, POST | Import Excel files |
| `/htmltopdf` | GET, POST | Export as PDF |

**Storage Path:** `home/users/{username}/{filename}`  
**Data Format:** JSON serialized spreadsheet objects  
**Authentication:** Required for all endpoints except `/login` and `/register`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 3306 already in use** | `sudo systemctl stop mysql` then retry |
| **Docker containers won't start** | Check if services are already running on ports 3307 or 9000 |
| **MinIO bucket missing** | Bucket auto-creates on first app start |
| **PHP/Composer installation fails** | Install Composer from https://getcomposer.org, then run `cd excelinterop && composer install` |

---

## Additional Resources

- [QUICKSTART.md](QUICKSTART.md) - Detailed quickstart guide
- [SETUP.md](SETUP.md) - Complete setup instructions  
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [SECURITY_AUDIT_REPORT.md](SECURITY_AUDIT_REPORT.md) - Security analysis

````
