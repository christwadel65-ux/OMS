from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QProgressBar, QTableWidget, QTableWidgetItem, QFileDialog,
    QMessageBox, QLineEdit, QLabel, QHeaderView, QMenuBar, QAction, QAbstractItemView, QComboBox, QMenu, QInputDialog, QTextEdit, QCheckBox, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
import sys
import os
import platform
import subprocess
import webbrowser
import fnmatch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import logging
import shutil
from datetime import datetime
import json

# Configuration du logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

"""
Outil de Maintenance Système
Auteur: c.Lecomte
Version: 1.0.2
Description: Application PyQt5 pour gérer les programmes installés et détecter les dossiers vides.
"""

# Helper pour masquer la fenêtre console sur Windows
def get_subprocess_startupinfo():
    """Retourne les paramètres pour masquer la fenêtre console sur Windows."""
    if platform.system() == "Windows":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return startupinfo
    return None

def get_subprocess_creationflags():
    """Retourne les flags de création pour masquer la console sur Windows."""
    if platform.system() == "Windows":
        return subprocess.CREATE_NO_WINDOW
    return 0

# ✅ Thread pour le scan des dossiers


class ScanThread(QThread):
    """
    Thread pour scanner les dossiers vides de manière asynchrone.
    Émet des signaux de progression et de fin avec les résultats.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)

    def __init__(self, chemin):
        super().__init__()
        self.chemin = chemin
        self._is_running = True

    def run(self):
        """Exécute le scan des dossiers vides."""
        dossiers_vides_local = []
        try:
            total_dossiers = sum(len(dirs)
                                 for _, dirs, _ in os.walk(self.chemin)) + 1
            compteur = 0
            for dossier, sous_dossiers, fichiers in os.walk(self.chemin):
                if not self._is_running:
                    break
                compteur += 1
                self.progress.emit(int((compteur / total_dossiers) * 100))
                if not sous_dossiers and not fichiers:
                    taille = self.taille_dossier(dossier)
                    dossiers_vides_local.append(
                        (dossier, self.format_taille(taille)))
        except (PermissionError, OSError) as e:
            logging.error(f"Erreur lors du scan: {e}")
        finally:
            self.progress.emit(100)
            self.finished.emit(dossiers_vides_local)

    def taille_dossier(self, path):
        """Calcule la taille totale d'un dossier en octets."""
        total = 0
        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except (OSError, PermissionError) as e:
                    logging.warning(
                        f"Impossible d'accéder à {os.path.join(root, f)}: {e}")
        return total

    def stop(self):
        """Arrête le thread proprement."""
        self._is_running = False

    def format_taille(self, octets):
        for unit in ['octets', 'Ko', 'Mo', 'Go', 'To']:
            if octets < 1024:
                return f"{octets:.2f} {unit}"
            octets /= 1024
        return f"{octets:.2f} To"

# ✅ Thread pour la liste des programmes


class ProgramThread(QThread):
    """
    Thread pour lister les programmes installés de manière asynchrone.
    Compatible Windows et Linux.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._is_running = True

    def run(self):
        """Récupère la liste des programmes installés."""
        programmes = []
        systeme = platform.system()
        try:
            if systeme == "Windows":
                ps_script = r"""
                $paths = @(
                    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall',
                    'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
                )
                foreach ($path in $paths) {
                    Get-ItemProperty -Path $path\* |
                    Where-Object { $_.DisplayName } |
                    Select-Object DisplayName, DisplayVersion, InstallLocation |
                    ConvertTo-Csv -NoTypeInformation
                }
                """
                cmd = ["powershell", "-Command", ps_script]
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True,
                    startupinfo=get_subprocess_startupinfo(),
                    creationflags=get_subprocess_creationflags()
                )
                lignes = [l for l in result.stdout.splitlines(
                ) if l.strip() and not l.startswith("DisplayName")]
                total = len(lignes) or 1
                for i, ligne in enumerate(lignes):
                    parts = ligne.split(",")
                    nom = parts[0].strip('"')
                    version = parts[1].strip('"') if len(parts) > 1 else ""
                    chemin = parts[2].strip('"') if len(parts) > 2 else ""
                    programmes.append((nom, version, chemin))
                    self.progress.emit(int((i + 1) / total * 100))
            elif systeme == "Linux":
                result = subprocess.run(
                    ["dpkg-query", "-W", "-f=${Package},${Version}\n"], capture_output=True, text=True)
                lignes = result.stdout.splitlines()
                total = len(lignes) or 1
                for i, ligne in enumerate(lignes):
                    parts = ligne.split(",")
                    nom = parts[0]
                    version = parts[1] if len(parts) > 1 else ""
                    programmes.append((nom, version, "/usr/bin"))
                    self.progress.emit(int((i + 1) / total * 100))
        except (subprocess.SubprocessError, OSError) as e:
            logging.error(
                f"Erreur lors de la récupération des programmes: {e}")
            programmes = []
        finally:
            self.progress.emit(100)
            self.finished.emit(programmes)

    def stop(self):
        """Arrête le thread proprement."""
        self._is_running = False

# ✅ Thread pour la recherche globale dans C:


class GlobalSearchThread(QThread):
    """
    Thread pour effectuer une recherche globale de fichiers.
    Limite les résultats pour éviter la surcharge mémoire.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    MAX_RESULTS = 1000  # Limite de sécurité

    def __init__(self, mot_cle, chemin_base="C:\\"):
        super().__init__()
        self.mot_cle = mot_cle.lower()
        self.chemin_base = chemin_base
        self._is_running = True

    def run(self):
        """Exécute la recherche globale avec limite de résultats."""
        resultats = []
        compteur = 0
        dossiers_exclus = ['$Recycle.Bin',
                           'Windows\\WinSxS', 'System Volume Information']

        try:
            for root, dirs, files in os.walk(self.chemin_base, topdown=True):
                if not self._is_running or len(resultats) >= self.MAX_RESULTS:
                    break

                # Exclure certains dossiers système
                dirs[:] = [d for d in dirs if not any(
                    exclu in os.path.join(root, d) for exclu in dossiers_exclus)]

                compteur += 1
                self.progress.emit(compteur % 100)

                for name in files:
                    if self.mot_cle in name.lower():
                        chemin_complet = os.path.join(root, name)
                        resultats.append(chemin_complet)
                        if len(resultats) >= self.MAX_RESULTS:
                            break
        except (PermissionError, OSError) as e:
            logging.warning(f"Accès refusé à certains dossiers: {e}")
        finally:
            self.finished.emit(resultats)

    def stop(self):
        """Arrête le thread proprement."""
        self._is_running = False


