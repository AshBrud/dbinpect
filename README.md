# 🗂️ DB Inspector

A powerful and flexible tool to inspect and analyze any SQLAlchemy-compatible database.  
Visualize your table structures, browse data, analyze relationships, and manage your database schema directly from the command line.

---

## ✨ Features

- 🔍 **Complete Inspection** : Analyze the structure of all your tables
- 📊 **Data Visualization** : Browse the content of your tables
- 🔗 **Relationships** : Discover foreign keys and relationships between tables
- 🗑️ **Management** : Delete tables if needed (with confirmation)
- 🎯 **Multi-database** : Support for PostgreSQL, MySQL, SQLite and all SQLAlchemy-compatible databases
- ⚙️ **Flexible Configuration** : Full URL or separate variables
- 🎨 **Colorful Output** : Enhanced readability with color-coded information (table names, types, keys, errors, warnings)

---

## 📋 Prerequisites

- Python 3.8 or higher
- Access to a database (PostgreSQL, MySQL, SQLite, etc.)

---

## 🚀 Installation

### Installation from PyPI

```bash
pip install dbinpect
```

This will install the `analyze-db` command in your environment.

### Installation from Source

Clone the project and install dependencies:

```bash
git clone https://github.com/AshBrud/dbinpect.git
cd dbinpect
pip install -r requirements.txt
```

### Development Installation

To install the package in development mode (useful if you modify the code):

```bash
pip install -e .
```

This will also install the `analyze-db` command in your environment.

### Installation from GitHub

```bash
pip install git+https://github.com/AshBrud/dbinpect.git
```

---

## ⚙️ Configuration

The project offers **three methods** to configure the database connection, with a clear priority order:

**Priority order** : CLI Arguments > Environment Variables > `.env` File > Default

### Method 1: CLI Arguments (Highest Priority) ⭐

Configure directly from the command line:

```bash
# With full URL
analyze-db --database-url "postgresql://user:password@localhost:5432/mydb" --all

# With separate variables
analyze-db --db-host localhost --db-port 5432 --db-user user --db-password pass --db-name mydb --all

# Mixed: partial override
analyze-db --db-password "new_password" --all
```

**Available arguments** :
- `--database-url`, `--db-url`, `-u` : Full database URL
- `--db-type` : Database type (postgresql, mysql, sqlite, etc.)
- `--db-host` : Database host
- `--db-port` : Database port
- `--db-user` : Username
- `--db-password` : Password
- `--db-name` : Database name

### Method 2: Environment Variables

Set variables in your shell before executing the command:

```bash
# Linux/Mac/Windows Git Bash
DATABASE_URL="postgresql://user:password@localhost:5432/mydb" analyze-db --all

# Or export for the session
export DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
analyze-db --all

# Separate variables
DB_HOST=localhost DB_USER=user DB_NAME=mydb analyze-db --all
```

**Windows PowerShell** :
```powershell
$env:DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
analyze-db --all
```

**Windows CMD** :
```cmd
set DATABASE_URL=postgresql://user:password@localhost:5432/mydb
analyze-db --all
```

### Method 3: `.env` File (For Local Development)

Create a `.env` file at the project root:

```env
# Option 1: Full URL
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Option 2: Separate variables
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=mydb
```

**Create the file** :
```bash
# Linux/Mac
cp env.example .env

# Windows
copy env.example .env
```

Then edit the `.env` file with your connection information.

### Supported Database Types

- **PostgreSQL** : `postgresql://user:pass@host:port/db`
- **MySQL** : `mysql://user:pass@host:port/db`
- **SQLite** : `sqlite:///path/to/database.db`
- **Others** : All databases supported by SQLAlchemy

### Configuration Examples

```bash
# PostgreSQL via CLI
analyze-db --database-url "postgresql://postgres:mypass@localhost:5432/testdb" --all

# MySQL via environment variables
DATABASE_URL="mysql://root:password@localhost:3306/mydb" analyze-db --table users

# SQLite via CLI
analyze-db --database-url "sqlite:///./database.db" --all

# Partial override: .env contains DB_HOST, DB_USER, DB_NAME, override only password
analyze-db --db-password "new_password" --all
```

> 💡 **Note** : If `DATABASE_URL` is defined (via CLI, env or .env), it takes priority over separate variables.

---

## 📖 Usage

Once installed, you can use the `analyze-db` command:

```bash
analyze-db --help
```

### Available Options

#### Inspection Options

