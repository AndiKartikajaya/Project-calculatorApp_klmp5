# 🧮 Calculator-Project - Advanced Calculator Application

## 📋 Deskripsi Singkat

**Calculator-App** adalah aplikasi kalkulator web yang dilengkapi dengan fitur riwayat perhitungan, export data, dan dukungan untuk berbagai jenis operasi matematika. Aplikasi ini dibangun dengan arsitektur modern yang memisahkan frontend dan backend, menggunakan FastAPI untuk backend dan HTML5 dengan JavaScript vanilla untuk frontend. Setiap pengguna dapat melakukan perhitungan, menyimpan riwayat perhitungan, serta mengekspor hasil perhitungan dalam format CSV atau PDF.

## 👥 Daftar Anggota

| No  | Nama                         | NIM         | Username GitHub | Peran/Tugas          |
| --- | ---------------------------- | ----------- | --------------- | -------------------- |
| 1   | Komang Andi Kartikajaya      | [240030339] | AndiKartikajaya | Full Stack Developer |
| 2   | Ni Wayan Intan Trisna Rahayu | [250030625] | AndiKartikajaya | Testing & Debugging  |
| 3   | I Kadek Dawista Lahran       | [240030036] | AndiKartikajaya | Debugging            |
| 4   | Serdi Leni Debora bantaika   | [220030332] | AndiKartikajaya | Tidak ada            |

**Peran/Tugas:**

- Backend Development (FastAPI, Database Design, API Endpoints)
- Frontend Development (HTML5, CSS3, JavaScript)
- Database Management (SQLite, Schema Design)
- Authentication & Authorization (JWT Token)
- Testing & Debugging

## 🛠️ Lingkungan Pengembangan

### Alat dan Teknologi

**Backend:**

- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn 0.24.0
- **Database:** SQLite dengan SQLAlchemy ORM 2.0.23
- **Authentication:** Python-Jose 3.3.0 dengan JWT
- **Password Hashing:** Passlib 1.7.4 dengan BCrypt
- **Validation:** Pydantic 2.5.0
- **Report Generation:** ReportLab 4.0.9

**Frontend:**

- **Markup:** HTML5
- **Styling:** CSS3
- **Scripting:** JavaScript (ES6+)
- **Server:** Python HTTP Server (Port 8080)

**Development Tools:**

- Python 3.10+
- Virtual Environment (venv)
- DB Browser for SQLite 3.13.1

### Requirement Packages

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic==2.5.0
python-dotenv==1.0.0
cryptography==41.0.7
email-validator==2.1.0
reportlab==4.0.9
```

## 💼 Proses Bisnis

### Alur Umum Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                    Calculator Application Flow              │
└─────────────────────────────────────────────────────────────┘

1. USER REGISTRATION & LOGIN
   ├── User membuka aplikasi → halaman login/register
   ├── User membuat akun baru atau login dengan akun lama
   ├── Backend verifikasi credentials dan generate JWT Token
   └── Token disimpan di localStorage browser

2. CALCULATION OPERATIONS
   ├── User memilih jenis kalkulator (Basic/Advanced/Unit/Finance)
   ├── User input nilai dan pilih operasi
   ├── Frontend kirim request ke backend dengan JWT Token
   ├── Backend validasi token → extract user_id
   ├── Backend proses perhitungan
   ├── Backend simpan ke database dengan user_id
   └── Frontend tampilkan hasil perhitungan

3. HISTORY & EXPORT
   ├── User bisa lihat semua perhitungan mereka di halaman History
   ├── Data di-filter berdasarkan user_id (secure)
   ├── User bisa export ke CSV atau PDF
   └── File dihasilkan dengan data user-specific

4. DATA SECURITY
   ├── JWT Token digunakan untuk setiap request
   ├── Password di-hash dengan BCrypt
   ├── Database CASCADE delete untuk data integrity
   └── User hanya bisa akses data mereka sendiri
```

### Modul-Modul Utama

1. **Authentication Module**
   - User Registration
   - User Login
   - JWT Token Generation & Verification
   - Password Hashing & Verification

