# 🗂️ DB Inspector

Un outil puissant et flexible pour inspecter et analyser n'importe quelle base de données compatible avec SQLAlchemy.  
Visualisez la structure de vos tables, consultez les données, analysez les relations et gérez votre schéma de base de données directement depuis la ligne de commande.

---

## ✨ Fonctionnalités

- 🔍 **Inspection complète** : Analysez la structure de toutes vos tables
- 📊 **Visualisation des données** : Consultez le contenu de vos tables
- 🔗 **Relations** : Découvrez les clés étrangères et les relations entre tables
- 🗑️ **Gestion** : Supprimez des tables si nécessaire (avec confirmation)
- 🎯 **Multi-bases** : Support de PostgreSQL, MySQL, SQLite et toutes les bases compatibles SQLAlchemy
- ⚙️ **Configuration flexible** : URL complète ou variables séparées

---

## 📋 Prérequis

- Python 3.8 ou supérieur
- Accès à une base de données (PostgreSQL, MySQL, SQLite, etc.)

---

## 🚀 Installation

### Installation depuis le code source

Clonez le projet et installez les dépendances :

```bash
git clone https://github.com/<ton-user>/dbinpect.git
cd dbinpect
pip install -r requirements.txt
```

### Installation en mode développement

Pour installer le package en mode développement (utile si vous modifiez le code) :

```bash
pip install -e .
```

Cela installera également la commande `analyze-db` dans votre environnement.

### Installation depuis PyPI (à venir)

```bash
pip install db-inspector
```

---

## ⚙️ Configuration

Le projet offre **trois méthodes** pour configurer la connexion à la base de données, avec un ordre de priorité clair :

**Ordre de priorité** : Arguments CLI > Variables d'environnement > Fichier `.env` > Défaut

### Méthode 1 : Arguments CLI (Priorité la plus haute) ⭐

Configurez directement depuis la ligne de commande :

```bash
# Avec URL complète
analyze-db --database-url "postgresql://user:password@localhost:5432/ma_base" --all

# Avec variables séparées
analyze-db --db-host localhost --db-port 5432 --db-user user --db-password pass --db-name ma_base --all

# Mixte : override partiel
analyze-db --db-password "new_password" --all
```

**Arguments disponibles** :
- `--database-url`, `--db-url`, `-u` : URL complète de la base de données
- `--db-type` : Type de base (postgresql, mysql, sqlite, etc.)
- `--db-host` : Hôte de la base de données
- `--db-port` : Port de la base de données
- `--db-user` : Nom d'utilisateur
- `--db-password` : Mot de passe
- `--db-name` : Nom de la base de données

### Méthode 2 : Variables d'environnement

Définissez les variables dans votre shell avant d'exécuter la commande :

```bash
# Linux/Mac/Windows Git Bash
DATABASE_URL="postgresql://user:password@localhost:5432/ma_base" analyze-db --all

# Ou exportez pour la session
export DATABASE_URL="postgresql://user:password@localhost:5432/ma_base"
analyze-db --all

# Variables séparées
DB_HOST=localhost DB_USER=user DB_NAME=ma_base analyze-db --all
```

**Windows PowerShell** :
```powershell
$env:DATABASE_URL="postgresql://user:password@localhost:5432/ma_base"
analyze-db --all
```

**Windows CMD** :
```cmd
set DATABASE_URL=postgresql://user:password@localhost:5432/ma_base
analyze-db --all
```

### Méthode 3 : Fichier `.env` (Pour développement local)

Créez un fichier `.env` à la racine du projet :

```env
# Option 1 : URL complète
DATABASE_URL=postgresql://user:password@localhost:5432/ma_base

# Option 2 : Variables séparées
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=ma_base
```

**Créer le fichier** :
```bash
# Linux/Mac
cp env.example .env

# Windows
copy env.example .env
```

Puis éditez le fichier `.env` avec vos informations de connexion.

### Types de bases de données supportées

- **PostgreSQL** : `postgresql://user:pass@host:port/db`
- **MySQL** : `mysql://user:pass@host:port/db`
- **SQLite** : `sqlite:///path/to/database.db`
- **Autres** : Toutes les bases de données supportées par SQLAlchemy

### Exemples de configuration

```bash
# PostgreSQL via CLI
analyze-db --database-url "postgresql://postgres:mypass@localhost:5432/testdb" --all

# MySQL via variables d'environnement
DATABASE_URL="mysql://root:password@localhost:3306/mydb" analyze-db --table users

# SQLite via CLI
analyze-db --database-url "sqlite:///./database.db" --all

# Override partiel : .env contient DB_HOST, DB_USER, DB_NAME, on override juste le mot de passe
analyze-db --db-password "new_password" --all
```

