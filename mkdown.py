#!/usr/bin/python3
#-*- coding: utf-8 -*-

####################################################################################################
### mkdown.py - script de base pour convertir un fichier markdown en page HTML.
### janvier 2022 - sous license MIT
####################################################################################################
### contact : meyer.daniel67@protonmail.com OU https://t.me/dnl_85
### dépôt   : https://github.com/dnl-85/blocpad_py
####################################################################################################
# NOTE :
# ce script n'utilise aucun module, c'est dire à quel point il est basique :)
# la fonction convert va permettre de lancer la convertion, il faudra lui spécifier le nom du
# fichier à convertir : par exemple si votre fichier se nomme essai.md, ceci donnera :
# convert("essai.md")

def convert(nom_fichier):
    # lecture du fichier texte Markdown et recupération de son contenu
    with open(nom_fichier, 'r') as fichier:
        contenu = fichier.read()

    # separation du fichier ligne par ligne
    # je recherche ici les retours à la ligne, identifié par \n
    contenu = contenu.split("\n")
    
    # création d'une variable pour marquer les listes à puces et les exemples de codes.
    # si marqueur = 0, ceci signifie qu'il n'est ni dans un code, ni dans un liste
    # si marqueur = 1, ceci signifie qu'il analyse un exemple de code
    # si marqueur = 2, ceci signifie qu'il analyse une liste numérotée
    # si marqueur = 3, ceci signifie qu'il analyse une liste pucée
    marqueur = 0
    
    # et création d'une variable contenant le futur fichier html avant l'enregistrement.
    nouveau_contenu = ""

    # ici je parcours le contenu du fichier, qui est une liste maintenant...
    for x in contenu:
        # on commence par les exemples de codes
        if x.startswith("    ") and marqueur == 0:
            x = verif_ligne("    ", "<pre><code>    ", "", x)
            marqueur = 1
        elif x.startswith("    ") and marqueur == 1:
            x = x
        elif marqueur == 1:
            x = verif_ligne("", "</code></pre>", "", x)
            marqueur = 0

        # ici on s'attaque aux titres, paragraphes et séparateurs horizontaux
        x = verif_ligne("######", "<h6>", "</h6>", x)
        x = verif_ligne("#####", "<h5>", "</h5>", x)
        x = verif_ligne("####", "<h4>", "</h4>", x)
        x = verif_ligne("###", "<h3>", "</h3>", x)
        x = verif_ligne("##", "<h2>", "</h2>", x)
        x = verif_ligne("#", "<h1>", "</h1>", x)
        x = verif_ligne("-----", "<hr>", "", x)

        # vérification et balisage des paragraphes
        if x.startswith("  ") and marqueur == 0:
            x = verif_ligne("  ", "<p>", "</p>", x)

        # ensuite on s'attaque aux listes à puces
        if x.startswith("-") and marqueur == 0:
            x = verif_ligne("-", "<ul>\n<li>", "</li>", x)
            marqueur = 2
        elif x.startswith("-") and marqueur == 2:
            x = verif_ligne("-", "<li>", "</li>", x)
        elif marqueur == 2:
            x = verif_ligne("", "</ul>", "", x)
            marqueur = 0

        # puis aux listes numérotées
        if x.startswith("+") and marqueur == 0:
            x = verif_ligne("+", "<ol>\n<li>", "</li>", x)
            marqueur = 3
        elif x.startswith("+") and marqueur == 3:
            x = verif_ligne("+", "<li>", "</li>", x)
        elif marqueur == 3:
            x = verif_ligne("", "</ol>", "", x)
            marqueur = 0

        # pour finir, on balise les emphasis (gras, sous-ligné et italique)
        # mais ceci ne doit pas intervenir dans un exemple de code
        if marqueur != 1:
            x = verif_emphasis("**", "<b>", "</b>", x)
            x = verif_emphasis("*", "<i>", "</i>", x)

        # concaténation dans la variable 'nouveau_contenu'
        nouveau_contenu = nouveau_contenu + x + "\n"

    # au final ne reste qu'à enregistrer le tout dans un fichier html
    with open("auto_html.html", "w") as fichier:
        fichier.write("<body>\n" + nouveau_contenu + "\n</body>")
        
# la fonction verif_ligne va permettre de changer les balises de titres, paragraphes et separateurs
# horizontaux en balises équivalentes HTML. ce sont souvent des balises qui englobent une ligne
# entière, tel les titres, les paragraphes...
def verif_ligne(balise_a_chercher, balise_debut, balise_fin, ligne):
    if ligne.startswith(balise_a_chercher):
        ligne = ligne.replace(balise_a_chercher, balise_debut) + balise_fin
    return ligne

# la fonction verif_emphasis va permettre de changer les balises qui délimiteront les séquences de
# textes en gras ou en italique. je commence d'abord par analyser les mots qui commencent et qui
# finissent par la balise à chercher puis j'analyse les mots qui commencent uniquement par la balise
# à chercher mais finissent normalement et je fini par les mots qui finissent uniquement par la
# balise à chercher mais commencent normalement
def verif_emphasis(balise_a_chercher, balise_debut, balise_fin, ligne):
    mots = ligne.split(" ")
    nouvelle_ligne = []

    for x in mots:
        if x.startswith(balise_a_chercher) and x.endswith(balise_a_chercher):
            x = x.replace(balise_a_chercher, "")
            x = balise_debut + x + balise_fin
        elif x.startswith(balise_a_chercher):
            x = x.replace(balise_a_chercher, balise_debut)
        elif x.endswith(balise_a_chercher):
            x = x.replace(balise_a_chercher, balise_fin)
        nouvelle_ligne.append(x)

    ligne = " ".join(nouvelle_ligne)
    return ligne

# et voilà !