2. **Calculator Module**
   - Basic Operations (+ - × ÷ ^ %)
   - Advanced Operations (√, sin, cos, tan, log, ln, factorial)
   - Unit Converter (length, weight, temperature, volume)
   - Financial Calculator (simple interest, compound interest, loan payment)

3. **History Module**
   - Menyimpan semua perhitungan user
   - Menampilkan riwayat terfilter per user
   - Timestamp untuk setiap perhitungan

4. **Export Module**
   - Export ke CSV format
   - Export ke PDF format
   - User-specific data export

## 📊 ERD (Entity Relationship Diagram)

### Data Model

```
┌─────────────────────────────┐
│        USERS TABLE          │
├─────────────────────────────┤
│ PK  id (INTEGER)            │
│     username (VARCHAR 50)   │ ← UNIQUE
│     email (VARCHAR 100)     │ ← UNIQUE
│     password_hash (VARCHAR) │
│     created_at (DATETIME)   │
└─────────────────────────────┘
         ▲
         │ 1:N
         │ (One User → Many Calculations)
         │
┌─────────────────────────────┐
│  CALCULATION_HISTORY TABLE  │
├─────────────────────────────┤
│ PK  id (INTEGER)            │
│ FK  user_id (INTEGER)       │ → references users.id
│     operation_type (VARCHAR)│
│     expression (TEXT)       │
│     result (VARCHAR 255)    │
│     created_at (DATETIME)   │
└─────────────────────────────┘
```

### Relationship Rules

- **One-to-Many:** Satu user dapat memiliki banyak calculation history
- **Cascade Delete:** Jika user dihapus, semua calculationnya juga terhapus
- **Foreign Key:** `calculation_history.user_id` mereferensi `users.id`

## 🗄️ Struktur dan Informasi Detil Tabel Database

### Tabel: `users`

| Column        | Type         | Constraint                 | Deskripsi                       |
| ------------- | ------------ | -------------------------- | ------------------------------- |
| id            | INTEGER      | PRIMARY KEY, AUTOINCREMENT | ID unik user                    |
| username      | VARCHAR(50)  | NOT NULL, UNIQUE, INDEX    | Username login (unik)           |
| email         | VARCHAR(100) | NOT NULL, UNIQUE, INDEX    | Email user (unik)               |
| password_hash | VARCHAR(255) | NOT NULL                   | Password ter-hash dengan BCrypt |
| created_at    | DATETIME     | DEFAULT NOW()              | Waktu akun dibuat               |

**Sample Data:**

```
id | username | email | created_at
1  | andi | andi@gmail.com | 2026-01-17 05:12:31
2  | root | root@example.com | 2026-01-17 05:12:57
9  | alexander | komangadi@gmail.com | 2026-01-20 12:07:45
```

### Tabel: `calculation_history`

| Column         | Type         | Constraint                 | Deskripsi                                      |
| -------------- | ------------ | -------------------------- | ---------------------------------------------- |
| id             | INTEGER      | PRIMARY KEY, AUTOINCREMENT | ID unik perhitungan                            |
| user_id        | INTEGER      | NOT NULL, FOREIGN KEY      | ID user (referensi ke users.id)                |
| operation_type | VARCHAR(50)  | NOT NULL                   | Jenis operasi (addition, sin, conversion, etc) |
| expression     | TEXT         | NOT NULL                   | Ekspresi/input perhitungan                     |
| result         | VARCHAR(255) | NOT NULL                   | Hasil perhitungan                              |
| created_at     | DATETIME     | DEFAULT NOW()              | Waktu perhitungan dilakukan                    |

**Sample Data:**

```
id | user_id | operation_type | expression | result | created_at
25 | 9 | sin | sin(2.0°) | 0.03489949670250097 | 2026-01-20 15:56:17
22 | 9 | conversion | 12333.0 meter = ? km | 12.3330 kilometer | 2026-01-20 15:41:10
20 | 9 | addition | 66.0 + 95.0 | 161.0 | 2026-01-20 15:40:39
```

## 🎯 Hasil Pengembangan - Fitur-Fitur Utama

### ✅ Modul yang Telah Diimplementasikan

