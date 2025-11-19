#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour visualiser et gérer la structure et le contenu des tables de la base de données.

NOTE: Ce script DOIT être exécuté comme un module depuis la racine du projet
pour que les imports fonctionnent correctement.

Exemple : python -m scripts.db_inspector --drop exams
"""
import logging
import argparse
import sys
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from typing import List, Dict, Any, Optional

# Import du module de couleurs
try:
    from app.utils.colors import (
        format_cyan_bright, format_bright, format_cyan, 
        format_yellow, format_dim, format_red, format_blue, format_green,
        print_section, print_info, print_warning, print_error, print_success
    )
except ImportError:
    # Fallback si le module n'est pas disponible
    def format_cyan_bright(text): return text
    def format_bright(text): return text
    def format_cyan(text): return text
    def format_yellow(text): return text
    def format_dim(text): return text
    def format_red(text): return text
    def format_blue(text): return text
    def format_green(text): return text
    def print_section(text): print(text)
    def print_info(text): print(f"ℹ️  {text}")
    def print_warning(text): print(f"⚠️  {text}")
    def print_error(text): print(f"❌ {text}")
    def print_success(text): print(f"✅ {text}")

# --- Configuration du Logging ---
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# --- Import des Settings de l'Application ---
try:
    from app.core.config import settings
except ImportError:
    logger.error("❌ Erreur d'importation. N'exécutez pas 'python scripts/db_inspector.py'.")
    logger.error("✅ Exécutez ce script comme un module depuis la racine de votre projet :")
    logger.error("   python -m scripts.db_inspector --help")
    exit(1)


def get_db_engine(custom_settings=None) -> Optional[Engine]:
    """
    Crée et retourne un engine SQLAlchemy en utilisant les settings de l'application.
    
    Args:
        custom_settings: Instance de Settings personnalisée (optionnel).
                        Si None, utilise les settings globaux.
    """
    # Utiliser les settings personnalisés si fournis, sinon les settings globaux
    from app.core.config import settings as default_settings
    active_settings = custom_settings if custom_settings else default_settings
    
    database_url = active_settings.get_database_url()
    
    if not database_url or database_url == "sqlite:///:memory:":
        # Section 2.2 : Messages d'erreur de configuration colorés
        print_error("Erreur: DATABASE_URL n'est pas configuré.")
        print_info("Options de configuration disponibles :")
        print(f"  1. Arguments CLI : {format_cyan('--database-url')} ou {format_cyan('--db-host')}, {format_cyan('--db-user')}, {format_cyan('--db-name')}")
        print(f"  2. Variables d'environnement : {format_cyan('DATABASE_URL')} ou {format_cyan('DB_HOST')}, {format_cyan('DB_USER')}, {format_cyan('DB_NAME')}")
        print(f"  3. Fichier .env : Créez un fichier {format_cyan('.env')} à la racine du projet")
        return None
        
    print(f"{format_dim('Connexion à la base de données via:')} {format_cyan(database_url)}")
    
    try:
        engine = create_engine(str(database_url)) # str() pour la compatibilité avec Pydantic
        with engine.connect():
            # Section 2.2 : Message de succès de connexion coloré
            print_success("Connexion à la base de données établie avec succès.")
            print()  # Ligne vide
        return engine
    except Exception as e:
        # Section 2.2 : Message d'erreur de connexion coloré
        print_error(f"Impossible de se connecter à la base de données: {e}")
        return None

def get_table_details(engine: Engine) -> List[Dict[str, Any]]:
    """Récupère les informations détaillées sur toutes les tables."""
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    all_tables_info: List[Dict[str, Any]] = []

    if not table_names:
        return []

    with engine.connect() as connection:
        for table_name in table_names:
            row_count = connection.execute(text(f'SELECT COUNT(*) FROM "{table_name}"')).scalar_one()
            all_tables_info.append({
                "table_name": table_name,
                "columns": inspector.get_columns(table_name),
                "primary_keys": inspector.get_pk_constraint(table_name).get('constrained_columns', []),
                "foreign_keys": inspector.get_foreign_keys(table_name),
                "row_count": row_count
            })
    return all_tables_info

def print_table_schema(table: Dict[str, Any]):
    """Affiche le schéma formaté d'une seule table."""
    # Section 2.3 : Titre de table en cyan brillant
    table_name = format_cyan_bright(table['table_name'])
    row_count = format_dim(f"({table['row_count']} lignes)")
    print(f"\n━━━ Table: {table_name} {row_count} ━━━")
    
    # Section 2.3 : Section "Colonnes" en gras
    print(f"  {format_bright('Colonnes:')}")
    for col in table['columns']:
        # Nom de colonne en gras
        col_name = format_bright(col['name'])
        # Type en bleu
        col_type = format_blue(str(col['type']))
        col_info = f"{col_name} ({col_type})"
        
        # NOT NULL en rouge
        if not col['nullable']:
            col_info += f" {format_red('NOT NULL')}"
        # [PK] en jaune
        if col['name'] in table['primary_keys']:
            col_info += f" {format_yellow('[PK]')}"
        
        print(f"    - {col_info}")

    if table['foreign_keys']:
        # Section 2.3 : Section "Foreign Keys" en gras
        print(f"  {format_bright('Clés Étrangères:')}")
        for fk in table['foreign_keys']:
            # Table référencée en vert
            ref_table = format_green(fk['referred_table'])
            ref_cols = ', '.join(fk['referred_columns'])
            ref = f"{ref_table}({ref_cols})"
            # Colonnes locales en gris
            local_cols = ', '.join(fk['constrained_columns'])
            local = format_dim(f"({local_cols})")
            # Flèche en gris
            arrow = format_dim("→")
            print(f"    - {local} {arrow} {ref}")
    
    # Séparateur en gris
    separator = format_dim("━" * (len(table['table_name']) + 22))
    print(separator)

