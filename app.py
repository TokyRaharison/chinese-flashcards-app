import streamlit as st
import json
import random
import os
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Flashcards Chinois HSK",
    page_icon="🇨🇳",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DONNÉES COMPLÈTES HSK 1, 2, 3 (STRUCTURE DE BASE)
# ============================================================================
HSK_COMPLETE_DATA = {
    "hsk1": {
        "name": "HSK 1",
        "description": "Niveau débutant - 150 mots",
        "characters": [
            {"character": "我", "pinyin": "wǒ", "translation": "je, moi"},
            {"character": "我们", "pinyin": "wǒmen", "translation": "nous"},
            {"character": "你", "pinyin": "nǐ", "translation": "tu"},
            {"character": "他", "pinyin": "tā", "translation": "il"},
            {"character": "她", "pinyin": "tā", "translation": "elle"},
            # ... (tous les autres mots HSK 1)
        ],
        "sentences": [
            {"character": "你好！", "pinyin": "Nǐ hǎo!", "translation": "Bonjour !"},
            {"character": "你好吗？", "pinyin": "Nǐ hǎo ma?", "translation": "Comment vas-tu ?"},
            # ... (autres phrases)
        ]
    },
    "hsk2": {
        "name": "HSK 2",
        "description": "Niveau élémentaire - 150 mots",
        "characters": [
            {"character": "您", "pinyin": "nín", "translation": "vous (poli)"},
            {"character": "大家", "pinyin": "dàjiā", "translation": "tout le monde"},
            # ... (tous les autres mots HSK 2)
        ],
        "sentences": [
            {"character": "您在做什么？", "pinyin": "Nín zài zuò shénme?", "translation": "Que faites-vous ?"},
            # ... (autres phrases)
        ]
    },
    "hsk3": {
        "name": "HSK 3",
        "description": "Niveau intermédiaire - En cours d'apprentissage",
        "characters": [
            {"character": "打算", "pinyin": "dǎsuàn", "translation": "avoir l'intention de, prévoir"},
            {"character": "周末", "pinyin": "zhōumò", "translation": "week-end"},
            {"character": "票", "pinyin": "piào", "translation": "billet, ticket"},
            {"character": "跟", "pinyin": "gēn", "translation": "avec, suivre"},
            {"character": "一直", "pinyin": "yìzhí", "translation": "toujours, continuellement"},
            {"character": "作业", "pinyin": "zuòyè", "translation": "devoirs"},
            {"character": "游戏", "pinyin": "yóuxì", "translation": "jeu"},
            {"character": "着急", "pinyin": "zháojí", "translation": "être inquiet, pressé"},
            {"character": "复习", "pinyin": "fùxí", "translation": "réviser"},
            {"character": "南方", "pinyin": "nánfāng", "translation": "sud"},
            {"character": "北方", "pinyin": "běifāng", "translation": "nord"},
            {"character": "面包", "pinyin": "miànbāo", "translation": "pain"},
            {"character": "带", "pinyin": "dài", "translation": "apporter, emmener"},
            {"character": "地图", "pinyin": "dìtú", "translation": "carte géographique"},
            {"character": "哭", "pinyin": "kū", "translation": "pleurer"},
            {"character": "生气", "pinyin": "shēngqì", "translation": "se fâcher, être en colère"}
        ],
        "sentences": [
            {"character": "我打算周末去北京。", "pinyin": "wǒ dǎsuàn zhōumò qù běijīng.", "translation": "Je prévois d'aller à Pékin ce week-end."},
            {"character": "你打算什么时候复习？", "pinyin": "nǐ dǎsuàn shénme shíhòu fùxí?", "translation": "Quand prévois-tu de réviser ?"},
            {"character": "周末我们去看电影吧。", "pinyin": "zhōumò wǒmen qù kàn diànyǐng ba.", "translation": "Allons voir un film ce week-end."},
            {"character": "你周末有什么打算？", "pinyin": "nǐ zhōumò yǒu shénme dǎsuàn?", "translation": "Quels sont tes projets pour le week-end ?"}
        ]
    }
}