#### 1. **Sistem Autentikasi** ✓

- [x] User Registration dengan validasi email
- [x] User Login dengan JWT Token
- [x] Password hashing menggunakan BCrypt
- [x] Token persistence di localStorage
- [x] Token validation pada setiap request

#### 2. **Kalkulator Dasar** ✓

- [x] Operasi Addition (+)
- [x] Operasi Subtraction (-)
- [x] Operasi Multiplication (×)
- [x] Operasi Division (÷)
- [x] Operasi Power (^)
- [x] Operasi Percentage (%)
- [x] Auto-save ke history

#### 3. **Kalkulator Lanjutan** ✓

- [x] Square Root (√)
- [x] Cubic Root (∛)
- [x] Trigonometric Functions (sin, cos, tan)
- [x] Logarithm (log, ln)
- [x] Factorial (n!)
- [x] Angle unit selection (Degrees/Radians)
- [x] Auto-save ke history

#### 4. **Unit Converter** ✓

- [x] Length Conversion (meter, km, cm, mm, mile, yard, foot, inch)
- [x] Weight Conversion (kg, g, pound, ounce, ton)
- [x] Temperature Conversion (Celsius, Fahrenheit, Kelvin)
- [x] Volume Conversion (liter, mL, gallon, etc)
- [x] Auto-save ke history

#### 5. **Kalkulator Finansial** ✓

- [x] Simple Interest (Bunga Sederhana)
- [x] Compound Interest (Bunga Majemuk)
- [x] Loan Payment Calculation (Cicilan Bulanan)
- [x] Auto-save ke history

#### 6. **Riwayat Perhitungan** ✓

- [x] Display semua perhitungan user
- [x] Sorting berdasarkan tanggal
- [x] Filtering user-specific (keamanan)
- [x] Pagination/limit hasil
- [x] Timestamp untuk setiap perhitungan

#### 7. **Export Functionality** ✓

- [x] Export ke CSV format
- [x] Export ke PDF format
- [x] User-specific data (hanya data user tersebut)
- [x] Include timestamp dan operation details

#### 8. **User Interface** ✓

- [x] Dashboard dengan 4 jenis kalkulator
- [x] Responsive design (desktop & mobile)
- [x] Form validation (client-side)
- [x] Real-time result display
- [x] Error handling & user feedback

#### 9. **Database & Backend** ✓

- [x] SQLite Database dengan proper schema
- [x] SQLAlchemy ORM integration
- [x] Pydantic validation schemas
- [x] RESTful API endpoints
- [x] Proper error handling
- [x] Input sanitization

### 📊 Status Fitur

| Fitur                | Status      | Catatan                                 |
| -------------------- | ----------- | --------------------------------------- |
| User Authentication  | ✅ Complete | JWT-based, production-ready             |
| Basic Calculator     | ✅ Complete | 6 operasi dasar, auto-save working      |
| Advanced Calculator  | ✅ Complete | 10 operasi lanjutan, fixed validation   |
| Unit Converter       | ✅ Complete | 4 kategori konversi, fixed validation   |
| Financial Calculator | ✅ Complete | 3 operasi finansial, fixed element IDs  |
| History Management   | ✅ Complete | Per-user filtering, proper timestamps   |
| CSV Export           | ✅ Complete | User-specific export working            |
| PDF Export           | ✅ Complete | ReportLab integration working           |
| Database Design      | ✅ Complete | 2 main tables with proper relationships |

## 📁 Struktur Folder