class DiskAnalysisThread(QThread):
    """
    Thread pour analyser l'espace disque et trouver les gros fichiers.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)

    def __init__(self, chemin, taille_min_mo=100):
        super().__init__()
        self.chemin = chemin
        self.taille_min = taille_min_mo * 1024 * 1024
        self._is_running = True

    def run(self):
        """Analyse les disques et trouve les gros fichiers."""
        resultats = {
            'partitions': [],
            'gros_fichiers': []
        }

        try:
            # Analyse des partitions
            if platform.system() == "Windows":
                import string
                for lettre in string.ascii_uppercase:
                    disque = f"{lettre}:\\"
                    if os.path.exists(disque):
                        try:
                            usage = shutil.disk_usage(disque)
                            resultats['partitions'].append({
                                'nom': lettre,
                                'total': usage.total,
                                'utilise': usage.used,
                                'libre': usage.free,
                                'pourcentage': (usage.used / usage.total * 100) if usage.total > 0 else 0
                            })
                        except (OSError, PermissionError):
                            pass
            else:
                usage = shutil.disk_usage("/")
                resultats['partitions'].append({
                    'nom': '/',
                    'total': usage.total,
                    'utilise': usage.used,
                    'libre': usage.free,
                    'pourcentage': (usage.used / usage.total * 100) if usage.total > 0 else 0
                })

            self.progress.emit(30)

            # Recherche des gros fichiers
            compteur = 0
            for root, dirs, files in os.walk(self.chemin):
                if not self._is_running or len(resultats['gros_fichiers']) >= 500:
                    break

                # Exclure les dossiers système
                dirs[:] = [d for d in dirs if d not in [
                    '$Recycle.Bin', 'System Volume Information', 'Windows']]

                compteur += 1
                if compteur % 100 == 0:
                    self.progress.emit(30 + (compteur % 70))

                for fichier in files:
                    try:
                        chemin_complet = os.path.join(root, fichier)
                        taille = os.path.getsize(chemin_complet)
                        if taille >= self.taille_min:
                            resultats['gros_fichiers'].append({
                                'chemin': chemin_complet,
                                'nom': fichier,
                                'taille': taille,
                                'date_modif': datetime.fromtimestamp(os.path.getmtime(chemin_complet))
                            })
                    except (OSError, PermissionError):
                        pass

            # Trier par taille décroissante
            resultats['gros_fichiers'].sort(
                key=lambda x: x['taille'], reverse=True)

        except Exception as e:
            logging.error(f"Erreur analyse disque: {e}")
        finally:
            self.progress.emit(100)
            self.finished.emit(resultats)

    def stop(self):
        """Arrête le thread proprement."""
        self._is_running = False


class CleanupThread(QThread):
    """
    Thread pour nettoyer les fichiers temporaires et le cache système.
    """
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)

    def __init__(self, options):
        super().__init__()
        self.options = options
        self._is_running = True

    def run(self):
        """Exécute le nettoyage selon les options."""
        resultats = {
            'fichiers_supprimes': 0,
            'espace_libere': 0,
            'erreurs': 0,
            'details': []
        }

        try:
            if self.options.get('temp_windows'):
                self.progress.emit(10, "Nettoyage dossier Temp Windows...")
                self._nettoyer_dossier(os.environ.get('TEMP', ''), resultats)
                self._nettoyer_dossier(os.environ.get('TMP', ''), resultats)

            if self.options.get('temp_user'):
                self.progress.emit(30, "Nettoyage dossier Temp utilisateur...")
                temp_user = os.path.join(os.environ.get(
                    'USERPROFILE', ''), 'AppData', 'Local', 'Temp')
                self._nettoyer_dossier(temp_user, resultats)

            if self.options.get('prefetch'):
                self.progress.emit(50, "Nettoyage Prefetch...")
                prefetch = r'C:\Windows\Prefetch'
                if os.path.exists(prefetch):
                    self._nettoyer_dossier(prefetch, resultats)

            if self.options.get('recycle_bin'):
                self.progress.emit(70, "Vidage de la corbeille...")
                self._vider_corbeille(resultats)

            if self.options.get('browser_cache'):
                self.progress.emit(85, "Nettoyage cache navigateurs...")
                self._nettoyer_cache_navigateurs(resultats)

        except Exception as e:
            logging.error(f"Erreur nettoyage: {e}")
            resultats['erreurs'] += 1
        finally:
            self.progress.emit(100, "Nettoyage terminé")
            self.finished.emit(resultats)

    def _nettoyer_dossier(self, chemin, resultats):
        """Nettoie un dossier de ses fichiers temporaires."""
        if not os.path.exists(chemin):
            return

        for root, dirs, files in os.walk(chemin):
            if not self._is_running:
                break
            for fichier in files:
                try:
                    chemin_fichier = os.path.join(root, fichier)
                    taille = os.path.getsize(chemin_fichier)
                    os.remove(chemin_fichier)
                    resultats['fichiers_supprimes'] += 1
                    resultats['espace_libere'] += taille
                    resultats['details'].append(f"Supprimé: {fichier}")
                except (OSError, PermissionError) as e:
                    resultats['erreurs'] += 1
                    logging.warning(f"Impossible de supprimer {fichier}: {e}")

    def _vider_corbeille(self, resultats):
        """Vide la corbeille Windows."""
        try:
            if platform.system() == "Windows":
                import winshell
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                resultats['details'].append("Corbeille vidée")
            else:
                # Linux
                corbeille = os.path.expanduser('~/.local/share/Trash/files')
                if os.path.exists(corbeille):
                    self._nettoyer_dossier(corbeille, resultats)
        except Exception as e:
            logging.error(f"Erreur vidage corbeille: {e}")
            resultats['erreurs'] += 1

    def _nettoyer_cache_navigateurs(self, resultats):
        """Nettoie les caches des navigateurs populaires."""
        userprofile = os.environ.get('USERPROFILE', '')
        caches = [
            os.path.join(userprofile, 'AppData', 'Local', 'Google',
                         'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(userprofile, 'AppData', 'Local', 'Microsoft',
                         'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(userprofile, 'AppData', 'Local',
                         'Mozilla', 'Firefox', 'Profiles')
        ]

        for cache in caches:
            if os.path.exists(cache):
                self._nettoyer_dossier(cache, resultats)

    def stop(self):
        """Arrête le thread proprement."""
        self._is_running = False


class UninstallThread(QThread):
    """
    Thread pour désinstaller un programme de manière asynchrone.
    """
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, programme_nom, display_name):
        super().__init__()
        self.programme_nom = programme_nom
        self.display_name = display_name
        self._is_running = True

    def run(self):
        """Exécute la désinstallation du programme."""
        try:
            if platform.system() == "Windows":
                self.progress.emit(10, f"Recherche de {self.display_name}...")
                
                # Recherche du programme dans le registre pour trouver la commande de désinstallation
                ps_script = r"""
                $paths = @(
                    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall',
                    'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
                    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall'
                )
                foreach ($path in $paths) {
                    Get-ItemProperty -Path $path\* |
                    Where-Object { $_.DisplayName -eq '""" + self.display_name + r"""' } |
                    Select-Object UninstallString, QuietUninstallString |
                    ConvertTo-Csv -NoTypeInformation
                }
                """
                
                self.progress.emit(30, "Récupération des informations de désinstallation...")
                cmd = ["powershell", "-Command", ps_script]
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=30,
                    startupinfo=get_subprocess_startupinfo(),
                    creationflags=get_subprocess_creationflags()
                )
                
                uninstall_cmd = None
                lines = [l for l in result.stdout.splitlines() if l.strip() and not l.startswith('"UninstallString"')]
                
                if lines:
                    parts = lines[0].split(',', 1)
                    # Utiliser QuietUninstallString si disponible, sinon UninstallString
                    if len(parts) > 1 and parts[1].strip().strip('"'):
                        uninstall_cmd = parts[1].strip().strip('"')
                    elif parts[0].strip().strip('"'):
                        uninstall_cmd = parts[0].strip().strip('"')
                
                if not uninstall_cmd:
                    self.finished.emit(False, f"Impossible de trouver la commande de désinstallation pour {self.display_name}")
                    return
                
                self.progress.emit(50, f"Désinstallation de {self.display_name}...")
                logging.info(f"Commande de désinstallation: {uninstall_cmd}")
                
                # Vérifier si le désinstalleur existe réellement
                # Extraire le chemin de l'exécutable de la commande
                exe_path_to_check = None
                if uninstall_cmd.startswith('"'):
                    # Commande avec guillemets
                    end_quote = uninstall_cmd.find('"', 1)
                    if end_quote > 0:
                        exe_path_to_check = uninstall_cmd[1:end_quote]
                elif '.exe' in uninstall_cmd.lower():
                    # Commande sans guillemets
                    exe_end = uninstall_cmd.lower().find('.exe') + 4
                    # Prendre jusqu'à l'exe, en séparant sur le premier espace après
                    cmd_part = uninstall_cmd[:exe_end]
                    if ' /' in cmd_part or ' -' in cmd_part:
                        # Il y a des arguments avant .exe, prendre seulement le début
                        exe_path_to_check = cmd_part.split()[0] if ' ' in cmd_part else cmd_part
                    else:
                        exe_path_to_check = cmd_part
                
                # Vérifier l'existence pour les chemins non-msiexec
                if exe_path_to_check and 'msiexec' not in exe_path_to_check.lower():
                    if not os.path.exists(exe_path_to_check):
                        self.finished.emit(False, 
                            f"Le désinstalleur n'existe pas: {exe_path_to_check}\n\n"
                            f"Le programme a peut-être été déplacé ou désinstallé manuellement.\n"
                            f"Vous pouvez supprimer l'entrée du registre manuellement.")
                        logging.warning(f"Désinstalleur introuvable: {exe_path_to_check}")
                        return
                
                # Préparer la commande de désinstallation
                # Certaines commandes incluent des arguments, d'autres non
                if 'msiexec' in uninstall_cmd.lower():
                    # Pour les installations MSI, ajouter /quiet pour une désinstallation silencieuse
                    if '/quiet' not in uninstall_cmd.lower() and '/qn' not in uninstall_cmd.lower():
                        uninstall_cmd += ' /quiet /norestart'
                
                # Détecter si la commande commence par un chemin (sans guillemets) avec des espaces
                # et l'entourer de guillemets si nécessaire
                if uninstall_cmd and not uninstall_cmd.startswith('"'):
                    # Chercher si c'est un chemin avec .exe
                    if '.exe' in uninstall_cmd.lower():
                        # Séparer le chemin de l'exe et les arguments
                        exe_end = uninstall_cmd.lower().find('.exe') + 4
                        exe_path = uninstall_cmd[:exe_end]
                        args = uninstall_cmd[exe_end:]
                        
                        # Si le chemin contient des espaces, ajouter des guillemets
                        if ' ' in exe_path and not exe_path.startswith('"'):
                            uninstall_cmd = f'"{exe_path}"{args}'
                
                self.progress.emit(70, "Exécution de la désinstallation...")
                logging.info(f"Commande finale: {uninstall_cmd}")
                
                # Exécuter avec un timeout de 5 minutes
                # Utiliser Popen pour pouvoir vérifier si le processus est toujours en cours
                import time
                process = subprocess.Popen(
                    uninstall_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    startupinfo=get_subprocess_startupinfo(),
                    creationflags=get_subprocess_creationflags()
                )
                
                # Attendre que le processus se termine (avec timeout)
                try:
                    stdout, stderr = process.communicate(timeout=300)
                    returncode = process.returncode
                except subprocess.TimeoutExpired:
                    process.kill()
                    self.finished.emit(False, "La désinstallation a pris trop de temps (timeout de 5 minutes).")
                    return
                
                self.progress.emit(100, "Désinstallation terminée")
                
                # Vérifier le code de retour
                if returncode == 0 or returncode == 3010:  # 3010 = reboot required
                    message = f"Programme '{self.display_name}' désinstallé avec succès."
                    if returncode == 3010:
                        message += " Un redémarrage peut être nécessaire."
                    self.finished.emit(True, message)
                elif returncode == 1602 or returncode == 1223:
                    # 1602/1223 = User cancelled
                    self.finished.emit(False, "Désinstallation annulée par l'utilisateur.")
                else:
                    error_msg = stderr[:200] if stderr else "Aucun message d'erreur"
                    self.finished.emit(False, f"Erreur lors de la désinstallation (code {returncode}).\n{error_msg}")
                    
            else:
                # Pour Linux
                self.progress.emit(50, f"Désinstallation de {self.programme_nom}...")
                cmd = ["sudo", "apt-get", "remove", "-y", self.programme_nom]
                process = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if process.returncode == 0:
                    self.finished.emit(True, f"Programme '{self.programme_nom}' désinstallé avec succès.")
                else:
                    self.finished.emit(False, f"Erreur lors de la désinstallation: {process.stderr[:200]}")
                    
        except subprocess.TimeoutExpired:
            self.finished.emit(False, "La désinstallation a pris trop de temps (timeout).")
        except Exception as e:
            logging.error(f"Erreur désinstallation: {e}")
            self.finished.emit(False, f"Erreur: {str(e)}")

    def stop(self):
        """Arrête le thread proprement."""
        self._is_running = False


class SecurityAnalysisThread(QThread):
    """
    Thread pour analyser la sécurité du système.
    """
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._is_running = True

    def run(self):
        """Analyse la sécurité du système."""
        resultats = {
            'programmes_demarrage': [],
            'programmes_obsoletes': [],
            'ports_ouverts': [],
            'services_suspects': []
        }

        try:
            self.progress.emit(20)
            # Programmes au démarrage
            if platform.system() == "Windows":
                resultats['programmes_demarrage'] = self._get_startup_programs()

            self.progress.emit(50)
            # Programmes potentiellement obsolètes (> 5 ans)
            resultats['programmes_obsoletes'] = self._check_obsolete_programs()

            self.progress.emit(80)
            # Services Windows suspects
            resultats['services_suspects'] = self._check_suspicious_services()

        except Exception as e:
            logging.error(f"Erreur analyse sécurité: {e}")
        finally:
            self.progress.emit(100)
            self.finished.emit(resultats)

    def _get_startup_programs(self):
        """Récupère les programmes au démarrage Windows."""
        startup_progs = []
        try:
            import winreg
            keys = [
                (winreg.HKEY_CURRENT_USER,
                 r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE,
                 r"Software\Microsoft\Windows\CurrentVersion\Run")
            ]

            for hkey, subkey in keys:
                try:
                    key = winreg.OpenKey(hkey, subkey)
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup_progs.append(
                                {'nom': name, 'chemin': value})
                            i += 1
                        except WindowsError:
                            break
                    winreg.CloseKey(key)
                except WindowsError:
                    pass
        except Exception as e:
            logging.error(f"Erreur lecture démarrage: {e}")

        return startup_progs

    def _check_obsolete_programs(self):
        """Vérifie les programmes potentiellement obsolètes."""
        obsoletes = []
        # Liste de programmes couramment obsolètes
        obsolete_patterns = ['java 6', 'java 7', 'flash',
                             'silverlight', 'quicktime', 'realplayer']

        try:
            if platform.system() == "Windows":
                ps_script = r"""
                $paths = @(
                    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall',
                    'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
                )
                foreach ($path in $paths) {
                    Get-ItemProperty -Path $path\* |
                    Where-Object { $_.DisplayName } |
                    Select-Object DisplayName, DisplayVersion, InstallDate |
                    ConvertTo-Csv -NoTypeInformation
                }
                """
                cmd = ["powershell", "-Command", ps_script]
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=30,
                    startupinfo=get_subprocess_startupinfo(),
                    creationflags=get_subprocess_creationflags()
                )

                for ligne in result.stdout.splitlines():
                    if any(pattern in ligne.lower() for pattern in obsolete_patterns):
                        parts = ligne.split(",")
                        if len(parts) >= 2:
                            obsoletes.append({
                                'nom': parts[0].strip('"'),
                                'version': parts[1].strip('"') if len(parts) > 1 else 'N/A',
                                'raison': 'Programme obsolète ou non maintenu'
                            })
        except Exception as e:
            logging.error(f"Erreur check obsoletes: {e}")

        return obsoletes[:20]  # Limiter à 20 résultats

    def _check_suspicious_services(self):
        """Vérifie les services Windows suspects."""
        suspects = []
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["powershell", "-Command",
                        "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object Name, DisplayName | ConvertTo-Csv -NoTypeInformation"],
                    capture_output=True, 
                    text=True, 
                    timeout=15,
                    startupinfo=get_subprocess_startupinfo(),
                    creationflags=get_subprocess_creationflags()
                )

                # Services souvent inutiles ou suspects
                suspicious_names = ['telemetry',
                                    'diagtrack', 'dmwappush', 'remoteregistry']

                for ligne in result.stdout.splitlines()[1:]:  # Skip header
                    if any(susp in ligne.lower() for susp in suspicious_names):
                        parts = ligne.split(",")
                        if len(parts) >= 2:
                            suspects.append({
                                'service': parts[0].strip('"'),
                                'description': parts[1].strip('"'),
                                'remarque': 'Service potentiellement inutile'
                            })
        except Exception as e:
            logging.error(f"Erreur check services: {e}")

        return suspects[:15]  # Limiter à 15 résultats

    def stop(self):
        """Arrête le thread proprement."""
        self._is_running = False


# ✅ Interface principale


class MaintenanceTool(QMainWindow):
    """
    Fenêtre principale de l'outil de maintenance système.
    Permet de gérer les programmes installés et de détecter les dossiers vides.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Outil Maintenance v1.0.2")
        self.resize(1600, 900)
        self.setMinimumSize(1300, 800)

        # Attributs pour stocker les données (remplace les variables globales)
        self.tous_les_programmes = []
        self.dossiers_vides = []
        self.current_theme = "dark"

        # Références aux threads pour pouvoir les arrêter
        self.scan_thread = None
        self.program_thread = None
        self.global_thread = None
        self.disk_thread = None
        self.cleanup_thread = None
        self.security_thread = None
        self.uninstall_thread = None

        # Données pour les nouvelles fonctionnalités
        self.disk_data = {}
        self.security_data = {}

        # ✅ Thème coloré amélioré
        self.setStyleSheet(
            "QMainWindow { background-color: #1e1e2e; color: #f0f0f0; font-family: 'Segoe UI', Arial; font-size: 9pt; }"
            "QLabel { background-color: #1e1e2e; color: #f0f0f0; font-size: 9pt; }"
            "QLabel#title { font-size: 11pt; font-weight: bold; color: #64b5f6; }"
            "QTabWidget::pane { border: 1px solid #3a3a52; background-color: #1e1e2e; }"
            "QTabBar::tab { background: #2d2d42; color: #b0b0c0; padding: 6px 14px; margin-right: 6px; font-size: 9pt; border: none; min-height: 30px; min-width: 200px; }"
            "QTabBar::tab:selected { background: #3a4a7c; color: #ffffff; border-bottom: 2px solid #64b5f6; font-weight: bold; }"
            "QTabBar::tab:hover:!selected { background: #35354a; color: #d0d0d0; }"
            "QPushButton { background-color: #3a4a7c; color: #ffffff; border: none; border-radius: 4px; padding: 7px 14px; font-size: 9pt; font-weight: 600; min-height: 28px; }"
            "QPushButton:hover { background-color: #4a5a9c; color: #ffffff; }"
            "QPushButton:pressed { background-color: #2a3a6c; color: #ffffff; }"
            "QPushButton:disabled { background-color: #2d2d42; color: #707070; }"
            "QLineEdit { background-color: #2d2d42; color: #f0f0f0; border: 1px solid #3a3a52; border-radius: 3px; padding: 5px; font-size: 9pt; selection-background-color: #3a4a7c; min-height: 26px; }"
            "QLineEdit:focus { border: 1px solid #64b5f6; color: #ffffff; }"
            "QTableWidget { background-color: #2d2d42; alternate-background-color: #35354a; color: #f0f0f0; gridline-color: #3a3a52; font-size: 9pt; }"
            "QTableWidget::item { padding: 4px; color: #f0f0f0; }"
            "QTableWidget::item:selected { background-color: #3a4a7c; color: #ffffff; }"
            "QHeaderView::section { background-color: #3a4a7c; color: #ffffff; padding: 5px; border: none; font-weight: bold; font-size: 9pt; }"
            "QProgressBar { background-color: #2d2d42; color: #f0f0f0; border: 1px solid #3a3a52; border-radius: 3px; text-align: center; font-size: 8pt; padding: 2px; height: 18px; }"
            "QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #64b5f6, stop:1 #42a5f5); border-radius: 2px; }"
            "QTextEdit { background-color: #2d2d42; color: #f0f0f0; border: 1px solid #3a3a52; border-radius: 3px; padding: 5px; font-family: 'Consolas', monospace; font-size: 8pt; }"
            "QTextEdit:focus { border: 1px solid #64b5f6; color: #ffffff; }"
            "QCheckBox { color: #ffffff; spacing: 6px; font-size: 9pt; background-color: transparent; font-weight: 500; }"
            "QCheckBox::indicator { width: 18px; height: 18px; }"
            "QCheckBox::indicator:unchecked { background-color: #2d2d42; border: 2px solid #555555; border-radius: 3px; }"
            "QCheckBox::indicator:checked { background-color: #3a4a7c; border: 2px solid #64b5f6; image: url(); }"
            "QCheckBox::indicator:hover { border: 2px solid #64b5f6; }"
            "QComboBox { background-color: #2d2d42; color: #f0f0f0; border: 1px solid #3a3a52; border-radius: 3px; padding: 5px; font-size: 9pt; min-height: 26px; }"
            "QComboBox::drop-down { border: none; }"
            "QComboBox::down-arrow { image: url(); }"
            "QComboBox QAbstractItemView { background-color: #2d2d42; color: #f0f0f0; selection-background-color: #3a4a7c; }"
            "QMessageBox { background-color: #1e1e2e; color: #f0f0f0; }"
            "QMessageBox QLabel { color: #f0f0f0; }"
            "QMessageBox QPushButton { background-color: #3a4a7c; color: #ffffff; border: none; border-radius: 4px; padding: 7px 14px; font-size: 9pt; font-weight: 600; min-height: 28px; }"
            "QMessageBox QPushButton:hover { background-color: #4a5a9c; }"
            "QMessageBox QPushButton:pressed { background-color: #2a3a6c; }"
            "QMenu { background-color: #2d2d42; color: #f0f0f0; border: 1px solid #3a3a52; }"
            "QMenu::item:selected { background-color: #3a4a7c; color: #ffffff; }"
            "QMenuBar { background-color: #1e1e2e; color: #f0f0f0; border-bottom: 1px solid #3a3a52; font-size: 9pt; padding: 6px 12px; }"
            "QMenuBar::item { padding: 4px 10px; margin-right: 8px; }"
            "QMenuBar::item:selected { background-color: #3a4a7c; color: #ffffff; }"
            "QFrame#headerBar { background-color: #181824; border-bottom: 1px solid #3a3a52; }"
            "QPushButton#headerButton { background-color: #2d2d42; color: #f0f0f0; border: 1px solid #3a3a52; border-radius: 7px; padding: 8px 14px; font-size: 9pt; font-weight: 700; min-width: 150px; }"
            "QPushButton#headerButton:hover { background-color: #3a4a7c; border-color: #64b5f6; }"
            "QPushButton#headerButton:pressed { background-color: #2a3a6c; }"
        )

        # ✅ Actions
        self.action_export = QAction("💾 Exporter la liste", self)
        self.action_export.setShortcut("Ctrl+E")
        self.action_export.triggered.connect(self.exporter_liste)
        self.action_export_pdf_prog = QAction(
            "📄 Exporter programmes en PDF", self)
        self.action_export_pdf_prog.triggered.connect(
            self.exporter_programmes_pdf)
        self.action_export_pdf_dos = QAction(
            "📄 Exporter dossiers en PDF", self)
        self.action_export_pdf_dos.triggered.connect(
            self.exporter_dossiers_pdf)
        self.action_quit = QAction("❌ Quitter", self)
        self.action_quit.setShortcut("Ctrl+Q")
        self.action_quit.triggered.connect(self.close)
        self.action_about = QAction("ℹ️ À propos", self)
        self.action_about.setShortcut("F1")
        self.action_about.triggered.connect(self.show_about)
        self.addActions([
            self.action_export,
            self.action_export_pdf_prog,
            self.action_export_pdf_dos,
            self.action_quit,
            self.action_about,
        ])

        # ✅ Barre d'actions simple (boutons au lieu de menu déroulant)
        header_bar = QFrame()
        header_bar.setObjectName("headerBar")
        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(14, 10, 14, 8)
        header_layout.setSpacing(10)

        def make_header_button(text, slot):
            btn = QPushButton(text)
            btn.setObjectName("headerButton")
            btn.clicked.connect(slot)
            return btn

        header_layout.addWidget(make_header_button(
            "💾 Exporter la liste", self.exporter_liste))
        header_layout.addWidget(make_header_button(
            "📄 PDF Programmes", self.exporter_programmes_pdf))
        header_layout.addWidget(make_header_button(
            "📄 PDF Dossiers", self.exporter_dossiers_pdf))
        header_layout.addWidget(make_header_button(
            "ℹ️ À propos", self.show_about))
        header_layout.addStretch()
        header_layout.addWidget(make_header_button("❌ Quitter", self.close))

        # ✅ Onglets
        self.tabs = QTabWidget()
        self.tabs.tabBar().setElideMode(Qt.ElideNone)
        self.tabs.tabBar().setUsesScrollButtons(True)
        self.tabs.tabBar().setExpanding(True)

        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(header_bar)
        main_layout.addWidget(self.tabs)
        self.setCentralWidget(central)

        # --- Onglet Programmes ---
        tab_programmes = QWidget()
        layout_prog = QVBoxLayout(tab_programmes)
        layout_prog.setContentsMargins(10, 10, 10, 10)
        layout_prog.setSpacing(10)
        self.tabs.addTab(tab_programmes, "Programmes installés")

        btn_layout = QHBoxLayout()
        self.btn_list = QPushButton("Lister les programmes")
        self.btn_list.clicked.connect(self.lancer_scan_programmes)
        btn_layout.addWidget(self.btn_list)

        # ✅ Bouton désinstaller
        self.btn_uninstall = QPushButton("Désinstaller le programme sélectionné")
        self.btn_uninstall.clicked.connect(self.desinstaller_programme)
        btn_layout.addWidget(self.btn_uninstall)

        # ✅ Bouton recherche globale
        self.btn_global_search = QPushButton("Recherche globale (C:)")
        self.btn_global_search.clicked.connect(self.lancer_recherche_globale)
        btn_layout.addWidget(self.btn_global_search)

        self.progress_prog = QProgressBar()
        btn_layout.addWidget(self.progress_prog)
        layout_prog.addLayout(btn_layout)

        # ✅ Barre de recherche avancée
        search_layout = QHBoxLayout()
        self.entry_filter = QLineEdit()
        self.entry_filter.setPlaceholderText("Filtrer par mot-clé...")
        self.entry_filter.textChanged.connect(self.filtrer_programmes)
        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["Tous", "Programme", "Version", "Chemin"])
        self.combo_filter.currentIndexChanged.connect(self.filtrer_programmes)
        search_layout.addWidget(QLabel("Recherche :"))
        search_layout.addWidget(self.entry_filter)
        search_layout.addWidget(QLabel("Filtrer par :"))
        search_layout.addWidget(self.combo_filter)
        layout_prog.addLayout(search_layout)

        self.table_programmes = QTableWidget(0, 3)
        self.table_programmes.setHorizontalHeaderLabels(
            ["Programme", "Version", "Chemin"])
        self.table_programmes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_programmes.setSortingEnabled(True)
        self.table_programmes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_programmes.cellDoubleClicked.connect(self.ouvrir_programme)
        layout_prog.addWidget(self.table_programmes)


