#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter manuellement des profils trouvés à un fichier Excel existant
"""

import pandas as pd
import os
from datetime import datetime

def charger_ou_creer_fichier(nom_fichier="Resultats_Profils.xlsx"):
    """Charge un fichier Excel existant ou en crée un nouveau"""
    if os.path.exists(nom_fichier):
        try:
            df = pd.read_excel(nom_fichier)
            print(f"✓ Fichier existant chargé: {nom_fichier}")
            print(f"  📊 Nombre de profils existants: {len(df)}")
            return df
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {str(e)}")
            print("🔄 Création d'un nouveau fichier...")
    
    # Créer un nouveau DataFrame
    df = pd.DataFrame(columns=[
        'Intitulé de poste',
        'Prénom',
        'Nom',
        'Email',
        'Entreprise',
        'LinkedIn',
        'Date d\'ajout',
        'Notes'
    ])
    print(f"✓ Nouveau fichier créé: {nom_fichier}")
    return df

def verifier_doublon(df, linkedin_url=None, prenom=None, nom=None, entreprise=None):
    """Vérifie si un profil existe déjà"""
    
    # Vérification par URL LinkedIn
    if linkedin_url and not df.empty:
        existing = df[df['LinkedIn'] == linkedin_url]
        if not existing.empty:
            return True, "URL LinkedIn déjà existante"
    
    # Vérification par nom + entreprise
    if prenom and nom and entreprise and not df.empty:
        existing = df[
            (df['Prénom'].str.lower() == prenom.lower()) & 
            (df['Nom'].str.lower() == nom.lower()) & 
            (df['Entreprise'].str.lower() == entreprise.lower())
        ]
        if not existing.empty:
            return True, "Nom + Entreprise déjà existants"
    
    return False, ""

def ajouter_profil_interactif(df):
    """Interface interactive pour ajouter un profil"""
    print("\n" + "="*50)
    print("AJOUT D'UN NOUVEAU PROFIL")
    print("="*50)
    
    # Saisie des informations
    intitule = input("Intitulé de poste: ").strip()
    prenom = input("Prénom: ").strip()
    nom = input("Nom: ").strip()
    email = input("Email (optionnel): ").strip()
    entreprise = input("Entreprise: ").strip()
    linkedin = input("URL LinkedIn: ").strip()
    notes = input("Notes (optionnel): ").strip()
    
    # Validation minimale
    if not intitule or not prenom or not nom:
        print("❌ Les champs Intitulé, Prénom et Nom sont obligatoires!")
        return df, False
    
    # Vérification des doublons
    is_duplicate, reason = verifier_doublon(df, linkedin, prenom, nom, entreprise)
    if is_duplicate:
        print(f"⚠️  ATTENTION: Profil potentiellement en double ({reason})")
        continuer = input("Voulez-vous quand même l'ajouter? (o/n): ").lower()
        if continuer != 'o':
            print("❌ Ajout annulé")
            return df, False
    
    # Créer le nouveau profil
    nouveau_profil = {
        'Intitulé de poste': intitule,
        'Prénom': prenom,
        'Nom': nom,
        'Email': email,
        'Entreprise': entreprise,
        'LinkedIn': linkedin,
        'Date d\'ajout': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Notes': notes
    }
    
    # Ajouter au DataFrame
    new_row = pd.DataFrame([nouveau_profil])
    df = pd.concat([df, new_row], ignore_index=True)
    
    print(f"✓ Profil ajouté: {prenom} {nom} chez {entreprise}")
    return df, True

def afficher_stats(df):
    """Affiche les statistiques du fichier"""
    if df.empty:
        print("📊 Aucun profil dans le fichier")
        return
    
    print(f"\n📊 STATISTIQUES:")
    print(f"   Total profils: {len(df)}")
    
    if 'Intitulé de poste' in df.columns:
        postes = df['Intitulé de poste'].value_counts()
        print(f"   Postes les plus représentés:")
        for poste, count in postes.head(5).items():
            print(f"     • {poste}: {count}")
    
    if 'Entreprise' in df.columns:
        entreprises = df['Entreprise'].value_counts()
        print(f"   Entreprises les plus représentées:")
        for entreprise, count in entreprises.head(5).items():
            print(f"     • {entreprise}: {count}")

def main():
    print("="*60)
    print("GESTIONNAIRE DE PROFILS PROFESSIONNELS")
    print("="*60)
    print("Ce script vous permet d'ajouter des profils trouvés")
    print("manuellement à un fichier Excel existant.")
    print("")
    
    # Demander le nom du fichier
    nom_fichier = input("Nom du fichier Excel (Entrée pour 'Resultats_Profils.xlsx'): ").strip()
    if not nom_fichier:
        nom_fichier = "Resultats_Profils.xlsx"
    
    # S'assurer que le fichier a l'extension .xlsx
    if not nom_fichier.endswith('.xlsx'):
        nom_fichier += '.xlsx'
    
    # Charger ou créer le fichier
    df = charger_ou_creer_fichier(nom_fichier)
    
    # Afficher les statistiques actuelles
    afficher_stats(df)
    
    # Boucle principale
    profils_ajoutes = 0
    while True:
        print(f"\n{'-'*40}")
        print("MENU:")
        print("1. Ajouter un profil")
        print("2. Voir les statistiques")
        print("3. Sauvegarder et quitter")
        print("4. Quitter sans sauvegarder")
        
        choix = input("\nVotre choix (1-4): ").strip()
        
        if choix == '1':
            df, ajout_reussi = ajouter_profil_interactif(df)
            if ajout_reussi:
                profils_ajoutes += 1
        
        elif choix == '2':
            afficher_stats(df)
        
        elif choix == '3':
            try:
                df.to_excel(nom_fichier, index=False)
                print(f"✓ Fichier sauvegardé: {nom_fichier}")
                print(f"📈 {profils_ajoutes} nouveaux profils ajoutés")
                break
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde: {str(e)}")
        
        elif choix == '4':
            if profils_ajoutes > 0:
                confirmer = input(f"Vous avez {profils_ajoutes} profils non sauvegardés. Êtes-vous sûr? (o/n): ")
                if confirmer.lower() != 'o':
                    continue
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide, veuillez saisir 1, 2, 3 ou 4")

if __name__ == "__main__":
    main()