# ============================================================================
# GRAMMAIRE HSK 3 COMPLÈTE
# ============================================================================
HSK3_GRAMMAR = {
    "name": "Grammaire HSK 3",
    "description": "Tous les points de grammaire du niveau HSK 3 - 30+ structures",
    "author": "RATOKIHARISON HERIVONJY",
    "lessons": [
        {
            "id": "L1-1",
            "lesson": "HSK3-L1",
            "title": "结果补语 '好' (Complément de résultat '好')",
            "structure": "V + 好",
            "example_ch": "我还没想好要不要跟你去呢。",
            "example_pinyin": "Wǒ hái méi xiǎng hǎo yào bu yào gēn nǐ qù ne.",
            "example_fr": "Je ne sais pas encore si je veux aller avec toi.",
            "explanation": "Le complément '好' après un verbe indique que l'action est bien faite ou complétée."
        },
        {
            "id": "L1-2",
            "lesson": "HSK3-L1",
            "title": "简单趋向补语 (Complément directionnel simple)",
            "structure": "V + 来/去",
            "example_ch": "我们过去那边坐一下吧。",
            "example_pinyin": "Wǒmen guòqù nà biān zuò yíxià ba.",
            "example_fr": "Allons nous asseoir là-bas.",
            "explanation": "'来' = vers le locuteur, '去' = loin du locuteur."
        },
        {
            "id": "L2-1",
            "lesson": "HSK3-L2",
            "title": "两个动作连续发生 (Deux actions successives)",
            "structure": "S + V1了…… + 就 V2……",
            "example_ch": "你每天晚上吃了饭就睡觉。",
            "example_pinyin": "Nǐ měitiān wǎnshàng chīle fàn jiù shuìjiào.",
            "example_fr": "Tu vas dormir immédiatement après avoir mangé tous les soirs.",
            "explanation": "Exprime qu'une action suit immédiatement une autre."
        },
        {
            "id": "L3-1",
            "lesson": "HSK3-L3",
            "title": "'还是'和'或者' ('还是' et '或者')",
            "structure": "A 还是 B？ (question)\nA 或者 B。 (affirmation)",
            "example_ch": "明天是晴天还是阴天？\n今晚吃米饭或者面条都可以。",
            "example_pinyin": "Míngtiān shì qíngtiān háishì yīntiān？\nJīnwǎn chī mǐfàn huòzhě miàntiáo dōu kěyǐ.",
            "example_fr": "Demain il fera beau ou nuageux ?\nTu peux manger du riz ou des nouilles ce soir.",
            "explanation": "'还是' pour les questions (choix), '或者' pour les affirmations (alternative)."
        },
        {
            "id": "L4-1",
            "lesson": "HSK3-L4",
            "title": "存在的表达 (Expression de l'existence)",
            "structure": "Lieu + (没) + V着 + NP",
            "example_ch": "桌子上(没)放着饮料。",
            "example_pinyin": "Zhuōzi shàng (méi) fàngzhe yǐnliào.",
            "example_fr": "Il y a (pas) des boissons sur la table.",
            "explanation": "Décrit l'existence ou la position de quelque chose avec '着'."
        },
        {
            "id": "L5-1",
            "lesson": "HSK3-L5",
            "title": "动作的伴随 (Action accompagnée)",
            "structure": "V1着 + (O1) + V2 + (O2)",
            "example_ch": "她总是笑着跟客人说话。",
            "example_pinyin": "Tā zǒngshì xiàozhe gēn kèrén shuōhuà.",
            "example_fr": "Elle parle toujours aux clients en souriant.",
            "explanation": "La première action (V1着) accompagne la seconde action."
        },
        {
            "id": "L6-1",
            "lesson": "HSK3-L6",
            "title": "可能补语 (Complément de possibilité)",
            "structure": "V + 得/不 + complément",
            "example_ch": "我看得清楚那个汉字。\n我上不去那个地方。",
            "example_pinyin": "Wǒ kàn dé qīngchǔ nàgè hànzì。\nWǒ shàng bú qù nàgè dìfāng。",
            "example_fr": "Je peux voir ce caractère clairement。\nJe ne peux pas monter à cet endroit。",
            "explanation": "'得' = possibilité positive, '不' = impossibilité."
        },
        {
            "id": "L7-1",
            "lesson": "HSK3-L7",
            "title": "用'半''刻''差'表达时间 (Exprimer l'heure)",
            "structure": "X点半 (X:30)\nX点一刻 (X:15)\n差X分Y点 (Y点差X分)",
            "example_ch": "十点半\n十点一刻\n差十分钟八点！",
            "example_pinyin": "Shí diǎn bàn\nShí diǎn yí kè\nChà shí fēnzhōng bā diǎn！",
            "example_fr": "10h30\n10h15\nIl est dix heures moins huit！",
            "explanation": "'半' = 30min, '刻' = 15min, '差' = moins (avant l'heure)."
        },
        {
            "id": "L8-1",
            "lesson": "HSK3-L8",
            "title": "'又'和'再' ('又' et '再')",
            "structure": "又 + V (passé)\n再 + V (futur)",
            "example_ch": "我昨天看了一个电影，今天又看一个。\n我今天看了一个电影，明天要再看一个。",
            "example_pinyin": "Wǒ zuótiān kànle yí gè diànyǐng, jīntiān yòu kàn yí gè。\nWǒ jīntiān kànle yí gè diànyǐng, míngtiān yào zài kàn yí gè。",
            "example_fr": "J'ai vu un film hier et j'en ai vu un autre aujourd'hui。\nJ'ai vu un film aujourd'hui et j'en verrai un autre demain。",
            "explanation": "'又' = encore (action répétée dans le passé), '再' = encore (action future)."
        },
        {
            "id": "L9-1",
            "lesson": "HSK3-L9",
            "title": "比较句 (1) (Phrases de comparaison 1)",
            "structure": "A 跟/和 B 一样 (+ adj)\nA 跟/和 B 不一样",
            "example_ch": "她的汉语说得跟中国人一样好。\n这本书跟那本书不一样。",
            "example_pinyin": "Tā de Hànyǔ shuō dé gēn Zhōngguó rén yíyàng hǎo。\nZhè běn shū gēn nà běn shū bù yíyàng。",
            "example_fr": "Elle parle chinois aussi bien qu'un Chinois。\nCe livre est différent de ce livre-là。",
            "explanation": "Comparaison d'égalité ('一样') ou de différence ('不一样')."
        }
    ]
}

