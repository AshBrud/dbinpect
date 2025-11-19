"""
Module de couleurs centralisé pour l'affichage coloré dans le terminal.

Utilise Colorama pour la compatibilité multiplateforme (Windows/Linux/Mac).
"""
from colorama import init, Fore, Style

# Initialiser Colorama (autoreset=True pour réinitialiser après chaque print)
init(autoreset=True)

# ============================================
# Fonctions d'affichage direct (print)
# ============================================

def print_success(message: str):
    """Affiche un message de succès en `vert`."""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message: str):
    """Affiche un message d'erreur en `rouge brillant`."""
    print(f"{Fore.RED}{Style.BRIGHT}❌ {message}{Style.RESET_ALL}")

def print_warning(message: str):
    """Affiche un message d'avertissement en `jaune brillant`."""
    print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  {message}{Style.RESET_ALL}")

def print_info(message: str):
    """Affiche un message d'information en `cyan`."""
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

def print_section(title: str):
    """Affiche un titre de section en `gras`."""
    print(f"{Style.BRIGHT}{title}{Style.RESET_ALL}")

# ============================================
# Fonctions de formatage (retournent une chaîne)
# ============================================

def format_bright(text: str) -> str:
    """Retourne un texte formaté en `brillant` (gras)."""
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"

def format_cyan(text: str) -> str:
    """Retourne un texte formaté en `cyan` (bleu clair)."""
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"

def format_cyan_bright(text: str) -> str:
    """Retourne un texte formaté en `cyan brillant` (bleu clair très foncé)."""
    return f"{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def format_yellow(text: str) -> str:
    """Retourne un texte formaté en `jaune`."""
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

def format_green(text: str) -> str:
    """Retourne un texte formaté en `vert`."""
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

def format_red(text: str) -> str:
    """Retourne un texte formaté en `rouge`."""
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def format_dim(text: str) -> str:
    """Retourne un texte formaté en `gris` (informations secondaires)."""
    return f"{Fore.WHITE}{Style.DIM}{text}{Style.RESET_ALL}"

def format_blue(text: str) -> str:
    """Retourne un texte formaté en `bleu`."""
    return f"{Fore.BLUE}{text}{Style.RESET_ALL}"

