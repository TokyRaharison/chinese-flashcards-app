#!/usr/bin/env python3
"""
SCRIPT DE CONFIGURATION AUTOMATIQUE
Pour l'application de flashcards chinois Streamlit
"""

import os
import json
import subprocess
import sys

def create_project_structure():
    """Crée toute la structure du projet"""
    
    print("=" * 50)
    print("🇨🇳 CONFIGURATION DE L'APPLICATION STREAMLIT")
    print("=" * 50)
    
    # 1. Créer les dossiers
    folders = ['pages', 'data', 'utils', 'assets']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Dossier créé: {folder}/")
    
    # 2. Créer les fichiers
    files_to_create = {
        'app.py': generate_app_py(),
        'styles.css': generate_styles_css(),
        'requirements.txt': generate_requirements(),
        'data/hsk_data.json': generate_hsk_data(),
        'pages/1_📝_Ajouter.py': generate_add_page(),
        'pages/2_📊_Statistiques.py': generate_stats_page(),
        'utils/helpers.py': generate_helpers()
    }
    
    for file_path, content in files_to_create.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fichier créé: {file_path}")
    
    print("\n" + "=" * 50)
    print("✅ STRUCTURE CRÉÉE AVEC SUCCÈS !")
    print("=" * 50)
    
    # 3. Instructions finales
    print("\n📋 PROCHAINES ÉTAPES :")
    print("1. Installez les dépendances :")
    print("   pip install -r requirements.txt")
    print("\n2. Lancez l'application :")
    print("   streamlit run app.py")
    print("\n3. Ouvrez votre navigateur à :")
    print("   http://localhost:8501")
    print("\n4. Commencez à ajouter vos mots HSK 3 !")
    
    # 4. Option : installer automatiquement
    response = input("\n📦 Voulez-vous installer les dépendances maintenant ? (o/n): ")
    if response.lower() == 'o':
        print("\n🔄 Installation des dépendances...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées !")
        
        # Lancer l'application ?
        launch = input("\n🚀 Voulez-vous lancer l'application maintenant ? (o/n): ")
        if launch.lower() == 'o':
            print("\n🌐 Lancement de l'application...")
            print("👉 Ouvrez http://localhost:8501 dans votre navigateur")
            subprocess.run(["streamlit", "run", "app.py"])

# ============================================================================
# FONCTIONS DE GÉNÉRATION DE CONTENU
# ============================================================================