# ✅ Menu contextuel pour copier uniquement le chemin
        self.table_programmes.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_programmes.customContextMenuRequested.connect(
            self.menu_contextuel_programmes)

        # --- Onglet Dossiers ---
        tab_dossiers = QWidget()
        layout_dos = QVBoxLayout(tab_dossiers)
        self.tabs.addTab(tab_dossiers, "Dossiers vides")

        select_layout = QHBoxLayout()
        self.label_path = QLabel("Chemin du dossier :")
        self.entry_path = QLineEdit()
        self.btn_browse = QPushButton("Parcourir")
        self.btn_browse.clicked.connect(self.parcourir_dossier)
        select_layout.addWidget(self.label_path)
        select_layout.addWidget(self.entry_path)
        select_layout.addWidget(self.btn_browse)
        layout_dos.addLayout(select_layout)

        btn_layout_dos = QHBoxLayout()
        self.btn_search = QPushButton("Rechercher")
        self.btn_search.clicked.connect(self.lancer_scan_dossiers)
        self.btn_delete = QPushButton("Supprimer sélection")
        self.btn_delete.clicked.connect(self.supprimer_selection)
        self.btn_export = QPushButton("Exporter la liste")
        self.btn_export.clicked.connect(self.exporter_liste)
        btn_layout_dos.addWidget(self.btn_search)
        btn_layout_dos.addWidget(self.btn_delete)
        btn_layout_dos.addWidget(self.btn_export)
        layout_dos.addLayout(btn_layout_dos)

        self.progress_bar = QProgressBar()
        layout_dos.addWidget(self.progress_bar)

        self.table_dossiers = QTableWidget(0, 2)
        self.table_dossiers.setHorizontalHeaderLabels(["Dossier", "Taille"])
        self.table_dossiers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_dossiers.setSortingEnabled(True)
        self.table_dossiers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_dossiers.cellDoubleClicked.connect(self.ouvrir_emplacement)
        layout_dos.addWidget(self.table_dossiers)