def print_table_data(engine: Engine, table_name: str, limit: int):
    """Affiche les premières lignes de données d'une table."""
    with engine.connect() as connection:
        result = connection.execute(text(f'SELECT * FROM "{table_name}" LIMIT {limit}'))
        rows = result.fetchall()
        if not rows:
            # Section 2.4 : Message "table vide" en jaune
            print_warning(f"La table '{table_name}' est vide.")
            return
            
        # Section 2.4 : Titre en cyan brillant
        title = format_cyan_bright(f"Données de la table: {table_name}")
        subtitle = format_dim(f"(les {limit} premières lignes)")
        print(f"\n━━━ {title} {subtitle} ━━━")
        
        columns = result.keys()
        # En-têtes de colonnes en gras
        header = " | ".join(format_bright(str(col)) for col in columns)
        print(header)
        print(format_dim("─" * len(header)))
        
        for row in rows:
            row_dict = dict(zip(columns, row))
            # Afficher les données avec formatage simple
            row_str = " | ".join(str(val) if val is not None else format_dim("NULL") for val in row_dict.values())
            print(row_str)

def drop_table(engine: Engine, table_name: str):
    """Supprime une table de la base de données après confirmation."""
    # Section 2.5 : Avertissement en jaune brillant
    print_warning(f"ATTENTION: Vous êtes sur le point de supprimer DÉFINITIVEMENT la table '{format_cyan_bright(table_name)}'.")
    confirmation = input("Êtes-vous sûr de vouloir continuer? (oui/non): ")

    if confirmation.lower() == 'oui':
        try:
            with engine.connect() as connection:
                # Utiliser 'BEGIN' et 'COMMIT' pour s'assurer que l'opération est transactionnelle
                trans = connection.begin()
                connection.execute(text(f'DROP TABLE "{table_name}"'))
                trans.commit()
            # Section 2.5 : Message de succès en vert
            print_success(f"La table '{table_name}' a été supprimée avec succès.")
        except Exception as e:
            # Section 2.5 : Message d'erreur en rouge
            print_error(f"Erreur lors de la suppression de la table '{table_name}': {e}")
    else:
        # Section 2.5 : Message d'annulation en gris
        print(f"{format_dim('Opération annulée.')}")