```
calculator-app/
├── 📄 README.md (file ini)
├── 📄 requirements.txt (dependencies)
├── 📄 calculator.db (SQLite database)
├── 📄 check_database.py (database inspection tool)
│
├── 📁 app/ (Backend - FastAPI)
│   ├── 📄 __init__.py
│   ├── 📄 main.py (FastAPI app initialization)
│   ├── 📄 config.py (environment config)
│   ├── 📄 database.py (SQLAlchemy setup)
│   │
│   ├── 📁 models/ (Database models)
│   │   ├── 📄 user.py (User model)
│   │   └── 📄 calculation.py (CalculationHistory model)
│   │
│   ├── 📁 schemas/ (Pydantic validation schemas)
│   │   ├── 📄 user.py (User schemas)
│   │   ├── 📄 calculator.py (Calculator operation schemas)
│   │   └── 📄 history.py (History schemas)
│   │
│   ├── 📁 services/ (Business logic)
│   │   ├── 📄 auth_service.py (Authentication logic)
│   │   ├── 📄 calculator_service.py (Calculation logic)
│   │   └── 📄 history_service.py (History management)
│   │
│   ├── 📁 repositories/ (Data access layer)
│   │   ├── 📄 user_repository.py (User DB operations)
│   │   └── 📄 history_repository.py (History DB operations)
│   │
│   └── 📁 api/ (API endpoints)
│       ├── 📄 __init__.py
│       ├── 📄 auth.py (Authentication endpoints)
│       ├── 📄 calculator.py (Calculator endpoints)
│       └── 📄 history.py (History endpoints)
│
└── 📁 frontend/ (Frontend - HTML5 + JavaScript)
    ├── 📄 index.html (Main dashboard)
    ├── 📄 auth.html (Auth page)
    ├── 📄 history.html (History page)
    ├── 📄 test.html (Testing utilities)
    │
    ├── 📁 css/
    │   └── 📄 style.css (Styling)
    │
    └── 📁 js/
        ├── 📄 auth.js (Authentication logic)
        ├── 📄 calculator.js (Calculator functions)
        └── 📄 history.js (History functions)
```

### Penjelasan Folder

- **`app/`** → Backend FastAPI application
  - **`models/`** → SQLAlchemy database models (User, CalculationHistory)
  - **`schemas/`** → Pydantic request/response validation schemas
  - **`services/`** → Business logic layer (calculations, auth, history)
  - **`repositories/`** → Data access layer (CRUD operations)
  - **`api/`** → REST API endpoints (routes)

- **`frontend/`** → Frontend application
  - **`html`** → HTML pages (login, dashboard, history)
  - **`css/`** → Stylesheet
  - **`js/`** → JavaScript logic files

## ⚙️ Cara Instalasi dan Menjalankan Aplikasi

### Prerequisites

- Python 3.10 atau lebih tinggi
- pip (Python package manager)
- Web browser (Chrome, Firefox, Edge, Safari)

### Step 1: Clone atau Download Project

```bash
# Navigate ke folder project
cd calculator-app
```

### Step 2: Setup Python Virtual Environment

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Untuk Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Atau untuk Windows (Command Prompt):
venv\Scripts\activate

# Untuk Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install semua required packages
pip install -r requirements.txt
```

### Step 4: Configure Environment (Optional)

Buat file `.env` di root folder jika diperlukan:

```
DATABASE_URL=sqlite:///./calculator.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

### Step 5: Run Backend (FastAPI Server)

