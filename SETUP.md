# C4GT Website Setup Guide

A Flask web application with MySQL database and MinIO storage for spreadsheet management.

## Prerequisites

- Python 3.8+
- Docker & Docker Compose (for containerized setup)
- PHP 7.4+ with Composer (for Excel functionality)
- Git

## Quick Start (Dockerized - Recommended)

### 1. Clone Repository
```bash
git clone https://github.com/rohansen856/c4gt-website
cd c4gt-website
```

### 2. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` with your values:
```bash
# Secret key for your app (Flask, Django, etc.)
SECRET_KEY="supersecretkey123"

# MySQL database connection details
MYSQL_HOST="db"
MYSQL_DATABASE="mydatabase"
MYSQL_USER="root"
MYSQL_PASSWORD="password"

# SQLAlchemy URI format: mysql+pymysql://user:password@host/database
SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:password@db/mydatabase"
SQLALCHEMY_TRACK_MODIFICATIONS="False"

# Application title (for frontend use maybe)
APP_TITLE="My Dockerized App"

# MinIO Configuration
MINIO_ENDPOINT="http://localhost:9000"
MINIO_ACCESS_KEY="minioadmin"
MINIO_SECRET_KEY="minioadmin"
MINIO_BUCKET_NAME="c4gt-storage"
# MinIO Docker Configuration
MINIO_ROOT_USER="minioadmin"
MINIO_ROOT_PASSWORD="minioadmin"
```

### 3. Start Services
```bash
docker-compose up -d
```

This starts:
- MySQL database on port 3306
- MinIO storage on ports 9000 (API) and 9001 (Console)

### 4. Install Python Dependencies
```bash
python3 -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

### 5. Run Application
```bash
python main.py
```

Visit http://localhost:5000

## Manual Setup (Non-Dockerized)

### 1. Install MySQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# macOS
brew install mysql

# Start MySQL service
sudo service mysql start  # Linux
brew services start mysql  # macOS
```

### 2. Create Database
```bash
mysql -u root -p
CREATE DATABASE c4gt_db;
exit
```

### 3. Install MinIO (Optional - for local storage)
```bash
# Download MinIO server
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/

# Start MinIO server
mkdir ~/minio-data
minio server ~/minio-data --console-address ":9001"
```

### 4. Environment Setup
Follow steps 2, 4, 5, and 6 from the dockerized setup above.

Update your `.env` file with actual database connection details:
```bash
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your-actual-password
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:your-actual-password@localhost:3306/c4gt_db
```

## Development Notes

- **Database Access**: Available via `g.handler.db` in route handlers
- **Excel Processing**: Requires PHP with PHPSpreadsheet library
- **File Storage**: Uses MinIO for cloud storage (S3-compatible)
- **Frontend**: Built with SocialCalc spreadsheet library

## Troubleshooting

### Common Issues

**Database Connection Error**
- Verify MySQL is running
- Check database credentials in `.env`
- Ensure database exists

**PHP/Excel Import Not Working**
- Install Composer dependencies in `excelinterop/`
- Ensure PHP is accessible from Python subprocess

**MinIO Connection Issues**
- Check MinIO server is running on ports 9000/9001
- Verify MINIO_* environment variables

**Port Already in Use**
- Change ports in `docker-compose.yml`
- Kill processes using required ports

### Logs
- Application logs: Check terminal output
- Docker logs: `docker-compose logs -f`
- MySQL logs: `docker-compose logs mysql-db`

## Production Deployment

Use Gunicorn for production:
```bash
gunicorn main:app --bind 0.0.0.0:8000
```

Configure nginx reverse proxy for static files and SSL termination.