> 💡 **Note** : Si `DATABASE_URL` est défini (via CLI, env ou .env), il a la priorité sur les variables séparées.

---

## 📖 Utilisation

Une fois installé, vous pouvez utiliser la commande `analyze-db` :

```bash
analyze-db --help
```

### Options disponibles

#### Options d'inspection

| Option | Description |
|--------|-------------|
| `--all`, `-a` | Affiche les détails de toutes les tables |
| `--table <nom>`, `-t <nom>` | Affiche le schéma d'une table spécifique |
| `--data [n]`, `-d [n]` | Affiche les premières lignes de données (par défaut 10) |
| `--drop <nom>` | Supprime une table spécifique ⚠️ **irréversible** |

#### Options de configuration (voir section Configuration)

| Option | Description |
|--------|-------------|
| `--database-url`, `--db-url`, `-u` | URL complète de la base de données |
| `--db-host` | Hôte de la base de données |
| `--db-port` | Port de la base de données |
| `--db-user` | Nom d'utilisateur |
| `--db-password` | Mot de passe |
| `--db-name` | Nom de la base de données |
| `--db-type` | Type de base (postgresql, mysql, sqlite, etc.) |

### Exemples d'utilisation

#### Lister toutes les tables

```bash
analyze-db
```

Affiche la liste de toutes les tables avec le nombre de lignes.

#### Afficher les détails de toutes les tables

```bash
analyze-db --all
```

Affiche le schéma complet (colonnes, types, clés primaires, clés étrangères) de toutes les tables.

#### Inspecter une table spécifique

```bash
analyze-db --table users
```

Affiche le schéma détaillé de la table `users` :
- Colonnes avec leurs types
- Clés primaires
- Clés étrangères
- Nombre de lignes

#### Consulter les données d'une table

```bash
# Afficher les 10 premières lignes (par défaut)
analyze-db --table users --data

# Afficher les 20 premières lignes
analyze-db --table users --data 20
```

#### Supprimer une table

```bash
analyze-db --drop old_table
```

⚠️ **Attention** : Cette action est irréversible. Une confirmation vous sera demandée avant la suppression.

---

## 🛠️ Développement

### Structure du projet

```
dbinpect/
│
├── app/
│   ├── __init__.py
│   └── core/
│       ├── __init__.py
│       └── config.py          # Configuration avec Pydantic Settings
│
├── scripts/
│   └── db_inspector.py        # Script principal
│
├── docs/
│   └── plan-action-configurations-base.md
│
├── .env.example               # Exemple de configuration
├── requirements.txt           # Dépendances Python
├── setup.py                   # Configuration du package
└── README.md                  # Ce fichier
```

### Technologies utilisées

- **SQLAlchemy** : ORM et gestion des connexions aux bases de données
- **Pydantic** : Validation et gestion de la configuration
- **Python-dotenv** : Chargement des variables d'environnement

### Installation des dépendances de développement

```bash
pip install -r requirements.txt
```

---

## 🐛 Dépannage

### Erreur : "DATABASE_URL n'est pas configuré"

**Solution** : Vérifiez que votre fichier `.env` existe et contient `DATABASE_URL` ou les variables `DB_HOST`, `DB_USER`, `DB_NAME`.

### Erreur : "Impossible de se connecter à la base de données"

**Solutions** :
1. Vérifiez que votre base de données est accessible
2. Vérifiez les identifiants dans votre fichier `.env`
3. Vérifiez que le service de base de données est démarré
4. Pour PostgreSQL, vérifiez que le port 5432 est ouvert

### La commande `analyze-db` n'est pas trouvée

**Solution** : Réinstallez le package en mode développement :
```bash
pip install -e .
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Forkez** le repository
2. **Créez** une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonction`)
3. **Commitez** vos modifications (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. **Poussez** vers la branche (`git push origin feature/ma-fonction`)
5. **Ouvrez** une Pull Request

### Améliorations futures

Consultez le [plan d'action](docs/plan-action-configurations-base.md) pour voir les améliorations prévues.

---

## 📜 Licence

Ce projet est sous licence MIT. Vous êtes libres de l'utiliser, le modifier et le partager.

Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- [SQLAlchemy](https://www.sqlalchemy.org/) pour l'excellent ORM
- [Pydantic](https://docs.pydantic.dev/) pour la validation de données
- Tous les contributeurs qui améliorent ce projet

---

## 📞 Support

Pour signaler un bug ou proposer une fonctionnalité, ouvrez une [issue](https://github.com/<ton-user>/dbinpect/issues) sur GitHub.

---

**Fait avec ❤️ pour la communauté Python**
