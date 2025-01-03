# LogosCoffee_Bot

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![VERSION](https://img.shields.io/badge/status-in%20development-yellow)

>- 🍀 **Clear architecture** for maximum flexibility and readability.
>- 🦅 **Independent service**
>- ⚡ **Asynchronous API** for fast request processing.
>- 🤖 **Telegram Bot** for user interaction.
>- 📝 **Logging** with multiple levels of detail. _(DEV)_
>- 🔬 **Testing** service. _(DEV)_

---

## Table of Contents
1. [Features](#features)
2. [Usage](#usage)  
3. [Configuration](#configuration)   

---

---

## Features
Client:
- **Log in** by phone number.
- Submit **anonymous reviews**.
- Choosing an item to add to the **shopping cart**.
- **Making an order** based on the contents of the shopping cart. _(DEV)_
- **Receive announcements** from the admin.

Admin:
- **Log in** by the secret token.
- **Distribute announcement** for the clients.
- **Receive anonymous reviews** from the clients.
- **Setting products** for menu. _(DEV)_

Employee:
- **Log in** by the secret token.
- **Manage order states**. _(DEV)_

---

## Usage
**1. Install:** Python 3.10+, PostgreSQL

**2. Create PostgreSQL server** (localhost) then **create database.**

**3. [Configure](#configuration) the environment variables.**

**4. Create `.venv`** and **install all the dependencies** from `rquirements.txt`.

**5. Upgrade DB** using 
```bash
alembic upgrade head
```

**6. Run the project:**
```bash
python src/main.py
```

---

### Configuration
Copy `template.env` and rename to `.env`. Settings are specified in the `.env` file:
```
ADMIN_BOT_TOKEN=<VALUE>
CLIENT_BOT_TOKEN=<VALUE>
EMPLOYEE_BOT_TOKEN=<VALUE>

DEFAULT_ADMIN_TOKEN_FOR_LOGIN=2DAd6jwe21kdASCx
DEFAULT_EMPLOYEE_TOKEN_FOR_LOGIN=d4djFaSS4dasxcf9

DB_DIALECT=<VALUE>
DB_USER=<VALUE>
DB_PASSWORD=<VALUE>
DB_HOST=<VALUE>
DB_PORT=<VALUE>
DB_NAME=<VALUE>

DB_URL=${DB_DIALECT}://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```
Replace all `<VALUE>` with the corresponding values.

<br><br>