# ✅ Menu contextuel pour copier uniquement le chemin
        self.table_dossiers.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_dossiers.customContextMenuRequested.connect(
            self.menu_contextuel_dossiers)

        # --- Onglet Analyse Disque ---
        tab_disque = QWidget()
        layout_disque = QVBoxLayout(tab_disque)
        self.tabs.addTab(tab_disque, "📊 Analyse Disque")

        btn_layout_disk = QHBoxLayout()
        self.btn_analyze_disk = QPushButton("Analyser l'espace disque")
        self.btn_analyze_disk.clicked.connect(self.lancer_analyse_disque)
        self.label_disk_min_size = QLabel("Taille min (Mo):")
        self.entry_disk_min_size = QLineEdit("100")
        self.entry_disk_min_size.setMaximumWidth(80)
        btn_layout_disk.addWidget(self.btn_analyze_disk)
        btn_layout_disk.addWidget(self.label_disk_min_size)
        btn_layout_disk.addWidget(self.entry_disk_min_size)
        self.progress_disk = QProgressBar()
        btn_layout_disk.addWidget(self.progress_disk)
        layout_disque.addLayout(btn_layout_disk)

        # Informations partitions
        self.text_partitions = QTextEdit()
        self.text_partitions.setReadOnly(True)
        self.text_partitions.setMaximumHeight(150)
        layout_disque.addWidget(QLabel("Informations des partitions:"))
        layout_disque.addWidget(self.text_partitions)

        # Tableau gros fichiers
        self.table_gros_fichiers = QTableWidget(0, 4)
        self.table_gros_fichiers.setHorizontalHeaderLabels(
            ["Fichier", "Chemin", "Taille", "Date modification"])
        self.table_gros_fichiers.horizontalHeader(
        ).setSectionResizeMode(QHeaderView.Stretch)
        self.table_gros_fichiers.setSortingEnabled(True)
        self.table_gros_fichiers.setEditTriggers(
            QAbstractItemView.NoEditTriggers)
        layout_disque.addWidget(QLabel("Gros fichiers:"))
        layout_disque.addWidget(self.table_gros_fichiers)

        # --- Onglet Nettoyage ---
        tab_cleanup = QWidget()
        layout_cleanup = QVBoxLayout(tab_cleanup)
        self.tabs.addTab(tab_cleanup, "🗑️ Nettoyage")

        layout_cleanup.addWidget(
            QLabel("Sélectionnez les éléments à nettoyer:"))

        self.check_temp_windows = QCheckBox(
            "Fichiers temporaires Windows (Temp)")
        self.check_temp_windows.setChecked(True)
        self.check_temp_user = QCheckBox("Fichiers temporaires utilisateur")
        self.check_temp_user.setChecked(True)
        self.check_prefetch = QCheckBox("Prefetch (requiert droits admin)")
        self.check_recycle_bin = QCheckBox("Vider la corbeille")
        self.check_browser_cache = QCheckBox("Cache des navigateurs")

        layout_cleanup.addWidget(self.check_temp_windows)
        layout_cleanup.addWidget(self.check_temp_user)
        layout_cleanup.addWidget(self.check_prefetch)
        layout_cleanup.addWidget(self.check_recycle_bin)
        layout_cleanup.addWidget(self.check_browser_cache)

        btn_layout_cleanup = QHBoxLayout()
        self.btn_cleanup = QPushButton("Lancer le nettoyage")
        self.btn_cleanup.clicked.connect(self.lancer_nettoyage)
        btn_layout_cleanup.addWidget(self.btn_cleanup)
        self.progress_cleanup = QProgressBar()
        btn_layout_cleanup.addWidget(self.progress_cleanup)
        layout_cleanup.addLayout(btn_layout_cleanup)

        self.label_cleanup_status = QLabel("")
        layout_cleanup.addWidget(self.label_cleanup_status)

        self.text_cleanup_results = QTextEdit()
        self.text_cleanup_results.setReadOnly(True)
        layout_cleanup.addWidget(QLabel("Résultats du nettoyage:"))
        layout_cleanup.addWidget(self.text_cleanup_results)

        # --- Onglet Sécurité ---
        tab_security = QWidget()
        layout_security = QVBoxLayout(tab_security)
        self.tabs.addTab(tab_security, "🔐 Analyse Sécurité")

        btn_layout_security = QHBoxLayout()
        self.btn_analyze_security = QPushButton("Analyser la sécurité")
        self.btn_analyze_security.clicked.connect(self.lancer_analyse_securite)
        btn_layout_security.addWidget(self.btn_analyze_security)
        self.progress_security = QProgressBar()
        btn_layout_security.addWidget(self.progress_security)
        layout_security.addLayout(btn_layout_security)

        # Programmes au démarrage
        layout_security.addWidget(QLabel("⏰ Programmes au démarrage:"))
        self.table_startup = QTableWidget(0, 2)
        self.table_startup.setHorizontalHeaderLabels(["Nom", "Chemin"])
        self.table_startup.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_startup.setMaximumHeight(200)
        self.table_startup.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout_security.addWidget(self.table_startup)

        # Programmes obsolètes
        layout_security.addWidget(
            QLabel("⚠️ Programmes potentiellement obsolètes:"))
        self.table_obsolete = QTableWidget(0, 3)
        self.table_obsolete.setHorizontalHeaderLabels(
            ["Programme", "Version", "Raison"])
        self.table_obsolete.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_obsolete.setMaximumHeight(200)
        self.table_obsolete.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout_security.addWidget(self.table_obsolete)

        # Services suspects
        layout_security.addWidget(QLabel("🔍 Services suspects:"))
        self.table_services = QTableWidget(0, 3)
        self.table_services.setHorizontalHeaderLabels(
            ["Service", "Description", "Remarque"])
        self.table_services.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_services.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout_security.addWidget(self.table_services)

        # ✅ Configuration des polices (après création de tous les widgets)
        self._setup_fonts()

    # ✅ Fonctions principales