def generate_app_py():
    """Génère le fichier app.py principal"""
    return '''import streamlit as st
import json
import random
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Flashcards Chinois HSK",
    page_icon="🇨🇳",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Charger les styles CSS
def load_css():
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css()

# Initialiser l'état de la session
if 'current_level' not in st.session_state:
    st.session_state.current_level = 'hsk1'
if 'flashcard_flipped' not in st.session_state:
    st.session_state.flashcard_flipped = False
if 'current_item' not in st.session_state:
    st.session_state.current_item = None
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'cards_viewed': 0,
        'last_reset': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'by_level': {'hsk1': 0, 'hsk2': 0, 'hsk3': 0}
    }

# Titre principal
st.title("🇨🇳 Flashcards Chinois HSK")
st.markdown("### Apprenez les caractères et phrases par niveau HSK")

# Charger les données HSK
@st.cache_data
def load_hsk_data():
    try:
        with open('data/hsk_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Fichier de données non trouvé. Exécutez setup.py d'abord.")
        return {'hsk1': {'name': 'HSK 1', 'description': 'Niveau débutant', 'characters': [], 'sentences': []},
                'hsk2': {'name': 'HSK 2', 'description': 'Niveau élémentaire', 'characters': [], 'sentences': []},
                'hsk3': {'name': 'HSK 3', 'description': 'Niveau intermédiaire', 'characters': [], 'sentences': []}}

hsk_data = load_hsk_data()

# ============================================================================
# BARRE LATÉRALE
# ============================================================================
with st.sidebar:
    st.header("📚 Navigation")
    
    # Sélecteur de niveau HSK
    st.subheader("Niveaux HSK")
    for level_id, level_info in hsk_data.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"**{level_info['name']}**", key=f"nav_{level_id}"):
                st.session_state.current_level = level_id
                st.session_state.flashcard_flipped = False
                st.rerun()
        with col2:
            total_items = len(level_info['characters']) + len(level_info['sentences'])
            st.caption(f"📊 {total_items}")
    
    st.divider()
    
    # Statistiques rapides
    st.subheader("📈 Vos statistiques")
    st.metric("Cartes vues", st.session_state.stats['cards_viewed'])
    st.caption(f"Dernière révision: {st.session_state.stats['last_reset']}")
    
    if st.button("🔄 Réinitialiser les stats", use_container_width=True):
        st.session_state.stats['cards_viewed'] = 0
        st.session_state.stats['last_reset'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state.stats['by_level'] = {'hsk1': 0, 'hsk2': 0, 'hsk3': 0}
        st.rerun()
    
    st.divider()
    st.caption("✨ Ajoutez vos mots HSK 3 dans la page 'Ajouter'")

# ============================================================================
# CONTENU PRINCIPAL : APPRENTISSAGE
# ============================================================================

# En-tête avec informations du niveau
level_info = hsk_data[st.session_state.current_level]
st.header(f"{level_info['name']}")
st.caption(f"{level_info['description']}")

# Métriques du niveau
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📖 Caractères", len(level_info['characters']))
with col2:
    st.metric("💬 Phrases", len(level_info['sentences']))
with col3:
    st.metric("👁️ Vues", st.session_state.stats['by_level'].get(st.session_state.current_level, 0))

st.divider()

# ============================================================================
# CONTAINER DE LA FLASHCARD
# ============================================================================
card_container = st.container(border=True)

with card_container:
    st.subheader("🎴 Flashcard")
    
    # Bouton pour une nouvelle carte
    if st.button("🔄 Nouvelle carte", use_container_width=True, type="primary"):
        all_items = level_info['characters'] + level_info['sentences']
        if all_items:
            new_item = random.choice(all_items)
            new_item['type'] = 'character' if new_item in level_info['characters'] else 'sentence'
            st.session_state.current_item = new_item
            st.session_state.flashcard_flipped = False
            st.session_state.stats['cards_viewed'] += 1
            st.session_state.stats['by_level'][st.session_state.current_level] = \\
                st.session_state.stats['by_level'].get(st.session_state.current_level, 0) + 1
            st.rerun()
        else:
            st.warning(f"Aucun élément dans {level_info['name']}. Ajoutez-en d'abord !")
    
    st.divider()
    
    # AFFICHAGE DE LA FLASHCARD
    if st.session_state.current_item:
        item = st.session_state.current_item
        
        # Face AVANT (caractère seulement)
        if not st.session_state.flashcard_flipped:
            st.markdown(f'''
            <div style="text-align: center; padding: 40px;">
                <div style="font-family: 'Noto Sans SC', sans-serif; font-size: 5em; 
                         margin: 20px; color: #1a5fb4;">
                    {item['character']}
                </div>
                <p style="color: #666; font-style: italic;">
                    Cliquez sur "Retourner" pour voir la réponse
                </p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Face ARRIÈRE (toutes les infos)
        else:
            badge_color = "#f0b429" if item['type'] == 'character' else "#c6466d"
            badge_text = "Caractère" if item['type'] == 'character' else "Phrase"
            
            st.markdown(f'''
            <div style="text-align: center; padding: 30px;">
                <div style="font-family: 'Noto Sans SC', sans-serif; font-size: 4em; 
                         margin: 15px; color: #1a5fb4;">
                    {item['character']}
                </div>
                
                <div style="margin: 15px;">
                    <span style="background-color: {badge_color}; color: white; 
                           padding: 8px 20px; border-radius: 25px; font-size: 0.9em;">
                        {badge_text}
                    </span>
                </div>
                
                <div style="font-size: 2.5em; color: #2d3748; margin: 20px; 
                         font-weight: 500;">
                    {item['pinyin']}
                </div>
                
                <div style="font-size: 1.8em; color: #26a269; margin: 15px; 
                         padding: 15px; background-color: #f0fff4; 
                         border-radius: 10px; border-left: 5px solid #38a169;">
                    {item['translation']}
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    else:
        # Première carte par défaut
        st.info("👆 Cliquez sur 'Nouvelle carte' pour commencer !")
        if level_info['characters']:
            default_item = level_info['characters'][0]
            default_item['type'] = 'character'
            st.session_state.current_item = default_item

# ============================================================================
# BOUTONS DE CONTRÔLE
# ============================================================================
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Retourner", use_container_width=True, 
                disabled=not st.session_state.current_item):
        st.session_state.flashcard_flipped = not st.session_state.flashcard_flipped
        st.rerun()

with col2:
    if st.button("👁️ Voir réponse", use_container_width=True,
                disabled=not st.session_state.current_item):
        st.session_state.flashcard_flipped = True
        st.rerun()

with col3:
    if st.button("🎲 Aléatoire HSK3", use_container_width=True):
        if 'hsk3' in hsk_data:
            hsk3_items = hsk_data['hsk3']['characters'] + hsk_data['hsk3']['sentences']
            if hsk3_items:
                new_item = random.choice(hsk3_items)
                new_item['type'] = 'character' if new_item in hsk_data['hsk3']['characters'] else 'sentence'
                st.session_state.current_item = new_item
                st.session_state.current_level = 'hsk3'
                st.session_state.flashcard_flipped = False
                st.session_state.stats['cards_viewed'] += 1
                st.session_state.stats['by_level']['hsk3'] = \\
                    st.session_state.stats['by_level'].get('hsk3', 0) + 1
                st.rerun()

# ============================================================================
# PIED DE PAGE
# ============================================================================
st.divider()
st.caption("""
💡 **Astuce** : Utilisez les pages dans la barre latérale pour ajouter des mots 
et voir vos statistiques détaillées. Vos mots HSK 3 sont automatiquement sauvegardés.
""")
'''

def generate_styles_css():
    """Génère le fichier CSS"""
    return '''/* styles.css - Styles pour l'application Streamlit */

/* Import des polices Google */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

/* Style général de l'application */
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
    font-family: 'Inter', sans-serif;
}

/* Style des titres */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    color: #2d3748;
}

/* Style spécial pour les caractères chinois */
.chinese-character {
    font-family: 'Noto Sans SC', sans-serif;
    font-weight: 700;
}

/* Cartes et conteneurs */
[data-testid="stContainer"] {
    border-radius: 15px;
}

/* Amélioration des boutons */
.stButton > button {
    border-radius: 10px !important;
    border: 1px solid #e2e8f0 !important;
    transition: all 0.3s ease !important;
    font-weight: 500 !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1) !important;
}

/* Bouton primaire (bleu) */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1a5fb4 0%, #2b6cb0 100%) !important;
    border: none !important;
    color: white !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a5fb4 0%, #2c5282 100%);
    color: white;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebar"] .stButton > button {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(255, 255, 255, 0.2) !important;
}

/* Métriques et cartes */
[data-testid="stMetricValue"] {
    font-size: 2em !important;
    font-weight: 700 !important;
}

/* Diviseurs */
hr {
    border-color: #e2e8f0 !important;
    margin: 2em 0 !important;
}

/* Cacher les éléments Streamlit par défaut */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}

/* Style pour les notifications */
.stAlert {
    border-radius: 10px !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .stButton > button {
        font-size: 0.9em !important;
        padding: 0.5em 1em !important;
    }
    
    h1 { font-size: 1.8em !important; }
    h2 { font-size: 1.5em !important; }
    h3 { font-size: 1.2em !important; }
}
'''

def generate_requirements():
    """Génère le fichier requirements.txt"""
    return '''streamlit>=1.28.0
pandas>=2.0.0
'''

def generate_hsk_data():
    """Génère le fichier JSON avec vos mots HSK 3"""
    return json.dumps({
        "hsk1": {
            "name": "HSK 1",
            "description": "Niveau débutant - 150 mots",
            "characters": [
                {"character": "我", "pinyin": "wǒ", "translation": "je, moi"},
                {"character": "你", "pinyin": "nǐ", "translation": "tu"},
                {"character": "他", "pinyin": "tā", "translation": "il"},
                {"character": "她", "pinyin": "tā", "translation": "elle"},
                {"character": "好", "pinyin": "hǎo", "translation": "bon"},
                {"character": "谢谢", "pinyin": "xièxie", "translation": "merci"},
                {"character": "再见", "pinyin": "zàijiàn", "translation": "au revoir"},
                {"character": "是", "pinyin": "shì", "translation": "être"},
                {"character": "不", "pinyin": "bù", "translation": "non"},
                {"character": "一", "pinyin": "yī", "translation": "un"}
            ],
            "sentences": [
                {"character": "你好！", "pinyin": "nǐ hǎo!", "translation": "Bonjour !"},
                {"character": "谢谢您。", "pinyin": "xièxie nín.", "translation": "Merci (poli)."},
                {"character": "我叫李小明。", "pinyin": "wǒ jiào Lǐ Xiǎomíng.", "translation": "Je m'appelle Li Xiaoming."},
                {"character": "我是学生。", "pinyin": "wǒ shì xuéshēng.", "translation": "Je suis étudiant."}
            ]
        },
        "hsk2": {
            "name": "HSK 2",
            "description": "Niveau élémentaire - 150 mots",
            "characters": [
                {"character": "您", "pinyin": "nín", "translation": "vous (poli)"},
                {"character": "喜欢", "pinyin": "xǐhuan", "translation": "aimer"},
                {"character": "吃", "pinyin": "chī", "translation": "manger"},
                {"character": "喝", "pinyin": "hē", "translation": "boire"},
                {"character": "很", "pinyin": "hěn", "translation": "très"},
                {"character": "也", "pinyin": "yě", "translation": "aussi"},
                {"character": "都", "pinyin": "dōu", "translation": "tous"},
                {"character": "今天", "pinyin": "jīntiān", "translation": "aujourd'hui"},
                {"character": "明天", "pinyin": "míngtiān", "translation": "demain"},
                {"character": "现在", "pinyin": "xiànzài", "translation": "maintenant"}
            ],
            "sentences": [
                {"character": "你喜欢吃中国菜吗？", "pinyin": "nǐ xǐhuan chī zhōngguó cài ma?", "translation": "Aimes-tu la cuisine chinoise ?"},
                {"character": "我很高兴。", "pinyin": "wǒ hěn gāoxìng.", "translation": "Je suis très content."},
                {"character": "今天天气很好。", "pinyin": "jīntiān tiānqì hěn hǎo.", "translation": "Le temps est très beau aujourd'hui."},
                {"character": "我现在学习中文。", "pinyin": "wǒ xiànzài xuéxí zhōngwén.", "translation": "J'étudie le chinois maintenant."}
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
                {"character": "我需要买一张火车票。", "pinyin": "wǒ xūyào mǎi yī zhāng huǒchē piào.", "translation": "J'ai besoin d'acheter un billet de train."},
                {"character": "我跟我朋友一起去。", "pinyin": "wǒ gēn wǒ péngyǒu yìqǐ qù.", "translation": "J'y vais avec mon ami."},
                {"character": "他一直很努力学习。", "pinyin": "tā yìzhí hěn nǔlì xuéxí.", "translation": "Il étudie toujours très dur."},
                {"character": "我有很多作业要做。", "pinyin": "wǒ yǒu hěn duō zuòyè yào zuò.", "translation": "J'ai beaucoup de devoirs à faire."}
            ]
        }
    }, ensure_ascii=False, indent=2)

def generate_add_page():
    """Génère la page d'ajout de mots"""
    return '''# 📝 Ajouter des mots HSK
import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="Ajouter des mots - Flashcards Chinois",
    page_icon="📝"
)

st.title("📝 Ajouter des mots HSK")

# Charger les données existantes
@st.cache_data
def load_data():
    with open('data/hsk_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open('data/hsk_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    st.cache_data.clear()

hsk_data = load_data()

# Formulaire d'ajout
with st.form("add_word_form", border=True):
    st.subheader("Ajouter un nouvel élément")
    
    col1, col2 = st.columns(2)
    with col1:
        level = st.selectbox(
            "Niveau HSK",
            ["hsk1", "hsk2", "hsk3"],
            format_func=lambda x: x.upper()
        )
    with col2:
        item_type = st.selectbox(
            "Type d'élément",
            ["character", "sentence"],
            format_func=lambda x: "Caractère/Mot" if x == "character" else "Phrase"
        )
    
    chinese = st.text_input("Caractère(s) chinois *", 
                           placeholder="例如: 谢谢")
    pinyin = st.text_input("Pinyin *", 
                          placeholder="例如: xièxie")
    translation = st.text_input("Traduction française *", 
                               placeholder="例如: merci")
    
    col1, col2 = st.columns(2)
    with col1:
        submitted = st.form_submit_button("💾 Sauvegarder", type="primary", use_container_width=True)
    with col2:
        clear = st.form_submit_button("🗑️ Effacer", use_container_width=True)
    
    if submitted:
        if chinese and pinyin and translation:
            new_item = {
                "character": chinese,
                "pinyin": pinyin,
                "translation": translation
            }
            
            # Ajouter au bon niveau et type
            category = "characters" if item_type == "character" else "sentences"
            hsk_data[level][category].append(new_item)
            save_data(hsk_data)
            
            st.success(f"✅ Élément ajouté avec succès au {level.upper()} !")
            st.balloons()
            
            # Afficher le nouvel élément
            with st.expander("Voir l'élément ajouté"):
                st.write(f"**Caractère:** {chinese}")
                st.write(f"**Pinyin:** {pinyin}")
                st.write(f"**Traduction:** {translation}")
        else:
            st.error("❌ Veuillez remplir tous les champs obligatoires (*)")

st.divider()

# Vue d'ensemble des données
st.subheader("📊 Vue d'ensemble de vos données")

for level_id, level_info in hsk_data.items():
    with st.expander(f"{level_info['name']} - {level_info['description']}"):
        chars_count = len(level_info['characters'])
        sentences_count = len(level_info['sentences'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Caractères/Mots", chars_count)
        with col2:
            st.metric("Phrases", sentences_count)
        
        # Afficher les 5 derniers ajouts
        st.caption(f"Derniers ajouts dans {level_id.upper()}:")
        
        all_items = level_info['characters'][-3:] + level_info['sentences'][-3:]
        for item in all_items[-5:]:
            st.write(f"- **{item['character']}** ({item['pinyin']}): {item['translation']}")

st.caption("💡 Conseil: Ajoutez vos mots HSK 3 après chaque cours pour les pratiquer immédiatement !")
'''

def generate_stats_page():
    """Génère la page de statistiques"""
    return '''# 📊 Statistiques
import streamlit as st
import json
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Statistiques - Flashcards Chinois",
    page_icon="📊"
)

st.title("📊 Statistiques d'apprentissage")

# Charger les données
@st.cache_data
def load_data():
    with open('data/hsk_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

hsk_data = load_data()

# Calculer les statistiques
stats_data = []
for level_id, level_info in hsk_data.items():
    chars = len(level_info['characters'])
    sentences = len(level_info['sentences'])
    total = chars + sentences
    
    stats_data.append({
        "Niveau": level_id.upper(),
        "Caractères": chars,
        "Phrases": sentences,
        "Total": total,
        "Couleur": "#1a5fb4" if level_id == "hsk1" else "#26a269" if level_id == "hsk2" else "#f0b429"
    })

# Créer un DataFrame
df = pd.DataFrame(stats_data)

# Afficher les métriques principales
st.subheader("Résumé global")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total HSK 1", df.loc[df['Niveau'] == 'HSK1', 'Total'].values[0])
with col2:
    st.metric("Total HSK 2", df.loc[df['Niveau'] == 'HSK2', 'Total'].values[0])
with col3:
    st.metric("Total HSK 3", df.loc[df['Niveau'] == 'HSK3', 'Total'].values[0])

st.divider()

# Graphique 1: Répartition par niveau
st.subheader("Répartition du vocabulaire par niveau")

fig1 = px.bar(df, x='Niveau', y='Total', 
              color='Niveau',
              color_discrete_sequence=['#1a5fb4', '#26a269', '#f0b429'],
              text='Total',
              title="Nombre total d'éléments par niveau HSK")
fig1.update_traces(texttemplate='%{text}', textposition='outside')
fig1.update_layout(showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# Graphique 2: Répartition caractères vs phrases
st.subheader("Répartition Caractères vs Phrases par niveau")

fig2 = px.bar(df, x='Niveau', y=['Caractères', 'Phrases'],
              barmode='group',
              color_discrete_sequence=['#3182ce', '#68d391'],
              title="Détail par type d'élément")
st.plotly_chart(fig2, use_container_width=True)

# Tableau détaillé
st.subheader("Tableau détaillé")
st.dataframe(df[['Niveau', 'Caractères', 'Phrases', 'Total']], 
             use_container_width=True, hide_index=True)

# Conseils de progression
st.divider()
st.subheader("🎯 Conseils pour votre progression")

progress_hsk3 = df.loc[df['Niveau'] == 'HSK3', 'Total'].values[0]

if progress_hsk3 < 50:
    st.info(f"**Objectif actuel:** Continuez à ajouter vos mots HSK 3 après chaque cours. Vous avez {progress_hsk3} mots/phrases.")
elif progress_hsk3 < 100:
    st.success(f"**Bonne progression !** Vous avez {progress_hsk3} éléments HSK 3. Pensez à réviser régulièrement.")
else:
    st.balloons()
    st.success(f"**Excellent !** Vous avez maîtrisé {progress_hsk3} éléments HSK 3. Prêt pour le HSK 4 ?")

st.caption(f"Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
'''

def generate_helpers():
    """Génère le fichier d'utilitaires"""
    return '''# utils/helpers.py
"""
Fonctions utilitaires pour l'application de flashcards
"""

import json
import random
from datetime import datetime

def load_hsk_data(filepath='data/hsk_data.json'):
    """Charge les données HSK depuis le fichier JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Fichier {filepath} non trouvé.")
        return None

def save_hsk_data(data, filepath='data/hsk_data.json'):
    """Sauvegarde les données HSK dans le fichier JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_random_item(level_data):
    """
    Retourne un élément aléatoire (caractère ou phrase) du niveau donné
    """
    all_items = level_data['characters'] + level_data['sentences']
    if not all_items:
        return None
    
    item = random.choice(all_items)
    # Ajouter le type pour l'affichage
    item['type'] = 'character' if item in level_data['characters'] else 'sentence'
    return item

def count_items_by_level(hsk_data, level_id):
    """Compte le nombre total d'éléments dans un niveau"""
    if level_id not in hsk_data:
        return 0
    level = hsk_data[level_id]
    return len(level['characters']) + len(level['sentences'])

def add_new_item(hsk_data, level_id, item_type, character, pinyin, translation):
    """Ajoute un nouvel élément aux données HSK"""
    if level_id not in hsk_data:
        return False
    
    new_item = {
        'character': character,
        'pinyin': pinyin,
        'translation': translation
    }
    
    category = 'characters' if item_type == 'character' else 'sentences'
    hsk_data[level_id][category].append(new_item)
    
    return True

def export_to_csv(hsk_data, filename='hsk_vocabulary.csv'):
    """Exporte le vocabulaire HSK vers un fichier CSV"""
    import pandas as pd
    
    data = []
    for level_id, level_info in hsk_data.items():
        for char in level_info['characters']:
            data.append({
                'Niveau': level_id.upper(),
                'Type': 'Caractère',
                'Chinois': char['character'],
                'Pinyin': char['pinyin'],
                'Traduction': char['translation']
            })
        for sentence in level_info['sentences']:
            data.append({
                'Niveau': level_id.upper(),
                'Type': 'Phrase',
                'Chinois': sentence['character'],
                'Pinyin': sentence['pinyin'],
                'Traduction': sentence['translation']
            })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    return filename

def get_progress_stats(hsk_data):
    """Retourne des statistiques de progression"""
    stats = {}
    for level_id in ['hsk1', 'hsk2', 'hsk3']:
        if level_id in hsk_data:
            level = hsk_data[level_id]
            stats[level_id] = {
                'name': level['name'],
                'characters': len(level['characters']),
                'sentences': len(level['sentences']),
                'total': len(level['characters']) + len(level['sentences'])
            }
    return stats

if __name__ == "__main__":
    # Test des fonctions
    data = load_hsk_data()
    if data:
        print("✅ Données HSK chargées avec succès")
        print(f"HSK1: {count_items_by_level(data, 'hsk1')} éléments")
        print(f"HSK2: {count_items_by_level(data, 'hsk2')} éléments")
        print(f"HSK3: {count_items_by_level(data, 'hsk3')} éléments")
'''

if __name__ == "__main__":
    create_project_structure()