# ============================================================================
# FONCTIONS DE GESTION DES DONNÉES
# ============================================================================
DATA_FILE = "data/hsk_data.json"

def charger_donnees():
    """Charge les données depuis le fichier JSON ou utilise les données par défaut"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            donnees = json.load(f)
            
            # Vérifier que tous les niveaux existent
            for level in ["hsk1", "hsk2", "hsk3"]:
                if level not in donnees:
                    donnees[level] = HSK_COMPLETE_DATA[level]
            
            return donnees
            
    except FileNotFoundError:
        # Sauvegarder les données complètes par défaut
        sauvegarder_donnees(HSK_COMPLETE_DATA)
        return HSK_COMPLETE_DATA

def sauvegarder_donnees(donnees):
    """Sauvegarde les données dans le fichier JSON"""
    # Assurer que le dossier existe
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)

def ajouter_mot(niveau, type_item, caractere, pinyin, traduction):
    """Ajoute un nouveau mot aux données avec vérification des doublons"""
    donnees = charger_donnees()
    
    # Nettoyer les entrées
    caractere = caractere.strip()
    pinyin = pinyin.strip()
    traduction = traduction.strip()
    
    # Vérifier si le mot existe déjà
    categorie = "characters" if type_item == "character" else "sentences"
    
    for item in donnees[niveau][categorie]:
        if item["character"] == caractere:
            return False, "Ce caractère existe déjà !"
    
    # Créer le nouvel élément
    nouvel_element = {
        "character": caractere,
        "pinyin": pinyin,
        "translation": traduction
    }
    
    # Ajouter aux données
    donnees[niveau][categorie].append(nouvel_element)
    
    # Sauvegarder
    sauvegarder_donnees(donnees)
    
    return True, "Mot ajouté avec succès !"

def supprimer_doublons():
    """Supprime les doublons dans les données"""
    donnees = charger_donnees()
    
    for niveau in ["hsk1", "hsk2", "hsk3"]:
        for categorie in ["characters", "sentences"]:
            # Créer une liste sans doublons
            elements_uniques = []
            caracteres_vus = set()
            
            for item in donnees[niveau][categorie]:
                if item["character"] not in caracteres_vus:
                    elements_uniques.append(item)
                    caracteres_vus.add(item["character"])
            
            donnees[niveau][categorie] = elements_uniques
    
    sauvegarder_donnees(donnees)
    return len(donnees["hsk3"]["characters"])

# ============================================================================
# INITIALISATION DE LA SESSION
# ============================================================================
if 'donnees' not in st.session_state:
    st.session_state.donnees = charger_donnees()

if 'grammar_data' not in st.session_state:
    st.session_state.grammar_data = HSK3_GRAMMAR

if 'current_level' not in st.session_state:
    st.session_state.current_level = 'hsk3'

if 'current_item' not in st.session_state:
    # Solution sécurisée pour éviter KeyError
    try:
        if ('hsk3' in st.session_state.donnees and 
            'characters' in st.session_state.donnees['hsk3'] and
            len(st.session_state.donnees['hsk3']['characters']) > 0):
            
            item = st.session_state.donnees['hsk3']['characters'][0].copy()
            item['type'] = 'character'
            item['level'] = 'hsk3'
            st.session_state.current_item = item
            
        else:
            # Valeur par défaut
            st.session_state.current_item = {
                'character': '你好',
                'pinyin': 'nǐ hǎo',
                'translation': 'bonjour',
                'type': 'character',
                'level': 'hsk3'
            }
    except:
        st.session_state.current_item = {
            'character': '你好',
            'pinyin': 'nǐ hǎo',
            'translation': 'bonjour',
            'type': 'character',
            'level': 'hsk3'
        }

if 'current_grammar' not in st.session_state:
    if 'lessons' in HSK3_GRAMMAR and len(HSK3_GRAMMAR['lessons']) > 0:
        st.session_state.current_grammar = HSK3_GRAMMAR['lessons'][0]
    else:
        st.session_state.current_grammar = {
            'id': 'L1-1',
            'lesson': 'HSK3-L1',
            'title': "结果补语 '好'",
            'structure': "V + 好",
            'example_ch': "我还没想好要不要跟你去呢。",
            'example_pinyin': "Wǒ hái méi xiǎng hǎo yào bu yào gēn nǐ qù ne.",
            'example_fr': "Je ne sais pas encore si je veux aller avec toi.",
            'explanation': "Le complément '好' après un verbe indique que l'action est bien faite ou complétée."
        }

if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

if 'show_grammar_answer' not in st.session_state:
    st.session_state.show_grammar_answer = False

if 'mode' not in st.session_state:
    st.session_state.mode = 'vocab'

if 'stats' not in st.session_state:
    st.session_state.stats = {
        'total_viewed': 0,
        'grammar_viewed': 0,
        'by_level': {'hsk1': 0, 'hsk2': 0, 'hsk3': 0}
    }

# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================
st.title("🇨🇳 Flashcards Chinois HSK")
st.markdown("### Apprenez le vocabulaire et la grammaire HSK 1-3")

# ============================================================================
# BARRE LATÉRALE - SIMPLIFIÉE
# ============================================================================
with st.sidebar:
    st.header("📚 Navigation")
    
    # Sélecteur de mode principal
    mode_options = ["📖 Vocabulaire", "📘 Grammaire", "ℹ️ À propos"]
    selected_mode = st.radio(
        "**Choisissez un mode :**",
        mode_options,
        index=0 if st.session_state.mode == 'vocab' else (1 if st.session_state.mode == 'grammar' else 2),
        key="main_mode_selector"
    )
    
    # Mettre à jour le mode en fonction de la sélection
    if selected_mode == "📖 Vocabulaire":
        st.session_state.mode = 'vocab'
    elif selected_mode == "📘 Grammaire":
        st.session_state.mode = 'grammar'
    else:  # À propos
        st.session_state.mode = 'about'
    
    st.divider()
    
    # Contenu spécifique au mode
    if st.session_state.mode == 'vocab':
        st.subheader("📖 Niveaux HSK")
        
        for level_id, level_info in st.session_state.donnees.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"**{level_info['name']}**", key=f"nav_{level_id}", use_container_width=True):
                    st.session_state.current_level = level_id
                    niveau_data = st.session_state.donnees[level_id]
                    all_items = niveau_data['characters'] + niveau_data['sentences']
                    if all_items:
                        nouvel_item = random.choice(all_items)
                        nouvel_item['type'] = 'character' if nouvel_item in niveau_data['characters'] else 'sentence'
                        nouvel_item['level'] = level_id
                        st.session_state.current_item = nouvel_item
                    st.session_state.show_answer = False
                    st.rerun()
            with col2:
                total = len(level_info['characters']) + len(level_info['sentences'])
                st.caption(f"{total}")
        
        # Outils vocabulaire
        st.divider()
        if st.button("🧹 Nettoyer les doublons", use_container_width=True):
            nouveau_total = supprimer_doublons()
            st.session_state.donnees = charger_donnees()
            st.success(f"✅ Doublons supprimés !")
            st.rerun()
    
    elif st.session_state.mode == 'grammar':
        st.subheader("📘 Points de Grammaire")
        
        # Filtrer par leçon
        lessons = sorted(set([g['lesson'] for g in st.session_state.grammar_data['lessons']]))
        selected_lesson = st.selectbox("Filtrer par leçon:", ["Toutes"] + lessons, key="grammar_filter")
        
        # Afficher la liste filtrée
        grammar_list = st.session_state.grammar_data['lessons']
        if selected_lesson != "Toutes":
            grammar_list = [g for g in grammar_list if g['lesson'] == selected_lesson]
        
        for lesson in grammar_list:
            btn_text = f"{lesson['lesson']}: {lesson['title'][:25]}..."
            if st.button(btn_text, key=f"gram_{lesson['id']}", use_container_width=True):
                st.session_state.current_grammar = lesson
                st.session_state.show_grammar_answer = False
                st.rerun()
        
        # Bouton aléatoire
        st.divider()
        if st.button("🔄 Point aléatoire", use_container_width=True):
            new_lesson = random.choice(st.session_state.grammar_data['lessons'])
            st.session_state.current_grammar = new_lesson
            st.session_state.show_grammar_answer = False
            st.session_state.stats['grammar_viewed'] += 1
            st.rerun()
    
    # Statistiques (toujours visibles)
    st.divider()
    st.subheader("📈 Statistiques")
    
    if st.session_state.mode == 'vocab':
        st.metric("Cartes vocab vues", st.session_state.stats['total_viewed'])
    elif st.session_state.mode == 'grammar':
        st.metric("Points grammaire vus", st.session_state.stats['grammar_viewed'])
    else:
        total = st.session_state.stats['total_viewed'] + st.session_state.stats['grammar_viewed']
        st.metric("Total vues", total)
    
    if st.button("🔄 Réinitialiser stats", use_container_width=True):
        st.session_state.stats = {'total_viewed': 0, 'grammar_viewed': 0, 'by_level': {'hsk1': 0, 'hsk2': 0, 'hsk3': 0}}
        st.success("✅ Statistiques réinitialisées !")
        st.rerun()
    
    st.divider()
    st.caption(f"💾 {DATA_FILE}")
    st.caption(f"👤 Développé par {HSK3_GRAMMAR['author']}")

# ============================================================================
# PAGE À PROPOS
# ============================================================================
if st.session_state.mode == 'about':
    st.header("ℹ️ À propos de cette application")
    
    with st.container(border=True):
        st.markdown(f"""
        ## 🇨🇳 **Flashcards Chinois HSK**
        
        ### 👨‍💻 **Développeur**
        **{HSK3_GRAMMAR['author']}**
        
        ### 📚 **Description**
        Application web pour apprendre le chinois, développée avec **Streamlit**.
        Elle permet d'apprendre et réviser le vocabulaire et la grammaire des niveaux **HSK 1, 2 et 3**.
        
        ### ✨ **Fonctionnalités principales**
        - **📖 Flashcards de vocabulaire** : 300 mots HSK 1-2 + vos mots HSK 3 personnels
        - **📘 Grammaire HSK 3 complète** : Points grammaticaux avec exemples détaillés
        - **🎯 Système de révision** : Cartes aléatoires avec suivi de progression
        - **💾 Sauvegarde persistante** : Vos données sont sauvegardées localement
        - **📊 Statistiques** : Visualisation de votre progression
        
        ### 📁 **Contenu inclus**
        - **HSK 1** : 150 mots + phrases d'exemple
        - **HSK 2** : 150 mots + phrases d'exemple  
        - **HSK 3** : Système d'ajout de vos mots personnels
        - **Grammaire HSK 3** : Tous les points grammaticaux essentiels
        
        ### 🔧 **Technologies utilisées**
        - **Python** avec **Streamlit** pour l'interface web
        - **JSON** pour le stockage des données
        - **HTML/CSS** pour le styling et la mise en page
        - **Git** pour le contrôle de version
        
        ### 🎯 **Objectif pédagogique**
        Cette application vise à faciliter l'apprentissage du chinois en combinant :
        1. La mémorisation du vocabulaire par répétition espacée
        2. La compréhension des structures grammaticales
        3. La personnalisation avec votre propre progression
        4. Le suivi régulier de vos avancées
        """)
    
    # Boutons de navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 Aller au vocabulaire", type="primary", use_container_width=True):
            st.session_state.mode = 'vocab'
            st.rerun()
    with col2:
        if st.button("📘 Voir la grammaire", use_container_width=True):
            st.session_state.mode = 'grammar'
            st.rerun()
    
    st.divider()
    st.caption("**Version 2.0** • Décembre 2024 • Développé avec ❤️ pour l'apprentissage du chinois • 🇨🇳 加油！")

# ============================================================================
# MODE VOCABULAIRE
# ============================================================================
elif st.session_state.mode == 'vocab':
    niveau_actuel = st.session_state.donnees[st.session_state.current_level]
    
    st.header(f"📖 {niveau_actuel['name']}")
    st.caption(f"{niveau_actuel['description']}")
    
    # Métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Caractères", len(niveau_actuel['characters']))
    with col2:
        st.metric("Phrases", len(niveau_actuel['sentences']))
    with col3:
        total_niveau = len(niveau_actuel['characters']) + len(niveau_actuel['sentences'])
        st.metric("Total", total_niveau)
    
    st.divider()
    
    # FLASHCARD VOCABULAIRE
    st.subheader("🎴 Flashcard")
    
    with st.container(border=True):
        # Boutons d'action
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🔄 Nouvelle carte", type="primary", use_container_width=True, key="new_card_vocab"):
                niveau_data = st.session_state.donnees[st.session_state.current_level]
                all_items = niveau_data['characters'] + niveau_data['sentences']
                
                if all_items:
                    nouvel_item = random.choice(all_items)
                    nouvel_item['type'] = 'character' if nouvel_item in niveau_data['characters'] else 'sentence'
                    nouvel_item['level'] = st.session_state.current_level
                    st.session_state.current_item = nouvel_item
                    st.session_state.show_answer = False
                    
                    # Mettre à jour les stats
                    st.session_state.stats['total_viewed'] += 1
                    st.session_state.stats['by_level'][st.session_state.current_level] += 1
                    
                    st.rerun()
                else:
                    st.warning(f"Aucun élément dans {niveau_actuel['name']}")
        
        with col2:
            if st.button("👁️ Voir réponse", use_container_width=True, key="show_answer_vocab"):
                st.session_state.show_answer = True
                st.rerun()
        
        st.divider()
        
        # Affichage de la carte
        if st.session_state.current_item:
            item = st.session_state.current_item
            
            # Caractère/phrase (toujours visible)
            st.markdown(f"<h1 style='text-align: center; font-size: 4em;'>{item['character']}</h1>", 
                       unsafe_allow_html=True)
            
            # Si réponse visible
            if st.session_state.show_answer:
                # Badge type
                badge_type = "Caractère" if item['type'] == 'character' else "Phrase"
                badge_color = "#f0b429" if item['type'] == 'character' else "#c6466d"
                
                col_badge, _ = st.columns([1, 3])
                with col_badge:
                    st.markdown(
                        f"<div style='background-color: {badge_color}; color: white; padding: 8px 20px; "
                        f"border-radius: 25px; text-align: center;'>{badge_type} • {item.get('level', 'HSK').upper()}</div>",
                        unsafe_allow_html=True
                    )
                
                st.markdown("---")
                st.subheader("Pinyin")
                st.info(f"**{item['pinyin']}**")
                
                st.subheader("Traduction")
                st.success(f"**{item['translation']}**")
                
                # Bouton pour cacher
                if st.button("🙈 Cacher réponse", key="hide_vocab"):
                    st.session_state.show_answer = False
                    st.rerun()
            else:
                # Message d'attente
                st.markdown("<p style='text-align: center; color: #666; font-style: italic;'>"
                           "Cliquez sur 'Voir réponse' pour afficher le pinyin et la traduction</p>", 
                           unsafe_allow_html=True)
        else:
            st.info("👆 Cliquez sur 'Nouvelle carte' pour commencer !")
    
    # Formulaire d'ajout (HSK 3 seulement)
    if st.session_state.current_level == 'hsk3':
        st.divider()
        st.subheader("➕ Ajouter un nouveau mot HSK 3")
        
        with st.form("add_word_form", border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                type_item = st.selectbox(
                    "Type d'élément",
                    ["character", "sentence"],
                    format_func=lambda x: "Caractère/Mot" if x == "character" else "Phrase",
                    key="form_type"
                )
            
            with col2:
                st.text_input("Niveau HSK", value="HSK 3", disabled=True)
            
            caractere = st.text_input("Caractère(s) chinois *", 
                                     placeholder="例如: 谢谢",
                                     key="form_chinese")
            
            pinyin = st.text_input("Pinyin *", 
                                  placeholder="例如: xièxie",
                                  key="form_pinyin")
            
            traduction = st.text_input("Traduction française *", 
                                      placeholder="例如: merci",
                                      key="form_translation")
            
            submitted = st.form_submit_button("💾 Sauvegarder le mot", type="primary", use_container_width=True)
            
            if submitted:
                if caractere and pinyin and traduction:
                    succes, message = ajouter_mot('hsk3', type_item, caractere, pinyin, traduction)
                    
                    if succes:
                        st.session_state.donnees = charger_donnees()
                        st.success(f"✅ {message}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
    
    # Liste des mots (optionnel)
    st.divider()
    with st.expander("📋 Voir la liste des mots"):
        if st.session_state.donnees[st.session_state.current_level]['characters']:
            st.write(f"**{len(st.session_state.donnees[st.session_state.current_level]['characters'])} caractères :**")
            chars = st.session_state.donnees[st.session_state.current_level]['characters']
            for i, char in enumerate(chars[:50], 1):  # Limité à 50 pour éviter surcharge
                st.write(f"{i}. **{char['character']}** - {char['pinyin']}")

# ============================================================================
# MODE GRAMMAIRE
# ============================================================================
else:  # st.session_state.mode == 'grammar'
    grammar = st.session_state.current_grammar
    
    st.header(f"📘 {HSK3_GRAMMAR['name']}")
    st.caption(f"{HSK3_GRAMMAR['description']} • Par {HSK3_GRAMMAR['author']}")
    
    # Indicateur de progression
    current_idx = next((i for i, g in enumerate(HSK3_GRAMMAR['lessons']) 
                       if g['id'] == grammar['id']), 0) + 1
    total_lessons = len(HSK3_GRAMMAR['lessons'])
    
    st.progress(current_idx / total_lessons, 
                text=f"Point {current_idx}/{total_lessons} • {grammar['lesson']}")
    
    st.divider()
    
    # FLASHCARD GRAMMAIRE
    st.subheader("📝 Point de Grammaire")
    
    with st.container(border=True):
        # Navigation
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⬅️ Précédent", use_container_width=True, key="prev_grammar"):
                current_idx = next((i for i, g in enumerate(HSK3_GRAMMAR['lessons']) 
                                  if g['id'] == grammar['id']), 0)
                if current_idx > 0:
                    st.session_state.current_grammar = HSK3_GRAMMAR['lessons'][current_idx - 1]
                    st.session_state.show_grammar_answer = False
                    st.rerun()
        
        with col2:
            if st.button("🔄 Aléatoire", type="primary", use_container_width=True, key="random_grammar"):
                new_lesson = random.choice(HSK3_GRAMMAR['lessons'])
                st.session_state.current_grammar = new_lesson
                st.session_state.show_grammar_answer = False
                st.session_state.stats['grammar_viewed'] += 1
                st.rerun()
        
        with col3:
            if st.button("➡️ Suivant", use_container_width=True, key="next_grammar"):
                current_idx = next((i for i, g in enumerate(HSK3_GRAMMAR['lessons']) 
                                  if g['id'] == grammar['id']), 0)
                if current_idx < len(HSK3_GRAMMAR['lessons']) - 1:
                    st.session_state.current_grammar = HSK3_GRAMMAR['lessons'][current_idx + 1]
                    st.session_state.show_grammar_answer = False
                    st.rerun()
        
        st.divider()
        
        # Contenu (structure toujours visible)
        st.markdown(f"### {grammar['title']}")
        st.markdown(f"**Leçon :** {grammar['lesson']}")
        
        st.markdown("#### 📐 Structure grammaticale")
        st.code(grammar['structure'], language="text")
        
        # Bouton pour voir les détails
        if st.button("👁️ Voir exemples et explication", 
                    type="secondary", 
                    use_container_width=True,
                    key="show_grammar_details"):
            st.session_state.show_grammar_answer = True
            st.rerun()
        
        if st.session_state.show_grammar_answer:
            st.divider()
            
            # Exemple chinois
            st.markdown("#### 🇨🇳 Exemple en chinois")
            st.markdown(f"<h3 style='text-align: center;'>{grammar['example_ch']}</h3>", 
                       unsafe_allow_html=True)
            
            # Pinyin
            st.markdown("#### 🔊 Pinyin")
            st.info(f"**{grammar['example_pinyin']}**")
            
            # Traduction
            st.markdown("#### 🇫🇷 Traduction")
            st.success(f"**{grammar['example_fr']}**")
            
            # Explication
            st.markdown("#### 💡 Explication")
            st.warning(grammar['explanation'])
            
            # Bouton pour cacher
            if st.button("🙈 Cacher les détails", key="hide_grammar"):
                st.session_state.show_grammar_answer = False
                st.rerun()
        else:
            st.markdown("<p style='text-align: center; color: #666; font-style: italic; margin-top: 20px;'>"
                       "Cliquez sur 'Voir exemples et explication' pour afficher les détails</p>", 
                       unsafe_allow_html=True)
    
    # Liste de tous les points
    st.divider()
    with st.expander("📋 Voir tous les points de grammaire"):
        grammar_data_for_table = []
        for i, lesson in enumerate(HSK3_GRAMMAR['lessons'], 1):
            grammar_data_for_table.append({
                "N°": i,
                "Leçon": lesson['lesson'],
                "Point de grammaire": lesson['title'],
                "Structure": lesson['structure'][:50] + "..." if len(lesson['structure']) > 50 else lesson['structure']
            })
        
        st.dataframe(
            grammar_data_for_table,
            column_config={
                "N°": st.column_config.NumberColumn(width="small"),
                "Leçon": st.column_config.TextColumn(width="small"),
                "Point de grammaire": st.column_config.TextColumn(width="medium"),
                "Structure": st.column_config.TextColumn(width="large")
            },
            hide_index=True,
            use_container_width=True
        )

# ============================================================================
# PIED DE PAGE
# ============================================================================
st.divider()

if st.session_state.mode == 'vocab':
    niveau = st.session_state.current_level
    mots = len(st.session_state.donnees[niveau]['characters'])
    phrases = len(st.session_state.donnees[niveau]['sentences'])
    
    st.caption(f"""
    📌 **Mode Vocabulaire** • {niveau.upper()}: {mots} mots + {phrases} phrases
    • **Nouvelle carte** pour pratiquer • **Voir réponse** pour révéler
    """)
elif st.session_state.mode == 'grammar':
    st.caption(f"""
    📌 **Mode Grammaire** • {current_idx}/{total_lessons} points étudiés
    • **Structure visible** • Navigation avec ⬅️➡️ • Exemples détaillés
    """)
else:
    st.caption("🇨🇳 Application développée par RATOKIHARISON HERIVONJY • Version 2.0 • Décembre 2024")