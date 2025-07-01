import pandas as pd
import sys
import os
import time
import re
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import random
import traceback

# Configuration de l'encodage pour Windows
if sys.platform.startswith('win'):
    try:
        # Forcer l'encodage UTF-8 pour la console Windows
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # Fallback pour les anciennes versions de Python
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def safe_print(message):
    """Fonction d'impression sécurisée qui gère les problèmes d'encodage"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Remplacer les émojis par des caractères ASCII si problème d'encodage
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)

class ProfileScraper:
    def __init__(self, excel_file=None, slow_mode=False):
        self.data = None
        self.driver = None
        self.slow_mode = slow_mode
        if excel_file and os.path.exists(excel_file):
            try:
                self.data = pd.read_excel(excel_file)
                print(f"Données chargées depuis {excel_file}")
                print(f"Colonnes: {list(self.data.columns)}")
                print(f"Nombre d'entrées: {len(self.data)}")
            except Exception as e:
                print(f"Erreur lors de l'ouverture du fichier Excel: {str(e)}")
        else:
            # Créer un nouveau DataFrame avec les colonnes simplifiées
            self.data = pd.DataFrame(columns=[
                'Intitulé de poste', 
                'Prénom', 
                'Nom', 
                'Entreprise', 
                'LinkedIn',
                'Date d\'ajout',
                'Notes'
            ])
            print("Nouveau fichier de données créé")
    
    def setup_browser(self):
        """Configure le navigateur pour le scraping avec techniques anti-CAPTCHA"""
        chrome_options = Options()
        
        # Techniques anti-détection pour éviter les CAPTCHAs
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent réaliste
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # Autres options pour paraître plus humain
        chrome_options.add_argument("--window-size=1366,768")  # Taille d'écran commune
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
        # Mode sans interface (décommentez si nécessaire)
        # chrome_options.add_argument("--headless=new")  # Nouveau mode headless Chrome
        
        try:
            print("🔧 Initialisation du navigateur avec techniques anti-détection...")
            
            # Trouver Chrome
            chrome_paths = [
                "C:/Program Files/Google/Chrome/Application/chrome.exe",
                "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
            ]
            
            if os.environ.get("LOCALAPPDATA"):
                chrome_paths.append(os.environ.get("LOCALAPPDATA") + "/Google/Chrome/Application/chrome.exe")
            
            chrome_path = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    print(f"✓ Chrome trouvé à: {path}")
                    break
            
            if chrome_path:
                chrome_options.binary_location = chrome_path
                self.driver = webdriver.Chrome(options=chrome_options)
                
                # Script pour masquer l'automatisation
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                print("✅ Navigateur initialisé avec succès (mode anti-détection)")
                return True
            else:
                print("❌ Chrome n'a pas été trouvé dans les emplacements standards")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation du navigateur: {str(e)}")
            print("🔄 Tentative de basculement en mode simulation...")
            return False
    
    def search_linkedin_with_delays(self, job_title, num_results=5):
        """Recherche LinkedIn avec délais humains pour éviter les CAPTCHAs"""
        if not self.driver:
            if not self.setup_browser():
                print("⚠️  Navigateur non disponible, la recherche ne peut pas continuer")
                return []
        
        results = []
        search_query = f"{job_title}"
        
        # Déterminer les délais en fonction du mode
        base_delay = 5 if self.slow_mode else 3
        search_delay = 8 if self.slow_mode else 4
        load_delay = 10 if self.slow_mode else 5
        
        try:
            print(f"🔍 Recherche Google pour: {search_query}")
            
            # Aller d'abord sur Google pour établir une session normale
            print("📄 Chargement de Google...")
            self.driver.get("https://www.google.com")
            time.sleep(base_delay)  # Délai humain
            
            # Gérer le consentement aux cookies si nécessaire
            try:
                consent_buttons = [
                    "//button[contains(., 'Tout accepter')]",
                    "//button[contains(., 'Accept all')]", 
                    "//button[contains(., 'J\\'accepte')]"
                ]
                for button_xpath in consent_buttons:
                    try:
                        consent_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, button_xpath))
                        )
                        consent_button.click()
                        print("✓ Consentement cookies accepté")
                        time.sleep(2)
                        break
                    except:
                        continue
            except:
                print("ℹ  Pas de popup de consentement")
            
            # Chercher la barre de recherche et taper comme un humain
            try:
                search_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "q"))
                )
                
                # Effacer et taper lentement comme un humain
                search_box.clear()
                search_text = f"site:linkedin.com/in/ {search_query}"
                
                for char in search_text:
                    search_box.send_keys(char)
                    time.sleep(0.1 + (0.05 * __import__('random').random()))  # Délai de frappe humain
                
                print(f"🔤 Recherche tapée: {search_text}")
                time.sleep(1)
                
                # Appuyer sur Entrée
                search_box.send_keys('\n')
                time.sleep(4)  # Attendre les résultats
                
            except Exception as e:
                print(f"❌ Erreur lors de la saisie: {str(e)}")
                print("🔄 Tentative avec URL directe...")
                encoded_query = search_query.replace(' ', '+')
                self.driver.get(f"https://www.google.com/search?q=site:linkedin.com/in/+{encoded_query}")
                time.sleep(5)
            
            # Vérifier s'il y a un CAPTCHA
            if "captcha" in self.driver.page_source.lower() or "unusual traffic" in self.driver.page_source.lower():
                print("🚫 CAPTCHA détecté ! La recherche ne peut pas continuer.")
                return []
            
            print("📊 Analyse des résultats...")
            
            # Capture d'écran pour débogage si nécessaire
            screenshot_path = f"search_results_{job_title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Capture d'écran enregistrée: {screenshot_path}")
            
            # Détecter et explorer les résultats avec une approche multistratégie
            found_linkedin_links = self._extract_linkedin_links()
            
            if not found_linkedin_links:
                print("⚠️  Aucun lien LinkedIn trouvé dans les résultats.")
                return []
            
            print(f"✓ {len(found_linkedin_links)} liens LinkedIn trouvés")
            
            count = 0
            for i, link_info in enumerate(found_linkedin_links):
                if count >= num_results:
                    break
                
                try:
                    print(f"  📄 Analyse du profil {i+1}...")
                    
                    # Extraire les informations en utilisant l'élément parent complet
                    profile_info = self._extract_profile_from_result(link_info, job_title)
                    
                    # Ne pas ajouter de profil si les informations sont trop incomplètes
                    if not profile_info.get('Prénom') or not profile_info.get('Nom') or not profile_info.get('Entreprise'):
                        safe_print(f"   ❌ Profil ignoré car informations incomplètes: {link_info.get('url', '')}")
                        continue  # Passer au profil suivant
                    
                    results.append(profile_info)
                    count += 1
                    print(f"    ✓ Profil extrait: {profile_info['Prénom']} {profile_info['Nom']} chez {profile_info['Entreprise']}")
                    
                    # Délai entre chaque extraction
                    time.sleep(1 + (0.5 * __import__('random').random()))
                    
                except Exception as e:
                    print(f"    ⚠️  Erreur lors de l'extraction du profil {i+1}: {str(e)}")
                    traceback.print_exc()
                    continue
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche: {str(e)}")
            print("La recherche ne peut pas continuer.")
            traceback.print_exc()
            return []
    
    def _extract_linkedin_links(self):
        """Extrait les liens LinkedIn des résultats de recherche avec plusieurs stratégies"""
        linkedin_links = []
        
        # STRATÉGIE 1: Essayer de trouver tous les résultats avec les sélecteurs modernes 2024
        result_selectors = [
            "#search div.MjjYud",  # Nouveau sélecteur Google 2024
            "div.g",               # Ancien sélecteur Google classique
            "#rso div.g",          # Variante avec parent
            "#center_col div",     # Plus général
            "[data-hveid]",        # Attribut data spécifique à Google
            "div.v7W49e > div",    # Structure parfois utilisée
            "div.hlcw0c"           # Autre variante
        ]
        
        for selector in result_selectors:
            try:
                results = self.driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"  Tentative avec '{selector}': {len(results)} résultats trouvés")
                
                if results:
                    for result in results:
                        # Essayer d'extraire le lien LinkedIn de ce résultat
                        link_info = self._extract_link_from_result(result)
                        if link_info and link_info.get('url'):
                            linkedin_links.append(link_info)
                    
                    if linkedin_links:
                        print(f"  ✓ {len(linkedin_links)} liens LinkedIn extraits avec le sélecteur '{selector}'")
                        break  # Utiliser cette stratégie si elle fonctionne
            except Exception as e:
                print(f"  ⚠️ Erreur avec le sélecteur '{selector}': {str(e)}")
        
        # STRATÉGIE 2 (fallback): Chercher directement tous les liens LinkedIn
        if not linkedin_links:
            print("  Utilisation de la stratégie de fallback: recherche directe des liens")
            try:
                all_links = self.driver.find_elements(By.TAG_NAME, "a")
                for link in all_links:
                    href = link.get_attribute("href")
                    if href and "linkedin.com/in/" in href:
                        # Essayer d'extraire le texte et le parent
                        link_text = link.text
                        parent_text = ""
                        
                        try:
                            # Remonter pour trouver le bloc parent qui contient ce lien
                            parent = link.find_element(By.XPATH, "./ancestor::div[contains(@class, 'g') or contains(@class, 'MjjYud') or @data-hveid]")
                            if parent:
                                parent_text = parent.text
                        except:
                            # Si on ne peut pas trouver le parent, utiliser le texte du lien uniquement
                            pass
                        
                        linkedin_links.append({
                            'url': href,
                            'element': link,
                            'title': link_text,
                            'full_text': parent_text or link_text
                        })
                
                print(f"  ✓ {len(linkedin_links)} liens LinkedIn trouvés par recherche directe")
            except Exception as e:
                print(f"  ⚠️ Erreur lors de la recherche directe: {str(e)}")
        
        # Filtrer les liens uniques
        unique_links = []
        seen_urls = set()
        
        for link in linkedin_links:
            url = link.get('url', '')
            if url and url not in seen_urls and "linkedin.com/in/" in url:
                seen_urls.add(url)
                unique_links.append(link)
        
        print(f"  ✓ {len(unique_links)} liens LinkedIn uniques trouvés au total")
        return unique_links
    
    def _extract_link_from_result(self, result_element):
        """Extrait un lien LinkedIn et son texte à partir d'un élément de résultat"""
        link_info = {'element': result_element, 'full_text': result_element.text}
        
        # Stratégie 1: Chercher les liens directs
        try:
            links = result_element.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and "linkedin.com/in/" in href:
                    link_info['url'] = href
                    
                    # Essayer d'extraire le titre de différentes manières
                    try:
                        # Méthode 1: h3 dans le lien
                        h3 = link.find_element(By.TAG_NAME, "h3")
                        if h3 and h3.text.strip():
                            link_info['title'] = h3.text.strip()
                    except:
                        pass
                    
                    if not link_info.get('title'):
                        # Méthode 2: titre du lien
                        link_info['title'] = link.text.strip() or link.get_attribute("title") or ""
                    
                    # Si on a un URL et au moins un texte, c'est suffisant
                    if link_info.get('url') and (link_info.get('title') or link_info.get('full_text')):
                        return link_info
        except:
            pass
        
        # Stratégie 2: Chercher les h3 puis remonter aux liens
        try:
            headings = result_element.find_elements(By.TAG_NAME, "h3")
            for heading in headings:
                try:
                    # Remonter au lien parent
                    parent_link = heading.find_element(By.XPATH, "./ancestor::a")
                    href = parent_link.get_attribute("href")
                    if href and "linkedin.com/in/" in href:
                        link_info['url'] = href
                        link_info['title'] = heading.text.strip()
                        return link_info
                except:
                    pass
        except:
            pass
        
        # Si on a trouvé une URL dans les tentatives précédentes, renvoyer ce qu'on a
        if link_info.get('url'):
            return link_info
        
        # Sinon, renvoyer None pour indiquer qu'aucun lien LinkedIn n'a été trouvé
        return None
    
    def _extract_profile_from_result(self, link_info, job_title):
        """Extrait les informations d'un profil à partir d'un résultat de recherche"""
        profile_info = {
            'Intitulé de poste': job_title,
            'LinkedIn': link_info.get('url', ''),
            'Prénom': '',
            'Nom': '',
            'Entreprise': '',
            'Date d\'ajout': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Notes': ''
        }
        
        # Collecter tous les textes disponibles
        heading = link_info.get('title', '').strip()
        full_text = link_info.get('full_text', '').strip()
        
        # Si heading est vide mais full_text ne l'est pas, essayer d'extraire un meilleur heading
        if not heading and full_text:
            # Essayer d'extraire la première ligne ou les premiers caractères
            lines = full_text.split('\n')
            if lines:
                heading = lines[0].strip()
        
        # Si le heading est toujours vide, tenter une dernière extraction directe
        if not heading and link_info.get('element'):
            try:
                # Rechercher un h3 ou tout autre élément de titre
                heading_elements = link_info['element'].find_elements(By.XPATH, 
                    ".//*[self::h3 or contains(@class, 'LC20lb') or contains(@class, 'DKV0Md')]")
                if heading_elements:
                    heading = heading_elements[0].text.strip()
            except:
                pass
        
        # Debug: afficher ce qu'on a trouvé
        print(f"   🔍 Informations trouvées:")
        print(f"     URL: {link_info.get('url', 'N/A')}")
        print(f"     Titre: {heading or 'N/A'}")
        print(f"     Texte complet: {full_text[:100] + '...' if len(full_text) > 100 else full_text or 'N/A'}")
        
        # Si on n'a toujours pas de texte exploitable, on ne peut pas continuer
        if not heading and not full_text:
            print("   ❌ Pas de texte exploitable trouvé, impossible d'extraire les informations")
            return profile_info
        
        # Fonction pour valider si un nom est réaliste
        def is_realistic_name(name):
            """Vérifie si un nom semble réaliste (pas d'artefact d'URL)"""
            if not name or len(name) < 2 or len(name) > 50:
                return False
            
            # Rejeter les noms avec des chiffres
            if re.search(r'\d', name):
                return False
            
            # Rejeter les suites de lettres trop longues (indices d'URLs)
            words = name.replace('-', ' ').replace("'", ' ').split()
            for word in words:
                if len(word) > 15:  # Mot trop long
                    return False
                # Rejeter les mots avec trop de consonnes consécutives (signe d'artefact)
                consonant_count = 0
                for char in word.lower():
                    if char in 'bcdfghjklmnpqrstvwxyz':
                        consonant_count += 1
                        if consonant_count > 4:  # Plus de 4 consonnes consécutives
                            return False
                    else:
                        consonant_count = 0
            
            # Rejeter les noms qui ressemblent à des codes/hashs
            name_clean = re.sub(r'[^a-zA-Z]', '', name.lower())
            if len(name_clean) > 8:
                # Vérifier la diversité des caractères (éviter aaaaabbbb par exemple)
                char_counts = {}
                for char in name_clean:
                    char_counts[char] = char_counts.get(char, 0) + 1
                
                # Si un caractère représente plus de 40% du nom, c'est suspect
                max_char_ratio = max(char_counts.values()) / len(name_clean)
                if max_char_ratio > 0.4:
                    return False
            
            # Vérifier que le nom contient au moins une voyelle
            if not re.search(r'[aeiouAEIOU]', name):
                return False
            
            # Rejeter les suites alphabétiques suspectes (qwerty, abcd, etc.)
            name_lower = name_clean.lower()
            suspicious_patterns = [
                'qwerty', 'azerty', 'abcdef', 'abcd', 'defg', 'qazwsx',
                'zxcvbn', 'mnbvcx', 'asdfgh', 'hjkl', 'poiuy', 'lkjh'
            ]
            for pattern in suspicious_patterns:
                if pattern in name_lower:
                    return False
            
            # Vérifier que ce n'est pas une suite alphabétique
            if len(name_clean) >= 6:
                for i in range(len(name_clean) - 5):
                    substring = name_clean[i:i+6]
                    # Vérifier si c'est une suite consécutive dans l'alphabet
                    is_consecutive = True
                    for j in range(1, len(substring)):
                        if ord(substring[j]) != ord(substring[j-1]) + 1:
                            is_consecutive = False
                            break
                    if is_consecutive:
                        return False
            
            return True
        
        # Fonction pour nettoyer et extraire le nom
        def extract_clean_name(text, is_url_source=False):
            """Extrait et nettoie un nom d'un texte"""
            if not text:
                return ""
            
            # Patterns d'extraction selon la source
            if is_url_source:
                # Pour les URLs, être plus restrictif
                name_patterns = [
                    r"^([a-zA-Z]+(?:-[a-zA-Z]+)*?)(?:-\d|$)",  # Prénom-nom (arrêt avant chiffres)
                    r"^([a-zA-Z]{2,15})$"  # Nom simple sans tirets ni chiffres
                ]
            else:
                # Pour les titres, plus permissif mais plus précis
                name_patterns = [
                    # Pattern exact pour "Prénom Nom - LinkedIn"
                    r"^([A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ\-\']+){1,2})\s*[-–]\s*LinkedIn",
                    # Pattern exact pour "Prénom Nom: Poste" (PRIORITÉ MAXIMALE)
                    r"^([A-Za-zÀ-ÿ]+(?:-[A-Za-zÀ-ÿ]+)?(?:\s+[A-Za-zÀ-ÿ\-\']+){0,2})\s*:",
                    # Pattern SPÉCIAL pour prénoms composés avec tiret + nom + " - " + poste (ex: "Jean-Baptiste Dupont - Poste")
                    r"^([A-Za-zÀ-ÿ]+-[A-Za-zÀ-ÿ]+\s+[A-Za-zÀ-ÿ\-\']+)\s+[-–]\s+",
                    # Pattern pour "Prénom Nom - Titre" (normal sans prénom composé)
                    r"^([A-Za-zÀ-ÿ]+\s+[A-Za-zÀ-ÿ\-\']+)\s*[-–]\s*[^-–]+",
                    # Pattern exact pour "Prénom Nom | Poste"  
                    r"^([A-Za-zÀ-ÿ]+(?:-[A-Za-zÀ-ÿ]+)?(?:\s+[A-Za-zÀ-ÿ\-\']+){0,2})\s*\|",
                    # Pattern pour "Prénom Nom, Poste"
                    r"^([A-Za-zÀ-ÿ]+(?:-[A-Za-zÀ-ÿ]+)?(?:\s+[A-Za-zÀ-ÿ\-\']+){0,2})\s*,",
                    # Pattern pour capturer avant mots-clés de poste (avec priorité sur noms complets)
                    r"^([A-Za-zÀ-ÿ]+(?:-[A-Za-zÀ-ÿ]+)*(?:\s+[A-Za-zÀ-ÿ\-\']+)*)(?:\s+(?:at|chez|@|de|du|CEO|CTO|VP|Manager|Directeur|Engineer|Developer|Consultant|Analyst))",
                    # Pattern pour nom avec titre (ex: "M. Jean Dupont")
                    r"^(?:M\.|Mme|Mr\.|Mrs\.|Dr\.|Pr\.)\s+([A-Za-zÀ-ÿ]+(?:-[A-Za-zÀ-ÿ]+)*(?:\s+[A-Za-zÀ-ÿ\-\']+)*)",
                    # Pattern pour capturer les 2-3 premiers mots si ils ressemblent à un nom
                    r"^([A-Za-zÀ-ÿ]+(?:-[A-Za-zÀ-ÿ]+)?(?:\s+[A-Za-zÀ-ÿ\-\']+){1,2})(?:\s|$)",
                    # Pattern pour nom simple en dernier recours (1 mot seulement)
                    r"^([A-Za-zÀ-ÿ]{3,15})(?:\s|$)"
                ]
            
            for pattern in name_patterns:
                match = re.search(pattern, text.strip(), re.IGNORECASE)
                if match:
                    potential_name = match.group(1).strip()
                    # Limiter à 3 mots maximum pour un nom
                    name_words = potential_name.split()
                    if len(name_words) <= 3 and is_realistic_name(potential_name):
                        return potential_name.title()
            
            return ""
        
        # Essayer d'extraire du titre/heading d'abord (plus fiable)
        clean_name = extract_clean_name(heading, False) if heading else ""
        name_found = bool(clean_name)
        
        # Si pas trouvé dans le titre mais qu'on a du texte complet, essayer avec celui-ci
        if not name_found and full_text:
            # Essayer les premières lignes du texte complet
            lines = full_text.split('\n')
            for line in lines[:3]:  # Essayer les 3 premières lignes
                if line.strip():
                    clean_name = extract_clean_name(line.strip(), False)
                    if clean_name:
                        name_found = True
                        break
        
        # Si toujours pas trouvé, essayer l'URL LinkedIn (en dernier recours)
        if not name_found:
            linkedin_url = link_info.get('url', '')
            if linkedin_url:
                linkedin_match = re.search(r"linkedin\.com/in/([a-zA-Z\-]+)", linkedin_url, re.IGNORECASE)
                if linkedin_match:
                    url_part = linkedin_match.group(1)
                    # Nettoyer et reformater le nom depuis l'URL
                    if '-' in url_part and len(url_part) > 3:
                        # Séparer par tirets et valider chaque partie
                        parts = url_part.split('-')
                        valid_url_parts = []
                        for part in parts:
                            if len(part) >= 2 and part.isalpha() and is_realistic_name(part):
                                valid_url_parts.append(part.capitalize())
                        
                        if len(valid_url_parts) >= 2:
                            # Prendre les 2 premiers comme prénom et nom
                            clean_name = ' '.join(valid_url_parts[:2])
                            name_found = True
                        elif len(valid_url_parts) == 1:
                            # Un seul nom valide, l'utiliser comme prénom
                            clean_name = valid_url_parts[0]
                            name_found = True
                    elif len(url_part) >= 3 and url_part.isalpha() and is_realistic_name(url_part):
                        # URL sans tirets mais nom valide
                        clean_name = url_part.capitalize()
                        name_found = True
        
        # Traitement du nom trouvé
        if name_found and clean_name:
            name_parts = clean_name.split()
            # Double vérification de chaque partie
            valid_parts = []
            for part in name_parts:
                if is_realistic_name(part) and len(part) >= 2:
                    valid_parts.append(part)
            
            if len(valid_parts) >= 1:
                profile_info['Prénom'] = valid_parts[0]
                if len(valid_parts) > 1:
                    profile_info['Nom'] = ' '.join(valid_parts[1:])
                else:
                    profile_info['Nom'] = ''
                print(f"   ✓ Nom extrait: {profile_info['Prénom']} {profile_info['Nom']}")
            else:
                name_found = False
                print("   ❌ Parties du nom invalides")
        else:
            print("   ❌ Aucun nom extrait")
        
        # Fonction pour extraire l'entreprise
        def extract_company(text):
            """Extrait le nom de l'entreprise d'un texte"""
            if not text:
                return ""
            
            company_patterns = [
                # Pattern PRIORITAIRE pour "Prénom Nom - Titre - Entreprise" (ex: "Kévin Moreno - Senior Technical Recruiter - Ubisoft Paris")
                r"^[A-Za-zÀ-ÿ\s\-\']+\s*[-–]\s*[^-–]+\s*[-–]\s*([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+?)(?:\s*$|\s*[-|•])",
                # Patterns spécifiques avec caractères spéciaux français
                r"^[A-Za-zÀ-ÿ\s\-\']+\s*[-–]\s*[^-–]+\s*[-–]\s*([LlDd]['\'][A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+?)(?:\s*$|\s*[-|•])",
                # Patterns avec | pour les titres LinkedIn
                r"\|\s*([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+?)(?:\s*$|\s*[-|•])",
                # Patterns français
                r"(?:chez|Chez)\s+([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+?)(?:\s*[-|•]|\s*$|\s*\|)",
                r"(?:à|À)\s+([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+?)(?:\s*[-|•]|\s*$|\s*\|)",
                r"(?:at|At)\s+([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+?)(?:\s*[-|•]|\s*$|\s*\|)",
                r"(?:@)\s*([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+?)(?:\s*[-|•]|\s*$|\s*\|)",
                # Patterns avec tirets (après nom et titre)
                r"[-–]\s*([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+?)(?:\s*[-|•]|\s*$|\s*\|)",
                # Patterns pour les titres LinkedIn typiques
                r"(?:Director|Manager|Engineer|Analyst|Consultant|Developer|Chef|Responsable|Directeur|Ingénieur|Développeur)\s+(?:at|chez)\s+([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+)",
                # Pattern pour capturer après le nom et titre
                r"(?:CEO|CTO|VP|President|Président|PDG|DG|Gérant)\s+(?:at|chez|de|d')\s*([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+)",
                # Patterns pour description
                r"travaille\s+(?:chez|pour)\s+([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+)",
                r"works\s+(?:at|for)\s+([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+)",
                # Pattern général pour mots capitalisés après certains mots-clés
                r"(?:Company|Société|Entreprise|Groupe|Group)[:,\s]+([A-Za-zÀ-ÿ][a-zA-Z0-9À-ÿ\s&\-\.\']+)"
            ]
            
            for pattern in company_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    company = match.group(1).strip()
                    # Nettoyer le nom de l'entreprise
                    company = re.sub(r'\s+', ' ', company)
                    company = re.sub(r'^(le|la|les|un|une|des|du|de|d\')\s+', '', company, flags=re.IGNORECASE)
                    company = company.strip(' -.,|•')
                    
                    # Vérifications de qualité
                    if (len(company) > 2 and len(company) < 80 and 
                        not re.match(r'^[0-9]+$', company) and
                        not company.lower() in ['linkedin', 'profile', 'profil', 'france', 'paris', 'voir', 'plus'] and
                        not re.match(r'^(voir|see|view|plus|more)', company.lower())):
                        
                        return company
            
            return ""
        
        # Essayer d'extraire l'entreprise à partir du titre et du texte complet
        company = ""
        if heading:
            company = extract_company(heading)
        
        if not company and full_text:
            # Essayer les premières lignes du texte complet
            lines = full_text.split('\n')
            for line in lines[:3]:  # Essayer les 3 premières lignes
                if line.strip():
                    company = extract_company(line.strip())
                    if company:
                        break
        
        # Si l'entreprise a été trouvée, l'ajouter au profil
        if company:
            profile_info['Entreprise'] = company
            print(f"   ✓ Entreprise extraite: {company}")
        else:
            print("   ❌ Aucune entreprise extraite")
        
        return profile_info
    
    def add_profile_to_data(self, profile_info):
        """Ajoute un nouveau profil aux données existantes en évitant les doublons"""
        
        # Vérifier que le profil a les informations essentielles
        if not profile_info.get('Prénom') or not profile_info.get('Nom') or not profile_info.get('Entreprise'):
            safe_print(f"  ❌ Profil incomplet, non ajouté: informations manquantes")
            return False
        
        # Vérifier si le profil existe déjà (basé sur LinkedIn URL)
        if 'LinkedIn' in profile_info and profile_info['LinkedIn']:
            existing = self.data[self.data['LinkedIn'] == profile_info['LinkedIn']]
            if not existing.empty:
                print(f"  ⚠️  Profil déjà existant: {profile_info.get('Prénom', '')} {profile_info.get('Nom', '')} - Ignoré")
                return False
        
        # Vérifier les doublons basés sur nom + entreprise
        if profile_info.get('Prénom') and profile_info.get('Nom') and profile_info.get('Entreprise'):
            existing = self.data[
                (self.data['Prénom'] == profile_info['Prénom']) & 
                (self.data['Nom'] == profile_info['Nom']) & 
                (self.data['Entreprise'] == profile_info['Entreprise'])
            ]
            if not existing.empty:
                print(f"  ⚠️  Profil similaire déjà existant: {profile_info.get('Prénom', '')} {profile_info.get('Nom', '')} - Ignoré")
                return False
        
        # Ajouter le profil aux données
        new_row = pd.DataFrame([profile_info])
        self.data = pd.concat([self.data, new_row], ignore_index=True)
        safe_print(f"  ✓ Profil ajouté: {profile_info.get('Prénom', '')} {profile_info.get('Nom', '')} chez {profile_info.get('Entreprise', '')}")
        safe_print(f"    LinkedIn: {profile_info.get('LinkedIn', '')}")
        return True
    
    def search_by_job_title(self, job_title, max_results=5):
        """Recherche des profils basés sur un intitulé de poste et les ajoute aux données existantes"""
        safe_print(f"\nRecherche de profils pour: {job_title}")
        safe_print(f"Nombre de profils avant recherche: {len(self.data)}")
        
        # Recherche sur LinkedIn avec techniques anti-CAPTCHA
        profiles = self.search_linkedin_with_delays(job_title, max_results)
        
        safe_print(f"Profils trouvés par la recherche: {len(profiles)}")
        
        if not profiles:
            safe_print("Aucun profil trouvé par la recherche!")
            safe_print("La recherche n'a pas pu trouver de profils correspondants.")
        
        # Ajouter la date d'ajout à chaque profil
        for profile in profiles:
            if 'Date d\'ajout' not in profile:
                profile['Date d\'ajout'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            if 'Notes' not in profile:
                profile['Notes'] = ''
            safe_print(f"   Profil trouvé: {profile.get('Prénom', '')} {profile.get('Nom', '')} chez {profile.get('Entreprise', '')}")
        
        # Ajouter les résultats aux données existantes en évitant les doublons
        added_count = 0
        for profile in profiles:
            if self.add_profile_to_data(profile):
                added_count += 1
        
        safe_print(f"{added_count} nouveaux profils ajoutés pour '{job_title}' (sur {len(profiles)} trouvés)")
        safe_print(f"Total de profils maintenant: {len(self.data)}")
        
        return profiles
    
    def save_to_excel(self, output_file="Resultats_Profils.xlsx"):
        """Sauvegarde les données dans un fichier Excel"""
        try:
            safe_print(f"\nSAUVEGARDE EN COURS...")
            safe_print(f"Fichier de destination: {output_file}")
            safe_print(f"Nombre de lignes dans self.data: {len(self.data)}")
            
            if self.data.empty:
                safe_print("ATTENTION: Aucune donnée à sauvegarder!")
                safe_print("   Le DataFrame est vide. Création d'un fichier vide...")
            else:
                safe_print(f"Données à sauvegarder:")
                safe_print(f"   Colonnes: {list(self.data.columns)}")
                safe_print(f"   Premiers profils:")
                for i, row in self.data.head(3).iterrows():
                    safe_print(f"   {i+1}. {row.get('Prénom', '')} {row.get('Nom', '')} - {row.get('Intitulé de poste', '')}")
            
            # Créer le répertoire s'il n'existe pas
            os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
            
            # Sauvegarder le fichier
            self.data.to_excel(output_file, index=False)
            safe_print(f"Données sauvegardées dans {output_file}")
            safe_print(f"Total de profils: {len(self.data)}")
            
            # Vérifier que le fichier a bien été créé
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                safe_print(f"Fichier créé - Taille: {file_size} bytes")
            else:
                safe_print("ERREUR: Fichier non créé!")
                return False
            
            # Afficher un résumé des données
            if not self.data.empty:
                safe_print(f"Répartition par poste:")
                postes_count = self.data['Intitulé de poste'].value_counts()
                for poste, count in postes_count.head(5).items():
                    safe_print(f"   • {poste}: {count} profils")
            
            return True
        except Exception as e:
            safe_print(f"Erreur lors de la sauvegarde du fichier Excel: {str(e)}")
            import traceback
            safe_print(f"Détails de l'erreur:")
            traceback.print_exc()
            return False
    
    def close(self):
        """Ferme le navigateur"""
        if self.driver:
            self.driver.quit()
            print("Navigateur fermé")

def main():
    # Correction pour la gestion des arguments
    parser = argparse.ArgumentParser(description="Scraper de profils professionnels basé sur des intitulés de postes")
    parser.add_argument("--input", "-i", help="Fichier Excel contenant les données existantes")
    parser.add_argument("--output", "-o", default="Resultats_Profils.xlsx", help="Fichier Excel de sortie (sera ajouté au fichier existant)")
    parser.add_argument("--job", "-j", help="Intitulé de poste à rechercher")
    parser.add_argument("--count", "-c", default=5, help="Nombre de résultats à récupérer par intitulé de poste")
    parser.add_argument("--slow", action="store_true", help="Mode lent avec délais supplémentaires pour éviter les CAPTCHA")
    
    args = parser.parse_args()
    
    # Traitement sécurisé du nombre de résultats
    try:
        count = int(args.count)
        if count <= 0:
            count = 5
    except (ValueError, TypeError):
        print(f"ATTENTION: Valeur incorrecte pour --count: '{args.count}'. Utilisation de la valeur par défaut: 5")
        count = 5
    
    scraper = ProfileScraper(args.input, args.slow)
    
    try:
        if args.job:
            # Recherche pour un intitulé de poste spécifique
            scraper.search_by_job_title(args.job, count)
        elif scraper.data is not None and 'Intitulé de poste' in scraper.data.columns:
            # Recherche pour tous les intitulés de postes du fichier d'entrée
            job_titles = scraper.data['Intitulé de poste'].unique()
            for job in job_titles:
                if pd.notna(job) and job.strip():
                    scraper.search_by_job_title(job, count)
        else:
            print("Veuillez spécifier un intitulé de poste avec --job ou fournir un fichier Excel valide avec --input")
            return
        
        # Sauvegarde des résultats
        scraper.save_to_excel(args.output)
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