| Option | Description |
|--------|-------------|
| `--all`, `-a` | Display details of all tables |
| `--table <name>`, `-t <name>` | Display the schema of a specific table |
| `--data [n]`, `-d [n]` | Display the first rows of data (default 10) |
| `--drop <name>` | Delete a specific table ⚠️ **irreversible** |

#### Configuration Options (see Configuration section)

| Option | Description |
|--------|-------------|
| `--database-url`, `--db-url`, `-u` | Full database URL |
| `--db-host` | Database host |
| `--db-port` | Database port |
| `--db-user` | Username |
| `--db-password` | Password |
| `--db-name` | Database name |
| `--db-type` | Database type (postgresql, mysql, sqlite, etc.) |

### Usage Examples

#### List all tables

```bash
analyze-db
```

Displays the list of all tables with the number of rows.

#### Display details of all tables

```bash
analyze-db --all
```

Displays the complete schema (columns, types, primary keys, foreign keys) of all tables.

#### Inspect a specific table

```bash
analyze-db --table users
```

Displays the detailed schema of the `users` table:
- Columns with their types
- Primary keys
- Foreign keys
- Number of rows

#### Browse table data

```bash
# Display the first 10 rows (default)
analyze-db --table users --data

# Display the first 20 rows
analyze-db --table users --data 20
```

#### Delete a table

```bash
analyze-db --drop old_table
```

⚠️ **Warning** : This action is irreversible. A confirmation will be requested before deletion.

---

## 🎨 Color-Coded Output

DB Inspector uses colors to make the output more readable and easier to analyze:

### Color Scheme

- **Cyan Bright** : Table names, titles, and important identifiers
- **Bold** : Section headers, column names, and emphasis
- **Blue** : Data types (INTEGER, VARCHAR, TEXT, etc.)
- **Yellow** : Primary keys `[PK]`
- **Red** : `NOT NULL` constraints and error messages
- **Green** : Referenced tables in foreign keys and success messages
- **Gray (Dim)** : Secondary information (row counts, separators, hints)
- **Yellow Bright** : Warnings and important alerts

### Examples

- **Table schemas** : Column names in bold, types in blue, constraints in red/yellow
- **Foreign keys** : Referenced tables in green with gray arrows
- **Messages** : Success (green), errors (red), warnings (yellow), info (cyan)
- **Help command** : Color-coded options and descriptions

> 💡 **Note** : Colors are automatically handled by Colorama for cross-platform compatibility. If your terminal doesn't support colors, the output will still be readable without them.

---

## 🛠️ Development

### Project Structure

```
dbinpect/
│
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Configuration with Pydantic Settings
│   └── utils/
│       ├── __init__.py
│       └── colors.py           # Color formatting utilities
│
├── scripts/
│   └── db_inspector.py        # Main script
│
├── .env.example               # Configuration example
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Modern package configuration
└── README.md                  # This file
```

### Technologies Used

- **SQLAlchemy** : ORM and database connection management
- **Pydantic** : Data validation and configuration management
- **Python-dotenv** : Environment variable loading
- **Colorama** : Cross-platform colored terminal output (Windows/Linux/Mac)

### Development Dependencies Installation

```bash
pip install -r requirements.txt
```

---

## 🐛 Troubleshooting

### Error: "DATABASE_URL is not configured"

**Solution** : Check that your `.env` file exists and contains `DATABASE_URL` or the variables `DB_HOST`, `DB_USER`, `DB_NAME`.

### Error: "Unable to connect to database"

**Solutions** :
1. Check that your database is accessible
2. Verify credentials in your `.env` file
3. Check that the database service is running
4. For PostgreSQL, verify that port 5432 is open

### Command `analyze-db` not found

**Solution** : Reinstall the package in development mode:
```bash
pip install -e .
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create** a branch for your feature (`git checkout -b feature/my-feature`)
3. **Commit** your changes (`git commit -m 'Add a new feature'`)
4. **Push** to the branch (`git push origin feature/my-feature`)
5. **Open** a Pull Request

### Future Improvements

Future improvements and features are planned. Check the GitHub repository for updates.

---

## 📜 License

This project is licensed under the MIT License. You are free to use, modify, and share it.

See the [LICENSE](LICENSE) file for more details.

---

## 🙏 Acknowledgments

- [SQLAlchemy](https://www.sqlalchemy.org/) for the excellent ORM
- [Pydantic](https://docs.pydantic.dev/) for data validation
- All contributors who improve this project

---

## 📞 Support

To report a bug or suggest a feature, open an [issue](https://github.com/AshBrud/dbinpect/issues) on GitHub.

---

**Made with ❤️ for the Python community**
