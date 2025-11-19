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
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from typing import List, Dict, Any, Optional

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
        logger.error("❌ Erreur: DATABASE_URL n'est pas configuré.")
        logger.error("💡 Options de configuration disponibles :")
        logger.error("   1. Arguments CLI : --database-url ou --db-host, --db-user, --db-name")
        logger.error("   2. Variables d'environnement : DATABASE_URL ou DB_HOST, DB_USER, DB_NAME")
        logger.error("   3. Fichier .env : Créez un fichier .env à la racine du projet")
        return None
        
    logger.info(f"Connexion à la base de données via: {database_url}")
    
    try:
        engine = create_engine(str(database_url)) # str() pour la compatibilité avec Pydantic
        with engine.connect():
            logger.info("✅ Connexion à la base de données établie avec succès.\n")
        return engine
    except Exception as e:
        logger.error(f"❌ Impossible de se connecter à la base de données: {e}")
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
    logger.info(f"\n--- Table: {table['table_name']} ({table['row_count']} lignes) ---")
    
    logger.info("  Colonnes:")
    for col in table['columns']:
        col_info = f"{col['name']} ({col['type']})"
        if not col['nullable']: col_info += " NOT NULL"
        if col['name'] in table['primary_keys']: col_info += " [PK]"
        logger.info(f"    - {col_info}")

    if table['foreign_keys']:
        logger.info("  Clés Étrangères:")
        for fk in table['foreign_keys']:
            ref = f"{fk['referred_table']}({', '.join(fk['referred_columns'])})"
            local = f"({', '.join(fk['constrained_columns'])})"
            logger.info(f"    - {local} -> {ref}")
    
    logger.info("-" * (len(table['table_name']) + 22))

def print_table_data(engine: Engine, table_name: str, limit: int):
    """Affiche les premières lignes de données d'une table."""
    with engine.connect() as connection:
        result = connection.execute(text(f'SELECT * FROM "{table_name}" LIMIT {limit}'))
        rows = result.fetchall()
        if not rows:
            logger.info(f"La table '{table_name}' est vide.")
            return
            
        logger.info(f"\n--- Données de la table: {table_name} (les {limit} premières lignes) ---")
        columns = result.keys()
        for row in rows:
            row_dict = dict(zip(columns, row))
            logger.info(row_dict)

def drop_table(engine: Engine, table_name: str):
    """Supprime une table de la base de données après confirmation."""
    logger.warning(f"⚠️  ATTENTION: Vous êtes sur le point de supprimer DÉFINITIVEMENT la table '{table_name}'.")
    confirmation = input("Êtes-vous sûr de vouloir continuer? (oui/non): ")

    if confirmation.lower() == 'oui':
        try:
            with engine.connect() as connection:
                # Utiliser 'BEGIN' et 'COMMIT' pour s'assurer que l'opération est transactionnelle
                trans = connection.begin()
                connection.execute(text(f'DROP TABLE "{table_name}"'))
                trans.commit()
            logger.info(f"✅ La table '{table_name}' a été supprimée avec succès.")
        except Exception as e:
            logger.error(f"❌ Erreur lors de la suppression de la table '{table_name}': {e}")
    else:
        logger.info("Opération annulée.")

def main():
    """Point d'entrée principal de la commande analyze-db."""
    parser = argparse.ArgumentParser(
        description="Inspecteur de base de données - Analyse et inspection de bases de données.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # --- Arguments de configuration de la base de données ---
    config_group = parser.add_argument_group(
        'Configuration de la base de données',
        'Ces options permettent de configurer la connexion directement en CLI.\n'
        'Priorité : Arguments CLI > Variables d\'environnement > Fichier .env > Défaut'
    )
    config_group.add_argument(
        "--database-url", "--db-url", "-u",
        type=str,
        metavar="URL",
        help="URL complète de la base de données (ex: postgresql://user:pass@host:port/db)\n"
             "Priorité la plus haute - override toutes les autres sources de configuration."
    )
    config_group.add_argument(
        "--db-type",
        type=str,
        metavar="TYPE",
        help="Type de base de données (postgresql, mysql, sqlite, etc.)\n"
             "Utilisé uniquement avec --db-host, --db-user, --db-name"
    )
    config_group.add_argument(
        "--db-host",
        type=str,
        metavar="HOST",
        help="Hôte de la base de données (ex: localhost, 192.168.1.1)"
    )
    config_group.add_argument(
        "--db-port",
        type=int,
        metavar="PORT",
        help="Port de la base de données (ex: 5432 pour PostgreSQL, 3306 pour MySQL)"
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
    
    # --- Arguments existants ---
    parser.add_argument("--all", "-a", action="store_true", help="Afficher les détails de TOUTES les tables.")
    parser.add_argument("--table", "-t", type=str, help="Se concentrer sur une table spécifique pour voir son schéma.")
    parser.add_argument("--data", "-d", nargs='?', type=int, const=10, default=None,
                        help="Afficher les données de la table spécifiée (nécessite --table).\n"
                             "Par défaut, 10 lignes sont affichées. Spécifiez un nombre (ex: --data 50).")
    
    # --- NOUVEL ARGUMENT POUR SUPPRIMER UNE TABLE ---
    parser.add_argument("--drop", type=str, metavar="TABLE_NAME",
                        help="Supprime une table spécifique de la base de données.\n"
                             "⚠️  Cette action est IRRÉVERSIBLE.")

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
                logger.error(f"❌ Table '{args.drop}' non trouvée. Tables disponibles: {all_table_names}")

        elif not all_details:
            logger.warning("Aucune table trouvée dans la base de données.")
        
        elif args.table:
            target_table = next((t for t in all_details if t['table_name'] == args.table), None)
            if target_table:
                print_table_schema(target_table)
                if args.data is not None:
                    print_table_data(engine, args.table, limit=args.data)
            else:
                logger.error(f"Table '{args.table}' non trouvée.")
        
        elif args.all:
            for table_info in all_details:
                print_table_schema(table_info)
        
        else:
            logger.info("Tables disponibles dans la base de données:")
            for table_info in all_details:
                logger.info(f"- {table_info['table_name']} ({table_info['row_count']} lignes)")
            logger.info("\nℹ️  Utilisez --help pour voir toutes les commandes.")


if __name__ == "__main__":
    main()