class ColoredHelpFormatter(argparse.RawTextHelpFormatter):
    """Formatter personnalisé qui ajoute des couleurs à l'aide."""
    
    def _format_action_invocation(self, action):
        """Colore les noms d'options et arguments."""
        if not action.option_strings:
            # Argument positionnel
            return format_cyan_bright(super()._format_action_invocation(action))
        
        # Options avec couleurs
        parts = []
        for option_string in action.option_strings:
            if option_string.startswith('--'):
                # Longue option en cyan brillant
                parts.append(format_cyan_bright(option_string))
            else:
                # Option courte en cyan
                parts.append(format_cyan(option_string))
        
        return ', '.join(parts)
    
    def _format_text(self, text):
        """Colore certaines parties du texte d'aide."""
        # Le texte peut déjà contenir des codes de couleur, on le laisse tel quel
        return super()._format_text(text)


def main():
    """Point d'entrée principal de la commande analyze-db."""
    parser = argparse.ArgumentParser(
        description=format_cyan_bright("🗂️  DB Inspector") + "\n\n" +
                    "Analyse et inspection de bases de données compatibles SQLAlchemy.\n" +
                    format_dim("Visualisez la structure de vos tables, consultez les données,\n") +
                    format_dim("analysez les relations et gérez votre schéma de base de données."),
        formatter_class=ColoredHelpFormatter,
        epilog=format_dim("\n💡 Pour plus d'informations, visitez: https://github.com/AshBrud/dbinpect")
    )
    
    # --- Arguments de configuration de la base de données ---
    config_group = parser.add_argument_group(
        format_bright('⚙️  Configuration de la base de données'),
        format_dim('Ces options permettent de configurer la connexion directement en CLI.\n') +
        format_dim('Priorité : ') + format_yellow('Arguments CLI') + format_dim(' > ') + 
        format_cyan('Variables d\'environnement') + format_dim(' > ') +
        format_cyan('Fichier .env') + format_dim(' > Défaut')
    )
    config_group.add_argument(
        "--database-url", "--db-url", "-u",
        type=str,
        metavar="URL",
        help=format_bright("URL complète de la base de données") + 
             " (ex: " + format_dim("postgresql://user:pass@host:port/db") + ")\n" +
             format_yellow("Priorité la plus haute") + " - override toutes les autres sources de configuration."
    )
    config_group.add_argument(
        "--db-type",
        type=str,
        metavar="TYPE",
        help="Type de base de données (" + format_cyan("postgresql") + ", " + 
             format_cyan("mysql") + ", " + format_cyan("sqlite") + ", etc.)\n" +
             format_dim("Utilisé uniquement avec --db-host, --db-user, --db-name")
    )
    config_group.add_argument(
        "--db-host",
        type=str,
        metavar="HOST",
        help="Hôte de la base de données (ex: " + format_dim("localhost") + ", " + 
             format_dim("192.168.1.1") + ")"
    )
    config_group.add_argument(
        "--db-port",
        type=int,
        metavar="PORT",
        help="Port de la base de données (ex: " + format_dim("5432") + " pour PostgreSQL, " + 
             format_dim("3306") + " pour MySQL)"
    )
    config_group.add_argument(
        "--db-user",
        type=str,
        metavar="USER",
        help="Nom d'utilisateur pour la connexion"
    )
    config_group.add_argument(
        "--db-password",
        type=str,
        metavar="PASSWORD",
        help="Mot de passe pour la connexion"
    )
    config_group.add_argument(
        "--db-name",
        type=str,
        metavar="NAME",
        help="Nom de la base de données"
    )
    
    # --- Arguments d'inspection ---
    parser.add_argument(
        "--all", "-a", 
        action="store_true", 
        help=format_bright("Afficher les détails de TOUTES les tables.") + 
             "\n" + format_dim("Affiche le schéma complet (colonnes, types, clés) de chaque table.")
    )
    parser.add_argument(
        "--table", "-t", 
        type=str, 
        metavar="TABLE",
        help="Se concentrer sur une table spécifique pour voir son schéma.\n" +
             format_dim("Affiche les colonnes, types, clés primaires et étrangères.")
    )
    parser.add_argument(
        "--data", "-d", 
        nargs='?', 
        type=int, 
        const=10, 
        default=None,
        help="Afficher les données de la table spécifiée " + format_yellow("(nécessite --table)") + ".\n" +
             format_dim("Par défaut, ") + format_bright("10") + format_dim(" lignes sont affichées. ") +
             format_dim("Spécifiez un nombre (ex: ") + format_cyan("--data 50") + format_dim(").")
    )
    
    # --- Argument pour supprimer une table ---
    parser.add_argument(
        "--drop", 
        type=str, 
        metavar="TABLE_NAME",
        help=format_yellow("⚠️  Supprime une table spécifique de la base de données.\n") +
             format_red("Cette action est IRRÉVERSIBLE.") + 
             format_dim(" Une confirmation sera demandée.")
    )

    args = parser.parse_args()
    
    # --- Gestion de la configuration avec priorité ---
    # Priorité : Arguments CLI > Variables d'environnement > Fichier .env > Défaut
    from app.core.config import Settings
    
    # Charger d'abord les settings par défaut (lit .env et variables d'environnement)
    base_settings = Settings()
    
    # Préparer les overrides depuis les arguments CLI
    config_overrides = {}
    if args.database_url:
        config_overrides['DATABASE_URL'] = args.database_url
    if args.db_type:
        config_overrides['DB_TYPE'] = args.db_type
    if args.db_host:
        config_overrides['DB_HOST'] = args.db_host
    if args.db_port:
        config_overrides['DB_PORT'] = args.db_port
    if args.db_user:
        config_overrides['DB_USER'] = args.db_user
    if args.db_password:
        config_overrides['DB_PASSWORD'] = args.db_password
    if args.db_name:
        config_overrides['DB_NAME'] = args.db_name
    
    # Créer une nouvelle instance de Settings avec les overrides CLI si fournis
    if config_overrides:
        # Fusionner les settings de base avec les overrides CLI
        settings = Settings.model_validate({
            **base_settings.model_dump(),
            **config_overrides
        })
    else:
        # Utiliser les settings de base (variables d'env ou .env)
        settings = base_settings

    engine = get_db_engine(settings)
    if engine:
        all_details = get_table_details(engine)
        all_table_names = [t['table_name'] for t in all_details]
        
        # --- LOGIQUE POUR LA NOUVELLE COMMANDE --drop ---
        if args.drop:
            if args.drop in all_table_names:
                drop_table(engine, args.drop)
            else:
                print_error(f"Table '{args.drop}' non trouvée. Tables disponibles: {all_table_names}")

        elif not all_details:
            print_warning("Aucune table trouvée dans la base de données.")
        
        elif args.table:
            target_table = next((t for t in all_details if t['table_name'] == args.table), None)
            if target_table:
                print_table_schema(target_table)
                if args.data is not None:
                    print_table_data(engine, args.table, limit=args.data)
            else:
                print_error(f"Table '{args.table}' non trouvée.")
        
        elif args.all:
            for table_info in all_details:
                print_table_schema(table_info)
        
        else:
            # Section 2.6 : Liste des tables avec couleurs
            print_section("Tables disponibles dans la base de données:")
            for table_info in all_details:
                table_name = format_cyan_bright(table_info['table_name'])
                row_count = format_dim(f"({table_info['row_count']} lignes)")
                print(f"  - {table_name} {row_count}")
            print()  # Ligne vide
            print_info("Utilisez --help pour voir toutes les commandes.")


if __name__ == "__main__":
    main()