# ✅ Fonctions principales

    def menu_contextuel_programmes(self, pos):
        menu = QMenu()
        copier_action = menu.addAction("Copier le chemin")
        action = menu.exec_(self.table_programmes.viewport().mapToGlobal(pos))
        if action == copier_action:
            ligne = self.table_programmes.currentRow()
            texte = self.table_programmes.item(
                ligne, 2).text()  # Colonne Chemin
            QApplication.clipboard().setText(texte)

    def menu_contextuel_dossiers(self, pos):
        menu = QMenu()
        copier_action = menu.addAction("Copier le chemin")
        action = menu.exec_(self.table_dossiers.viewport().mapToGlobal(pos))
        if action == copier_action:
            ligne = self.table_dossiers.currentRow()
            texte = self.table_dossiers.item(
                ligne, 0).text()  # Colonne Dossier
            QApplication.clipboard().setText(texte)

    def show_about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("À propos")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Outil Maintenance : Auteur: c.Lecomte Vers. 1.0.2")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setTextInteractionFlags(Qt.NoTextInteraction)
        msg.exec_()

    def parcourir_dossier(self):
        chemin = QFileDialog.getExistingDirectory(
            self, "Sélectionner un dossier")
        if chemin:
            self.entry_path.setText(chemin)

    def lancer_scan_dossiers(self):
        chemin = self.entry_path.text()
        if not chemin:
            QMessageBox.critical(
                self, "Erreur", "Veuillez sélectionner un dossier.")
            return
        self.progress_bar.setValue(0)
        self.table_dossiers.setRowCount(0)
        self.scan_thread = ScanThread(chemin)
        self.scan_thread.progress.connect(self.progress_bar.setValue)
        self.scan_thread.finished.connect(self.afficher_resultats_dossiers)
        self.scan_thread.start()

    def afficher_resultats_dossiers(self, resultats):
        """Affiche les résultats du scan de dossiers vides dans le tableau."""
        self.dossiers_vides = resultats
        self.table_dossiers.setSortingEnabled(False)
        if self.dossiers_vides:
            self.table_dossiers.setRowCount(len(self.dossiers_vides))
            for row, (dossier, taille) in enumerate(self.dossiers_vides):
                self.table_dossiers.setItem(row, 0, QTableWidgetItem(dossier))
                self.table_dossiers.setItem(row, 1, QTableWidgetItem(taille))
            self.table_dossiers.setSortingEnabled(True)
            logging.info(f"{len(self.dossiers_vides)} dossiers vides trouvés.")
        else:
            QMessageBox.information(self, "Info", "Aucun dossier vide trouvé.")

    def lancer_scan_programmes(self):
        self.progress_prog.setValue(0)
        self.table_programmes.setRowCount(0)
        self.program_thread = ProgramThread()
        self.program_thread.progress.connect(self.progress_prog.setValue)
        self.program_thread.finished.connect(
            self.afficher_resultats_programmes)
        self.program_thread.start()

    def afficher_resultats_programmes(self, programmes):
        """Affiche les programmes installés dans le tableau."""
        self.tous_les_programmes = programmes
        self.table_programmes.setSortingEnabled(False)
        if self.tous_les_programmes:
            self.table_programmes.setRowCount(len(self.tous_les_programmes))
            for row, prog in enumerate(self.tous_les_programmes):
                for col, val in enumerate(prog):
                    self.table_programmes.setItem(
                        row, col, QTableWidgetItem(val))
            self.table_programmes.setSortingEnabled(True)
            logging.info(
                f"{len(self.tous_les_programmes)} programmes trouvés.")
        else:
            QMessageBox.information(
                self, "Info", "Aucun programme trouvé ou système non supporté.")

    def filtrer_programmes(self):
        """Filtre les programmes affichés selon les critères de recherche."""
        texte = self.entry_filter.text().lower().strip()
        filtre_type = self.combo_filter.currentText()
        self.table_programmes.setRowCount(0)
        for prog in self.tous_les_programmes:
            nom, version, chemin = prog
            chemin_normalise = os.path.normpath(
                os.path.abspath(chemin)).lower() if chemin else ""
            match = False
            if filtre_type == "Tous":
                match = (fnmatch.fnmatch(nom.lower(), f"*{texte}*") or fnmatch.fnmatch(
                    version.lower(), f"*{texte}*") or fnmatch.fnmatch(chemin_normalise, f"*{texte}*"))
            elif filtre_type == "Programme":
                match = fnmatch.fnmatch(nom.lower(), f"*{texte}*")
            elif filtre_type == "Version":
                match = fnmatch.fnmatch(version.lower(), f"*{texte}*")
            elif filtre_type == "Chemin":
                match = fnmatch.fnmatch(chemin_normalise, f"*{texte}*")
            if match:
                row = self.table_programmes.rowCount()
                self.table_programmes.insertRow(row)
                for col, val in enumerate(prog):
                    self.table_programmes.setItem(
                        row, col, QTableWidgetItem(val))

    def lancer_recherche_globale(self):
        """Lance une recherche globale de fichiers sur le disque C:\\."""
        mot_cle, ok = QInputDialog.getText(
            self, "Recherche globale",
            "Entrer le mot-clé à rechercher:\n(Attention: cette opération peut être longue)")

        if not ok or not mot_cle or len(mot_cle.strip()) < 2:
            QMessageBox.warning(
                self, "Info", "Veuillez entrer un mot-clé valide (au moins 2 caractères).")
            return

        confirm = QMessageBox.question(
            self, "Confirmation",
            f"La recherche de '{mot_cle}' sur tout le disque C:\\ peut prendre plusieurs minutes.\n"
            f"Les résultats seront limités aux {GlobalSearchThread.MAX_RESULTS} premiers fichiers trouvés.\n\n"
            "Voulez-vous continuer ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        self.progress_prog.setValue(0)
        self.global_thread = GlobalSearchThread(mot_cle.strip())
        self.global_thread.progress.connect(self.progress_prog.setValue)
        self.global_thread.finished.connect(self.afficher_resultats_globaux)
        self.global_thread.start()
        logging.info(f"Recherche globale lancée pour: {mot_cle}")

    def afficher_resultats_globaux(self, resultats):
        """Affiche les résultats de la recherche globale."""
        if not resultats:
            QMessageBox.information(self, "Info", "Aucun fichier trouvé.")
            return

        message_limite = ""
        if len(resultats) >= GlobalSearchThread.MAX_RESULTS:
            message_limite = f"\n\n⚠️ Limite de {GlobalSearchThread.MAX_RESULTS} résultats atteinte. Affinez votre recherche pour voir plus de fichiers."

        # Limiter l'affichage à 50 résultats dans la boîte de dialogue
        texte = "\n".join(resultats[:50])
        if len(resultats) > 50:
            texte += f"\n\n... et {len(resultats) - 50} autres fichiers"

        QMessageBox.information(
            self, "Résultats",
            f"Fichiers trouvés ({len(resultats)} total):\n{texte}{message_limite}")
        logging.info(f"Recherche terminée: {len(resultats)} fichiers trouvés.")

    def desinstaller_programme(self):
        """Désinstalle le programme sélectionné dans le tableau."""
        selection = self.table_programmes.selectionModel().selectedRows()
        if not selection:
            QMessageBox.warning(
                self, "Attention",
                "Veuillez sélectionner un programme à désinstaller.")
            return

        # Récupérer le nom du programme sélectionné
        row = selection[0].row()
        programme_nom = self.table_programmes.item(row, 0).text()
        programme_version = self.table_programmes.item(row, 1).text() if self.table_programmes.item(row, 1) else "N/A"

        # Demander confirmation
        confirm = QMessageBox.question(
            self, "Confirmation de désinstallation",
            f"⚠️ ATTENTION ⚠️\n\n"
            f"Vous êtes sur le point de désinstaller :\n\n"
            f"Programme : {programme_nom}\n"
            f"Version : {programme_version}\n\n"
            f"Cette action peut ne pas être réversible.\n"
            f"Voulez-vous continuer ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        # Lancer la désinstallation
        self.progress_prog.setValue(0)
        self.btn_uninstall.setEnabled(False)
        
        self.uninstall_thread = UninstallThread(programme_nom, programme_nom)
        self.uninstall_thread.progress.connect(self.update_uninstall_progress)
        self.uninstall_thread.finished.connect(self.afficher_resultat_desinstallation)
        self.uninstall_thread.start()
        logging.info(f"Désinstallation lancée pour: {programme_nom}")

    def update_uninstall_progress(self, value, message):
        """Met à jour la progression de la désinstallation."""
        self.progress_prog.setValue(value)
        self.statusBar().showMessage(message, 3000)

    def afficher_resultat_desinstallation(self, success, message):
        """Affiche le résultat de la désinstallation."""
        self.btn_uninstall.setEnabled(True)
        self.progress_prog.setValue(0)
        
        if success:
            QMessageBox.information(
                self, "Succès",
                f"✅ {message}\n\nLa liste des programmes va être actualisée.")
            logging.info(f"Désinstallation réussie: {message}")
            # Rafraîchir automatiquement la liste des programmes
            self.lancer_scan_programmes()
        else:
            QMessageBox.critical(
                self, "Erreur",
                f"❌ Échec de la désinstallation\n\n{message}\n\n"
                f"Note: Certains programmes nécessitent des droits administrateur ou un désinstalleur manuel.")
            logging.error(f"Échec désinstallation: {message}")

    def ouvrir_programme(self, row, col):
        """Ouvre l'emplacement du programme sélectionné."""
        chemin = self.table_programmes.item(row, 2).text()
        try:
            if chemin.startswith("http://") or chemin.startswith("https://"):
                webbrowser.open(chemin)
            elif chemin and os.path.exists(chemin):
                if platform.system() == "Windows":
                    os.startfile(chemin)
                else:
                    subprocess.run(["xdg-open", chemin], check=True)
            else:
                QMessageBox.warning(self, "Attention",
                                    "Chemin introuvable ou lien invalide.")
        except (OSError, subprocess.SubprocessError) as e:
            QMessageBox.critical(
                self, "Erreur", f"Impossible d'ouvrir le chemin: {e}")
            logging.error(f"Erreur lors de l'ouverture: {e}")

    def ouvrir_emplacement(self, row, col):
        """Ouvre le dossier sélectionné dans l'explorateur."""
        dossier = self.table_dossiers.item(row, 0).text()
        try:
            if os.path.exists(dossier):
                if platform.system() == "Windows":
                    os.startfile(dossier)
                else:
                    subprocess.run(["xdg-open", dossier], check=True)
            else:
                QMessageBox.warning(self, "Attention", "Dossier introuvable.")
        except (OSError, subprocess.SubprocessError) as e:
            QMessageBox.critical(
                self, "Erreur", f"Impossible d'ouvrir le dossier: {e}")
            logging.error(f"Erreur lors de l'ouverture: {e}")

    def lancer_analyse_disque(self):
        """Lance l'analyse de l'espace disque et la recherche de gros fichiers."""
        try:
            taille_min = int(self.entry_disk_min_size.text())
        except ValueError:
            QMessageBox.warning(
                self, "Erreur", "Veuillez entrer une taille valide en Mo.")
            return

        confirm = QMessageBox.question(
            self, "Confirmation",
            f"L'analyse va rechercher tous les fichiers de plus de {taille_min} Mo.\n"
            "Cette opération peut prendre plusieurs minutes.\n\n"
            "Continuer ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        self.progress_disk.setValue(0)
        self.table_gros_fichiers.setRowCount(0)
        self.text_partitions.clear()

        self.disk_thread = DiskAnalysisThread("C:\\", taille_min)
        self.disk_thread.progress.connect(self.progress_disk.setValue)
        self.disk_thread.finished.connect(self.afficher_resultats_disque)
        self.disk_thread.start()
        logging.info(f"Analyse disque lancée (taille min: {taille_min} Mo)")

    def afficher_resultats_disque(self, resultats):
        """Affiche les résultats de l'analyse disque."""
        self.disk_data = resultats

        # Afficher les partitions
        info_partitions = "=== PARTITIONS ===\n\n"
        for part in resultats['partitions']:
            total_gb = part['total'] / (1024**3)
            utilise_gb = part['utilise'] / (1024**3)
            libre_gb = part['libre'] / (1024**3)

            info_partitions += f"💾 Disque {part['nom']}:\n"
            info_partitions += f"   Total: {total_gb:.2f} Go\n"
            info_partitions += f"   Utilisé: {utilise_gb:.2f} Go ({part['pourcentage']:.1f}%)\n"
            info_partitions += f"   Libre: {libre_gb:.2f} Go\n"
            info_partitions += f"   {'🔴' if part['pourcentage'] > 90 else '🟡' if part['pourcentage'] > 75 else '🟢'}\n\n"

        self.text_partitions.setPlainText(info_partitions)

        # Afficher les gros fichiers
        self.table_gros_fichiers.setSortingEnabled(False)
        if resultats['gros_fichiers']:
            self.table_gros_fichiers.setRowCount(
                len(resultats['gros_fichiers']))
            for row, fichier in enumerate(resultats['gros_fichiers']):
                self.table_gros_fichiers.setItem(
                    row, 0, QTableWidgetItem(fichier['nom']))
                self.table_gros_fichiers.setItem(
                    row, 1, QTableWidgetItem(fichier['chemin']))

                taille_mb = fichier['taille'] / (1024**2)
                if taille_mb >= 1024:
                    taille_str = f"{taille_mb / 1024:.2f} Go"
                else:
                    taille_str = f"{taille_mb:.2f} Mo"
                self.table_gros_fichiers.setItem(
                    row, 2, QTableWidgetItem(taille_str))

                date_str = fichier['date_modif'].strftime("%Y-%m-%d %H:%M")
                self.table_gros_fichiers.setItem(
                    row, 3, QTableWidgetItem(date_str))

            self.table_gros_fichiers.setSortingEnabled(True)
            logging.info(
                f"{len(resultats['gros_fichiers'])} gros fichiers trouvés.")
        else:
            QMessageBox.information(self, "Info", "Aucun gros fichier trouvé.")

    def lancer_nettoyage(self):
        """Lance le nettoyage du système selon les options sélectionnées."""
        options = {
            'temp_windows': self.check_temp_windows.isChecked(),
            'temp_user': self.check_temp_user.isChecked(),
            'prefetch': self.check_prefetch.isChecked(),
            'recycle_bin': self.check_recycle_bin.isChecked(),
            'browser_cache': self.check_browser_cache.isChecked()
        }

        if not any(options.values()):
            QMessageBox.warning(self, "Attention",
                                "Veuillez sélectionner au moins une option.")
            return

        confirm = QMessageBox.question(
            self, "Confirmation",
            "⚠️ ATTENTION ⚠️\n\n"
            "Le nettoyage va supprimer définitivement des fichiers.\n"
            "Certaines applications devront peut-être être redémarrées.\n\n"
            "Voulez-vous continuer ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        self.progress_cleanup.setValue(0)
        self.text_cleanup_results.clear()
        self.label_cleanup_status.setText("Nettoyage en cours...")

        self.cleanup_thread = CleanupThread(options)
        self.cleanup_thread.progress.connect(self.update_cleanup_progress)
        self.cleanup_thread.finished.connect(self.afficher_resultats_nettoyage)
        self.cleanup_thread.start()
        logging.info("Nettoyage lancé")

    def update_cleanup_progress(self, value, message):
        """Met à jour la progression du nettoyage."""
        self.progress_cleanup.setValue(value)
        self.label_cleanup_status.setText(message)

    def afficher_resultats_nettoyage(self, resultats):
        """Affiche les résultats du nettoyage."""
        self.label_cleanup_status.setText("Nettoyage terminé !")

        espace_mb = resultats['espace_libere'] / (1024**2)
        if espace_mb >= 1024:
            espace_str = f"{espace_mb / 1024:.2f} Go"
        else:
            espace_str = f"{espace_mb:.2f} Mo"

        rapport = f"=== RAPPORT DE NETTOYAGE ===\n\n"
        rapport += f"✅ Fichiers supprimés: {resultats['fichiers_supprimes']}\n"
        rapport += f"💾 Espace libéré: {espace_str}\n"
        rapport += f"❌ Erreurs: {resultats['erreurs']}\n\n"

        if resultats['details']:
            rapport += "=== DÉTAILS ===\n\n"
            # Limiter à 100 lignes pour éviter la surcharge
            for detail in resultats['details'][:100]:
                rapport += f"• {detail}\n"
            if len(resultats['details']) > 100:
                rapport += f"\n... et {len(resultats['details']) - 100} autres opérations"

        self.text_cleanup_results.setPlainText(rapport)

        QMessageBox.information(
            self, "Nettoyage terminé",
            f"✅ Nettoyage réussi !\n\n"
            f"Fichiers supprimés: {resultats['fichiers_supprimes']}\n"
            f"Espace libéré: {espace_str}\n"
            f"Erreurs: {resultats['erreurs']}"
        )
        logging.info(
            f"Nettoyage terminé: {espace_str} libérés, {resultats['fichiers_supprimes']} fichiers")

    def lancer_analyse_securite(self):
        """Lance l'analyse de sécurité du système."""
        confirm = QMessageBox.question(
            self, "Confirmation",
            "L'analyse de sécurité va examiner:\n"
            "• Les programmes au démarrage\n"
            "• Les logiciels potentiellement obsolètes\n"
            "• Les services Windows suspects\n\n"
            "Cette opération peut prendre quelques minutes.\n\n"
            "Continuer ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        self.progress_security.setValue(0)
        self.table_startup.setRowCount(0)
        self.table_obsolete.setRowCount(0)
        self.table_services.setRowCount(0)

        self.security_thread = SecurityAnalysisThread()
        self.security_thread.progress.connect(self.progress_security.setValue)
        self.security_thread.finished.connect(self.afficher_resultats_securite)
        self.security_thread.start()
        logging.info("Analyse de sécurité lancée")

    def afficher_resultats_securite(self, resultats):
        """Affiche les résultats de l'analyse de sécurité."""
        self.security_data = resultats

        # Programmes au démarrage
        self.table_startup.setSortingEnabled(False)
        if resultats['programmes_demarrage']:
            self.table_startup.setRowCount(
                len(resultats['programmes_demarrage']))
            for row, prog in enumerate(resultats['programmes_demarrage']):
                self.table_startup.setItem(
                    row, 0, QTableWidgetItem(prog['nom']))
                self.table_startup.setItem(
                    row, 1, QTableWidgetItem(prog['chemin']))
            self.table_startup.setSortingEnabled(True)

        # Programmes obsolètes
        self.table_obsolete.setSortingEnabled(False)
        if resultats['programmes_obsoletes']:
            self.table_obsolete.setRowCount(
                len(resultats['programmes_obsoletes']))
            for row, prog in enumerate(resultats['programmes_obsoletes']):
                self.table_obsolete.setItem(
                    row, 0, QTableWidgetItem(prog['nom']))
                self.table_obsolete.setItem(
                    row, 1, QTableWidgetItem(prog['version']))
                self.table_obsolete.setItem(
                    row, 2, QTableWidgetItem(prog['raison']))
            self.table_obsolete.setSortingEnabled(True)

        # Services suspects
        self.table_services.setSortingEnabled(False)
        if resultats['services_suspects']:
            self.table_services.setRowCount(
                len(resultats['services_suspects']))
            for row, service in enumerate(resultats['services_suspects']):
                self.table_services.setItem(
                    row, 0, QTableWidgetItem(service['service']))
                self.table_services.setItem(
                    row, 1, QTableWidgetItem(service['description']))
                self.table_services.setItem(
                    row, 2, QTableWidgetItem(service['remarque']))
            self.table_services.setSortingEnabled(True)

        # Résumé
        nb_startup = len(resultats['programmes_demarrage'])
        nb_obsoletes = len(resultats['programmes_obsoletes'])
        nb_services = len(resultats['services_suspects'])

        message = f"Analyse de sécurité terminée !\n\n"
        message += f"📊 Programmes au démarrage: {nb_startup}\n"
        message += f"⚠️ Programmes obsolètes: {nb_obsoletes}\n"
        message += f"🔍 Services suspects: {nb_services}\n"

        if nb_obsoletes > 0 or nb_services > 0:
            message += "\n⚠️ Attention: Des éléments nécessitent votre vigilance."

        QMessageBox.information(self, "Analyse terminée", message)
        logging.info(
            f"Analyse sécurité terminée: {nb_startup} démarrage, {nb_obsoletes} obsolètes, {nb_services} services")

    def supprimer_selection(self):
        """Supprime les dossiers vides sélectionnés."""
        selection = self.table_dossiers.selectionModel().selectedRows()
        if not selection:
            QMessageBox.information(
                self, "Info", "Veuillez sélectionner au moins un dossier.")
            return

        confirm = QMessageBox.question(
            self, "Confirmation",
            f"Voulez-vous supprimer définitivement {len(selection)} dossiers vides ?\n\n"
            "⚠️ Cette action est irréversible !",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            supprime = 0
            erreurs = 0
            for index in sorted(selection, reverse=True):  # Supprimer en ordre inverse
                dossier = self.table_dossiers.item(index.row(), 0).text()
                try:
                    os.rmdir(dossier)
                    self.table_dossiers.removeRow(index.row())
                    supprime += 1
                    logging.info(f"Dossier supprimé: {dossier}")
                except (OSError, PermissionError) as e:
                    erreurs += 1
                    logging.error(f"Impossible de supprimer {dossier}: {e}")

            msg = f"{supprime} dossier(s) supprimé(s)."
            if erreurs > 0:
                msg += f"\n{erreurs} erreur(s) rencontrée(s)."
            QMessageBox.information(self, "Résultat", msg)

    def exporter_liste(self):
        """Exporte la liste des dossiers vides dans un fichier texte."""
        if not self.dossiers_vides:
            QMessageBox.information(self, "Info", "Aucune liste à exporter.")
            return

        fichier, _ = QFileDialog.getSaveFileName(
            self, "Exporter la liste", "", "Fichier texte (*.txt)")
        if fichier:
            try:
                with open(fichier, "w", encoding="utf-8") as f:
                    f.write(
                        f"Liste des dossiers vides - {len(self.dossiers_vides)} dossiers\n")
                    f.write("=" * 80 + "\n\n")
                    for dossier, taille in self.dossiers_vides:
                        f.write(f"{dossier}\n Taille: {taille}\n\n")
                QMessageBox.information(
                    self, "Succès", f"Liste exportée dans : {fichier}")
                logging.info(f"Liste exportée: {fichier}")
            except (OSError, IOError) as e:
                QMessageBox.critical(
                    self, "Erreur", f"Impossible d'exporter la liste: {e}")
                logging.error(f"Erreur d'export: {e}")

    def exporter_programmes_pdf(self):
        """Exporte la liste des programmes installés en PDF."""
        if not self.tous_les_programmes:
            QMessageBox.information(
                self, "Info", "Aucun programme à exporter.")
            return

        fichier, _ = QFileDialog.getSaveFileName(
            self, "Exporter en PDF", "", "Fichier PDF (*.pdf)")
        if fichier:
            try:
                doc = SimpleDocTemplate(
                    fichier, pagesize=A4, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
                styles = getSampleStyleSheet()
                elements = []
                elements.append(
                    Paragraph("Liste des programmes installés", styles['Title']))
                elements.append(Spacer(1, 12))

                data = [["Programme", "Version", "Chemin"]]
                for prog in self.tous_les_programmes:
                    nom = Paragraph(prog[0], styles['Normal'])
                    version = Paragraph(prog[1], styles['Normal'])
                    chemin = Paragraph(prog[2], styles['Normal'])
                    data.append([nom, version, chemin])

                table = Table(data, colWidths=[150, 80, 250])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ]))

                elements.append(table)
                doc.build(elements)
                QMessageBox.information(
                    self, "Succès", f"PDF exporté dans : {fichier}")
            except Exception as e:
                QMessageBox.critical(
                    self, "Erreur", f"Erreur lors de l'export PDF : {e}")

    def exporter_dossiers_pdf(self):
        """Exporte la liste des dossiers vides en PDF."""
        if not self.dossiers_vides:
            QMessageBox.information(self, "Info", "Aucun dossier à exporter.")
            return

        fichier, _ = QFileDialog.getSaveFileName(
            self, "Exporter en PDF", "", "Fichier PDF (*.pdf)")
        if fichier:
            try:
                doc = SimpleDocTemplate(
                    fichier, pagesize=A4, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
                styles = getSampleStyleSheet()
                elements = []
                elements.append(
                    Paragraph("Liste des dossiers vides", styles['Title']))
                elements.append(Spacer(1, 12))

                data = [["Dossier", "Taille"]]
                for dossier, taille in self.dossiers_vides:
                    d = Paragraph(dossier, styles['Normal'])
                    t = Paragraph(taille, styles['Normal'])
                    data.append([d, t])

                table = Table(data, colWidths=[350, 100])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ]))

                elements.append(table)
                doc.build(elements)
                QMessageBox.information(
                    self, "Succès", f"PDF exporté dans : {fichier}")
                logging.info(f"PDF dossiers exporté: {fichier}")
            except Exception as e:
                QMessageBox.critical(
                    self, "Erreur", f"Impossible d'exporter en PDF: {e}")
                logging.error(f"Erreur export PDF dossiers: {e}")

    def closeEvent(self, event):
        """Gère la fermeture de l'application en arrêtant proprement les threads."""
        # Arrêter tous les threads en cours
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
            self.scan_thread.wait(1000)

        if self.program_thread and self.program_thread.isRunning():
            self.program_thread.stop()
            self.program_thread.wait(1000)

        if self.global_thread and self.global_thread.isRunning():
            self.global_thread.stop()
            self.global_thread.wait(1000)

        if self.disk_thread and self.disk_thread.isRunning():
            self.disk_thread.stop()
            self.disk_thread.wait(1000)

        if self.cleanup_thread and self.cleanup_thread.isRunning():
            self.cleanup_thread.stop()
            self.cleanup_thread.wait(1000)

        if self.security_thread and self.security_thread.isRunning():
            self.security_thread.stop()
            self.security_thread.wait(1000)

        if self.uninstall_thread and self.uninstall_thread.isRunning():
            self.uninstall_thread.stop()
            self.uninstall_thread.wait(1000)

        logging.info("Application fermée.")
        event.accept()

    def _setup_fonts(self):
        """Configure les polices et réduit les espacements pour une meilleure apparence."""
        # Augmenter les marges et espacements des layouts
        for layout in self.findChildren(QVBoxLayout):
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(12)

        for layout in self.findChildren(QHBoxLayout):
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(12)

        # Définir les polices principales
        font_normal = QFont("Segoe UI", 9)
        font_normal.setStyleStrategy(QFont.PreferAntialias)

        font_bold = QFont("Segoe UI", 9, QFont.Bold)
        font_bold.setStyleStrategy(QFont.PreferAntialias)

        font_title = QFont("Segoe UI", 10, QFont.Bold)
        font_title.setStyleStrategy(QFont.PreferAntialias)

        font_mono = QFont("Consolas", 8)
        font_mono.setStyleStrategy(QFont.PreferAntialias)

        # Appliquer les polices à la fenêtre principale
        self.setFont(font_normal)

        # Trouver tous les widgets et appliquer les polices appropriées
        for widget in self.findChildren(QLabel):
            widget.setFont(font_normal)

        for widget in self.findChildren(QPushButton):
            widget.setFont(font_bold)

        for widget in self.findChildren(QLineEdit):
            widget.setFont(font_normal)

        for widget in self.findChildren(QTableWidget):
            widget.setFont(font_normal)
            widget.setAlternatingRowColors(True)

        for widget in self.findChildren(QTextEdit):
            widget.setFont(font_mono)

        for widget in self.findChildren(QCheckBox):
            widget.setFont(font_normal)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MaintenanceTool()
    window.show()
    logging.info("Application démarrée.")
    sys.exit(app.exec_())
