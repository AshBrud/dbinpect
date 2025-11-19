#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier que les couleurs fonctionnent correctement.
"""
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.colors import (
    print_success, print_error, print_warning, print_info, print_section,
    format_cyan_bright, format_bright, format_cyan, format_yellow,
    format_dim, format_red, format_blue, format_green
)

def test_colors():
    """Teste toutes les fonctions de couleurs."""
    print("=" * 60)
    print_section("TEST DES COULEURS - DB Inspector")
    print("=" * 60)
    print()
    
    # Test des fonctions print_*
    print("--- Fonctions d'affichage direct (print) ---")
    print_success("Message de succès")
    print_error("Message d'erreur")
    print_warning("Message d'avertissement")
    print_info("Message d'information")
    print_section("Titre de section")
    print()
    
    # Test des fonctions format_*
    print("--- Fonctions de formatage (retournent une chaîne) ---")
    print(f"Texte en cyan brillant: {format_cyan_bright('Table: users')}")
    print(f"Texte en gras: {format_bright('Colonnes:')}")
    print(f"Texte en cyan: {format_cyan('postgresql')}")
    print(f"Texte en jaune: {format_yellow('[PK]')}")
    print(f"Texte en rouge: {format_red('NOT NULL')}")
    print(f"Texte en bleu: {format_blue('INTEGER')}")
    print(f"Texte en vert: {format_green('referred_table')}")
    print(f"Texte en gris: {format_dim('(10 lignes)')}")
    print()
    
    # Test d'un schéma de table simulé
    print("--- Simulation d'un schéma de table ---")
    table_name = format_cyan_bright("users")
    row_count = format_dim("(42 lignes)")
    print(f"\n━━━ Table: {table_name} {row_count} ━━━")
    print(f"  {format_bright('Colonnes:')}")
    
    # Colonne 1
    col_name = format_bright("id")
    col_type = format_blue("INTEGER")
    pk = format_yellow("[PK]")
    not_null = format_red("NOT NULL")
    print(f"    - {col_name} ({col_type}) {not_null} {pk}")
    
    # Colonne 2
    col_name = format_bright("username")
    col_type = format_blue("VARCHAR(50)")
    not_null = format_red("NOT NULL")
    print(f"    - {col_name} ({col_type}) {not_null}")
    
    # Colonne 3
    col_name = format_bright("email")
    col_type = format_blue("VARCHAR(100)")
    print(f"    - {col_name} ({col_type})")
    
    # Clé étrangère
    print(f"  {format_bright('Clés Étrangères:')}")
    local = format_dim("(user_id)")
    arrow = format_dim("→")
    ref_table = format_green("profiles")
    print(f"    - {local} {arrow} {ref_table}(id)")
    
    print()
    print("=" * 60)
    print_success("Tous les tests de couleurs ont été exécutés avec succès!")
    print("=" * 60)

if __name__ == "__main__":
    test_colors()

