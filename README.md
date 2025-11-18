# 🗂️ DB Inspector

Inspecteur de base de données pour visualiser et gérer la structure et le contenu des tables.  
Ce projet est conçu pour fonctionner avec **SQLAlchemy** et peut être utilisé sur des bases SQLite ou PostgreSQL.  
Il permet d’afficher le schéma des tables, de consulter les données, et même de supprimer des tables si nécessaire.

---

## 🚀 Installation

Clonez le projet et installez les dépendances :

```bash
git clone https://github.com/<ton-user>/<repo>.git
cd repo
pip install -r requirements.txt
```

Pour installer en mode développement (utile si vous modifiez le code) :

```bash
pip install -e .
```

---

## ⚙️ Configuration

Le projet utilise un fichier `.env` pour stocker les paramètres sensibles.  
Exemple de `.env` :

```
DATABASE_URL=postgresql://user:password@localhost:5432/ma_base
```

👉 Assurez-vous que `DATABASE_URL` pointe vers votre base de données.

---

## 📖 Utilisation

Une fois installé, vous pouvez exécuter le script via la commande :

```bash
analyze-db --help
```

### Options disponibles :
- `--all` : Affiche les détails de toutes les tables.
- `--table <nom>` : Affiche le schéma d’une table spécifique.
- `--data <n>` : Affiche les premières lignes de données d’une table (par défaut 10).
- `--drop <nom>` : Supprime une table spécifique (⚠️ irréversible).

### Exemples :
```bash
# Afficher toutes les tables
analyze-db --all

# Inspecter une table spécifique
analyze-db --table exams

# Voir les 20 premières lignes d'une table
analyze-db --table exams --data 20

# Supprimer une table
analyze-db --drop exams
```

---

## 🛠️ Développement

Structure du projet :

```
mon-projet/
│
├── app/
│   └── core/
│       └── config.py   # settings avec Pydantic
├── scripts/
│   └── db_inspector.py # script principal
├── requirements.txt
├── setup.py ou pyproject.toml
└── README.md
```

---

## 🤝 Contribution

Les contributions sont les bienvenues !  
1. Forkez le repo  
2. Créez une branche (`git checkout -b feature/ma-fonction`)  
3. Faites vos modifications  
4. Ouvrez une Pull Request

---

## 📜 Licence

Ce projet est sous licence MIT. Vous êtes libres de l’utiliser, le modifier et le partager.
```

---

👉 Ce README est prêt à être publié sur GitHub : il explique **installation, configuration, usage, contribution et licence**.  
Tu veux que je te propose aussi un `.gitignore` adapté pour ton projet Python (venv, caches, `.env`) afin de compléter ton repo avant publication ?
