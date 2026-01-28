# SocialCalc Backend Setup Guide

This is a Flask-based spreadsheet backend that integrates MinIO for file storage instead of AWS S3.

## Quick Start (Recommended - Using Docker)

### Step 1: Clone and Navigate to Project
```bash
cd /home/virtualvasu/Desktop/test/c4gt-website-minio-integration-vasu
```

### Step 2: Create Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` file with your desired values (or keep defaults for local development).

### Step 3: Start Docker Services
```bash
docker-compose up -d
```

This starts:
- **MySQL** on `localhost:3306` (for user data, sheets metadata)
- **MinIO** on `localhost:9000` (API) and `localhost:9001` (Web Console)

Verify services are running:
```bash
docker-compose ps
```

### Step 4: Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv env

# Activate it
source env/bin/activate  # On Windows: .\env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: (Optional) Install PHP Dependencies for Excel Import/Export
```bash
cd excelinterop
composer install
cd ..
```

### Step 6: Run the Application
```bash
python main.py
```

The application will start on `http://localhost:5000`

---

## MinIO Console Access

Once running, access MinIO web console at: **http://localhost:9001**

**Default Credentials:**
- Username: `minioadmin`
- Password: `minioadmin`

### First Time Setup:
1. Create a bucket named `c4gt-storage` (or whatever name you set in `.env`)
2. This is where all spreadsheet files will be stored

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home page |
| `/login` | GET, POST | User login |
| `/register` | GET, POST | User registration |
| `/lostpw` | GET, POST | Password recovery |
| `/logout` | GET, POST | User logout |
| `/pwreset` | GET, POST | Password reset |
| `/save` | GET, POST | Save spreadsheet to MinIO |
| `/usersheet` | POST | Manage user sheets |
| `/downloadfile` | POST | Download spreadsheet |
| `/import` | GET, POST | Import Excel files |
| `/htmltopdf` | GET, POST | Convert HTML to PDF |

---

## Troubleshooting

### MySQL Connection Error
```
Error: Access denied for user 'root'@'db'
```
**Solution:** Verify credentials in `.env` match `docker-compose.yml`

### MinIO Connection Error
```
Error: Failed to connect to MinIO
```
**Solution:** 
1. Check if MinIO container is running: `docker-compose logs minio`
2. Verify `MINIO_ENDPOINT` in `.env` is set correctly
3. Ensure bucket exists in MinIO console

### Port Already in Use
```
Error: Address already in use
```
**Solution:** Change ports in `docker-compose.yml` or kill conflicting processes

### PHP Dependencies Not Found
```
Error: PHP/Composer not found when importing Excel
```
**Solution:** 
1. Install PHP 7.4+
2. Install Composer
3. Run `cd excelinterop && composer install`

---

## Project Structure

```
.
├── main.py                 # Flask application entry point
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker services configuration
├── cloud/
│   ├── authenticate/       # User authentication logic
│   └── storage/            # MinIO storage interface (S3-compatible)
├── route_handlers/         # API endpoint handlers
│   ├── Auth/               # Login, register, password handlers
│   ├── SaveHandler.py      # Save spreadsheet to MinIO
│   ├── UserSheetHandler.py # Manage user sheets
│   ├── ImportHandler.py    # Import Excel files
│   └── ...
├── excelinterop/           # PHP/Excel import-export utilities
├── templates/              # HTML templates
└── static/                 # Frontend assets (SocialCalc library)
```

---

## Development Tips

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f mysql-db
docker-compose logs -f minio
```

### Access MySQL Directly
```bash
# From host
mysql -h 127.0.0.1 -u root -p

# From Docker
docker-compose exec db mysql -u root -p
```

### Restart Services
```bash
# Soft restart
docker-compose restart

# Hard restart (removes containers)
docker-compose down
docker-compose up -d
```

### Check MinIO Bucket
```bash
# List buckets and objects via MinIO console
# http://localhost:9001
```

---

## Production Deployment

### Using Gunicorn
```bash
# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

Or use the provided script:
```bash
./run.sh  # Runs 4 instances on ports 8000-8003
```

### Production .env Settings
```bash
FLASK_ENV="production"
FLASK_DEBUG=False
SECRET_KEY="<generate-strong-key>"
SQLALCHEMY_DATABASE_URI="mysql+pymysql://user:password@prod-db-host/c4gt_db"
MINIO_ENDPOINT="https://your-minio-domain"
```

### Nginx Configuration
See [configs/nginx.conf](configs/nginx.conf) for reverse proxy setup.

---

## Key Technologies

- **Backend:** Flask 3.0.3
- **Database:** MySQL 8.0
- **Storage:** MinIO (S3-compatible)
- **ORM:** SQLAlchemy
- **Excel:** PHPSpreadsheet
- **Frontend:** SocialCalc (JavaScript spreadsheet library)
- **PDF Export:** pdfkit + wkhtmltopdf

---

## Support

Refer to individual files for detailed documentation:
- [SETUP.md](SETUP.md) - Original setup guide
- [SECURITY_AUDIT_REPORT.md](SECURITY_AUDIT_REPORT.md) - Security considerations
- [AWS_SERVICES_AUDIT.md](AWS_SERVICES_AUDIT.md) - AWS vs MinIO comparison