```bash
# Terminal 1 - Backend
cd calculator-app
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Output yang diharapkan:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Cek API Documentation:**

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Step 6: Run Frontend (HTTP Server)

```bash
# Terminal 2 - Frontend
cd calculator-app/frontend
python -m http.server 8080
```

Output yang diharapkan:

```
Serving HTTP on 127.0.0.1 port 8080
```

### Step 7: Buka Aplikasi di Browser

```
http://127.0.0.1:8080/
```

## 🎮 Cara Menggunakan Aplikasi

### 1. **Registrasi User Baru**

```
1. Klik "Register" di halaman login
2. Isi username, email, password
3. Klik "Register"
4. Anda akan redirect ke login page
```

### 2. **Login**

```
1. Isi username dan password
2. Klik "Login"
3. Dashboard akan muncul jika login berhasil
```

### 3. **Melakukan Perhitungan**

#### Basic Calculator:

```
1. Pilih "Basic Calculator"
2. Masukkan angka pertama
3. Pilih operasi (+, -, ×, ÷, ^, %)
4. Masukkan angka kedua
5. Klik "Calculate"
6. Hasil muncul dan otomatis tersimpan ke history
```

#### Advanced Calculator:

```
1. Pilih "Advanced Calculator"
2. Pilih operasi (Square, Square Root, sin, cos, dll)
3. Masukkan nilai
4. Untuk trigonometric, pilih unit (Degrees/Radians)
5. Klik "Calculate"
```

#### Unit Converter:

```
1. Pilih "Unit Converter"
2. Pilih jenis konversi (Length, Weight, Temperature)
3. Masukkan nilai
4. Pilih satuan asal dan tujuan
5. Klik "Convert"
```

#### Financial Calculator:

```
1. Pilih "Financial Calculator"
2. Pilih operasi (Simple Interest, Compound Interest, Loan Payment)
3. Masukkan principal, rate, time
4. Klik "Calculate"
```

### 4. **Melihat Riwayat**

```
1. Klik "History" di menu
2. Semua perhitungan Anda akan ditampilkan
3. Sorted berdasarkan tanggal terbaru
```

### 5. **Export Data**

```
1. Di halaman History, klik "Export to CSV" atau "Export to PDF"
2. File akan di-download dengan nama format: history_[timestamp].csv/pdf
3. Hanya data perhitungan Anda yang di-export
```

## 🔍 Database Inspection

### Menggunakan Script Python

```bash
cd calculator-app
python check_database.py
```

Output akan menampilkan:

- Daftar tabel database
- Semua user yang terdaftar
- Riwayat 20 perhitungan terakhir
- Summary perhitungan per user
- Info file database

### Menggunakan DB Browser for SQLite

```bash
1. Download DB Browser for SQLite v3.13.1
2. Buka aplikasi
3. File → Open → pilih calculator.db
4. Browse tabel users dan calculation_history
5. View dan edit data sesuai kebutuhan
```

## 🐛 Troubleshooting

### Backend tidak bisa jalan

```bash
# Check jika port 8000 sudah terpakai
netstat -ano | findstr :8000

# Jika terpakai, gunakan port lain:
uvicorn app.main:app --reload --port 8001
```

### Frontend tidak bisa akses API

```
Pastikan:
1. Backend sudah running di http://127.0.0.1:8000
2. Frontend running di http://127.0.0.1:8080
3. Check browser console (F12) untuk error messages
```

### Database error

```bash
# Reset database (HATI-HATI: semua data akan hilang)
rm calculator.db
python -c "from app.database import engine, Base; Base.metadata.create_all(engine)"
```

## 📝 API Documentation

### Authentication Endpoints

```
POST /auth/register
- Input: username, email, password
- Output: token, user info

POST /auth/login
- Input: username, password
- Output: token

POST /auth/refresh
- Input: token
- Output: new token
```

### Calculator Endpoints

```
POST /calculator/basic
- Headers: Authorization: Bearer {token}
- Input: num1, num2, operation
- Output: result, expression, history_id

POST /calculator/advanced
- Headers: Authorization: Bearer {token}
- Input: value, operation, angle_unit
- Output: result, expression, history_id

POST /calculator/convert
- Headers: Authorization: Bearer {token}
- Input: value, from_unit, to_unit, conversion_type
- Output: result, converted_value, history_id

POST /calculator/finance
- Headers: Authorization: Bearer {token}
- Input: principal, rate, time, operation
- Output: result, expression, history_id
```

### History Endpoints

```
GET /history/all
- Headers: Authorization: Bearer {token}
- Output: List of user's calculations

GET /history/export/csv
- Headers: Authorization: Bearer {token}
- Output: CSV file

GET /history/export/pdf
- Headers: Authorization: Bearer {token}
- Output: PDF file
```

## 📌 Catatan Penting

1. **Security:** JWT token disimpan di localStorage. Hati-hati dengan XSS attacks.
2. **Database:** SQLite cocok untuk development. Untuk production, gunakan PostgreSQL.
3. **CORS:** Backend sudah support CORS untuk development.
4. **Password:** Harus minimal 8 karakter dan di-hash dengan BCrypt.
5. **Token Expiry:** Token berlaku selamanya (bisa disesuaikan di config).

## 📚 Referensi

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT Documentation](https://tools.ietf.org/html/rfc7519)
- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)

---

**Terakhir diupdate:** 21 Januari 2026
