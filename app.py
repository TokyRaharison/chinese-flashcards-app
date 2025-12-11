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
            {"character": "它", "pinyin": "tā", "translation": "il/elle (animal/chose)"},
            {"character": "您", "pinyin": "nín", "translation": "vous (poli)"},
            {"character": "这", "pinyin": "zhè", "translation": "ce, cette"},
            {"character": "那", "pinyin": "nà", "translation": "cela, cette"},
            {"character": "谁", "pinyin": "shéi", "translation": "qui"},
            {"character": "什么", "pinyin": "shénme", "translation": "quoi"},
            {"character": "哪", "pinyin": "nǎ", "translation": "quel"},
            {"character": "几", "pinyin": "jǐ", "translation": "combien"},
            {"character": "多少", "pinyin": "duōshao", "translation": "combien"},
            {"character": "怎么样", "pinyin": "zěnmeyàng", "translation": "comment"},
            {"character": "怎么", "pinyin": "zěnme", "translation": "comment"},
            {"character": "为什么", "pinyin": "wèishénme", "translation": "pourquoi"},
            {"character": "哪里", "pinyin": "nǎlǐ", "translation": "où"},
            {"character": "这里", "pinyin": "zhèlǐ", "translation": "ici"},
            {"character": "那里", "pinyin": "nàlǐ", "translation": "là"},
            {"character": "上", "pinyin": "shàng", "translation": "sur, au-dessus"},
            {"character": "下", "pinyin": "xià", "translation": "sous, en dessous"},
            {"character": "前", "pinyin": "qián", "translation": "devant"},
            {"character": "后", "pinyin": "hòu", "translation": "derrière"},
            {"character": "左", "pinyin": "zuǒ", "translation": "gauche"},
            {"character": "右", "pinyin": "yòu", "translation": "droite"},
            {"character": "里", "pinyin": "lǐ", "translation": "dans"},
            {"character": "外", "pinyin": "wài", "translation": "dehors"},
            {"character": "中", "pinyin": "zhōng", "translation": "milieu"},
            {"character": "一", "pinyin": "yī", "translation": "un"},
            {"character": "二", "pinyin": "èr", "translation": "deux"},
            {"character": "三", "pinyin": "sān", "translation": "trois"},
            {"character": "四", "pinyin": "sì", "translation": "quatre"},
            {"character": "五", "pinyin": "wǔ", "translation": "cinq"},
            {"character": "六", "pinyin": "liù", "translation": "six"},
            {"character": "七", "pinyin": "qī", "translation": "sept"},
            {"character": "八", "pinyin": "bā", "translation": "huit"},
            {"character": "九", "pinyin": "jiǔ", "translation": "neuf"},
            {"character": "十", "pinyin": "shí", "translation": "dix"},
            {"character": "零", "pinyin": "líng", "translation": "zéro"},
            {"character": "百", "pinyin": "bǎi", "translation": "cent"},
            {"character": "千", "pinyin": "qiān", "translation": "mille"},
            {"character": "万", "pinyin": "wàn", "translation": "dix mille"},
            {"character": "个", "pinyin": "gè", "translation": "classificateur général"},
            {"character": "本", "pinyin": "běn", "translation": "classificateur pour livres"},
            {"character": "张", "pinyin": "zhāng", "translation": "classificateur pour papiers"},
            {"character": "只", "pinyin": "zhī", "translation": "classificateur pour animaux"},
            {"character": "是", "pinyin": "shì", "translation": "être"},
            {"character": "有", "pinyin": "yǒu", "translation": "avoir"},
            {"character": "在", "pinyin": "zài", "translation": "être à, dans"},
            {"character": "来", "pinyin": "lái", "translation": "venir"},
            {"character": "去", "pinyin": "qù", "translation": "aller"},
            {"character": "到", "pinyin": "dào", "translation": "arriver à"},
            {"character": "回", "pinyin": "huí", "translation": "retourner"},
            {"character": "见", "pinyin": "jiàn", "translation": "voir"},
            {"character": "看", "pinyin": "kàn", "translation": "regarder"},
            {"character": "听", "pinyin": "tīng", "translation": "écouter"},
            {"character": "说", "pinyin": "shuō", "translation": "parler"},
            {"character": "读", "pinyin": "dú", "translation": "lire"},
            {"character": "写", "pinyin": "xiě", "translation": "écrire"},
            {"character": "买", "pinyin": "mǎi", "translation": "acheter"},
            {"character": "卖", "pinyin": "mài", "translation": "vendre"},
            {"character": "吃", "pinyin": "chī", "translation": "manger"},
            {"character": "喝", "pinyin": "hē", "translation": "boire"},
            {"character": "睡", "pinyin": "shuì", "translation": "dormir"},
            {"character": "做", "pinyin": "zuò", "translation": "faire"},
            {"character": "学习", "pinyin": "xuéxí", "translation": "étudier"},
            {"character": "工作", "pinyin": "gōngzuò", "translation": "travailler"},
            {"character": "玩", "pinyin": "wán", "translation": "jouer"},
            {"character": "爱", "pinyin": "ài", "translation": "aimer"},
            {"character": "喜欢", "pinyin": "xǐhuan", "translation": "aimer"},
            {"character": "想", "pinyin": "xiǎng", "translation": "penser, vouloir"},
            {"character": "知道", "pinyin": "zhīdào", "translation": "savoir"},
            {"character": "会", "pinyin": "huì", "translation": "pouvoir, savoir"},
            {"character": "能", "pinyin": "néng", "translation": "pouvoir"},
            {"character": "可以", "pinyin": "kěyǐ", "translation": "pouvoir"},
            {"character": "要", "pinyin": "yào", "translation": "vouloir"},
            {"character": "需要", "pinyin": "xūyào", "translation": "avoir besoin"},
            {"character": "应该", "pinyin": "yīnggāi", "translation": "devoir"},
            {"character": "好", "pinyin": "hǎo", "translation": "bon"},
            {"character": "坏", "pinyin": "huài", "translation": "mauvais"},
            {"character": "大", "pinyin": "dà", "translation": "grand"},
            {"character": "小", "pinyin": "xiǎo", "translation": "petit"},
            {"character": "多", "pinyin": "duō", "translation": "beaucoup"},
            {"character": "少", "pinyin": "shǎo", "translation": "peu"},
            {"character": "高", "pinyin": "gāo", "translation": "haut"},
            {"character": "矮", "pinyin": "ǎi", "translation": "petit (taille)"},
            {"character": "长", "pinyin": "cháng", "translation": "long"},
            {"character": "短", "pinyin": "duǎn", "translation": "court"},
            {"character": "新", "pinyin": "xīn", "translation": "nouveau"},
            {"character": "旧", "pinyin": "jiù", "translation": "vieux"},
            {"character": "漂亮", "pinyin": "piàoliang", "translation": "joli"},
            {"character": "好吃", "pinyin": "hǎochī", "translation": "délicieux"},
            {"character": "好喝", "pinyin": "hǎohē", "translation": "délicieux (boisson)"},
            {"character": "好看", "pinyin": "hǎokàn", "translation": "beau"},
            {"character": "好听", "pinyin": "hǎotīng", "translation": "agréable à écouter"},
            {"character": "好闻", "pinyin": "hǎowén", "translation": "agréable à sentir"},
            {"character": "现在", "pinyin": "xiànzài", "translation": "maintenant"},
            {"character": "今天", "pinyin": "jīntiān", "translation": "aujourd'hui"},
            {"character": "明天", "pinyin": "míngtiān", "translation": "demain"},
            {"character": "昨天", "pinyin": "zuótiān", "translation": "hier"},
            {"character": "早上", "pinyin": "zǎoshàng", "translation": "matin"},
            {"character": "上午", "pinyin": "shàngwǔ", "translation": "matinée"},
            {"character": "中午", "pinyin": "zhōngwǔ", "translation": "midi"},
            {"character": "下午", "pinyin": "xiàwǔ", "translation": "après-midi"},
            {"character": "晚上", "pinyin": "wǎnshàng", "translation": "soir"},
            {"character": "年", "pinyin": "nián", "translation": "année"},
            {"character": "月", "pinyin": "yuè", "translation": "mois"},
            {"character": "日", "pinyin": "rì", "translation": "jour"},
            {"character": "星期", "pinyin": "xīngqī", "translation": "semaine"},
            {"character": "天", "pinyin": "tiān", "translation": "jour, ciel"},
            {"character": "时间", "pinyin": "shíjiān", "translation": "temps"},
            {"character": "点", "pinyin": "diǎn", "translation": "heure"},
            {"character": "分", "pinyin": "fēn", "translation": "minute"},
            {"character": "秒", "pinyin": "miǎo", "translation": "seconde"},
            {"character": "爸爸", "pinyin": "bàba", "translation": "papa"},
            {"character": "妈妈", "pinyin": "māma", "translation": "maman"},
            {"character": "哥哥", "pinyin": "gēge", "translation": "grand frère"},
            {"character": "弟弟", "pinyin": "dìdi", "translation": "petit frère"},
            {"character": "姐姐", "pinyin": "jiějie", "translation": "grande sœur"},
            {"character": "妹妹", "pinyin": "mèimei", "translation": "petite sœur"},
            {"character": "儿子", "pinyin": "érzi", "translation": "fils"},
            {"character": "女儿", "pinyin": "nǚ'ér", "translation": "fille"},
            {"character": "老师", "pinyin": "lǎoshī", "translation": "professeur"},
            {"character": "学生", "pinyin": "xuésheng", "translation": "étudiant"},
            {"character": "朋友", "pinyin": "péngyou", "translation": "ami"},
            {"character": "同学", "pinyin": "tóngxué", "translation": "camarade de classe"},
            {"character": "医生", "pinyin": "yīshēng", "translation": "médecin"},
            {"character": "护士", "pinyin": "hùshi", "translation": "infirmier"},
            {"character": "老板", "pinyin": "lǎobǎn", "translation": "patron"},
            {"character": "工人", "pinyin": "gōngrén", "translation": "ouvrier"},
            {"character": "家", "pinyin": "jiā", "translation": "maison, famille"},
            {"character": "学校", "pinyin": "xuéxiào", "translation": "école"},
            {"character": "医院", "pinyin": "yīyuàn", "translation": "hôpital"},
            {"character": "商店", "pinyin": "shāngdiàn", "translation": "magasin"},
            {"character": "饭店", "pinyin": "fàndiàn", "translation": "restaurant"},
            {"character": "银行", "pinyin": "yínháng", "translation": "banque"},
            {"character": "邮局", "pinyin": "yóujú", "translation": "bureau de poste"},
            {"character": "公园", "pinyin": "gōngyuán", "translation": "parc"},
            {"character": "图书馆", "pinyin": "túshūguǎn", "translation": "bibliothèque"},
            {"character": "电影院", "pinyin": "diànyǐngyuàn", "translation": "cinéma"}
        ],
        "sentences": [
            {"character": "你好！", "pinyin": "Nǐ hǎo!", "translation": "Bonjour !"},
            {"character": "你好吗？", "pinyin": "Nǐ hǎo ma?", "translation": "Comment vas-tu ?"},
            {"character": "我很好，谢谢。", "pinyin": "Wǒ hěn hǎo, xièxie.", "translation": "Je vais bien, merci."},
            {"character": "你叫什么名字？", "pinyin": "Nǐ jiào shénme míngzì?", "translation": "Comment tu t'appelles ?"},
            {"character": "我叫小明。", "pinyin": "Wǒ jiào Xiǎomíng.", "translation": "Je m'appelle Xiaoming."},
            {"character": "你是哪国人？", "pinyin": "Nǐ shì nǎ guó rén?", "translation": "De quel pays es-tu ?"},
            {"character": "我是法国人。", "pinyin": "Wǒ shì Fǎguó rén.", "translation": "Je suis français."},
            {"character": "你会说中文吗？", "pinyin": "Nǐ huì shuō Zhōngwén ma?", "translation": "Sais-tu parler chinois ?"},
            {"character": "我会说一点中文。", "pinyin": "Wǒ huì shuō yīdiǎn Zhōngwén.", "translation": "Je parle un peu chinois."},
            {"character": "多少钱？", "pinyin": "Duōshǎo qián?", "translation": "Combien ça coûte ?"},
            {"character": "太贵了！", "pinyin": "Tài guì le!", "translation": "Trop cher !"},
            {"character": "便宜一点。", "pinyin": "Piányi yīdiǎn.", "translation": "Un peu moins cher."},
            {"character": "我喜欢吃中国菜。", "pinyin": "Wǒ xǐhuan chī Zhōngguó cài.", "translation": "J'aime manger la cuisine chinoise."},
            {"character": "我不喜欢吃辣的。", "pinyin": "Wǒ bù xǐhuan chī là de.", "translation": "Je n'aime pas manger épicé."},
            {"character": "今天天气很好。", "pinyin": "Jīntiān tiānqì hěn hǎo.", "translation": "Aujourd'hui, il fait beau."},
            {"character": "明天会下雨吗？", "pinyin": "Míngtiān huì xià yǔ ma?", "translation": "Est-ce qu'il pleuvra demain ?"},
            {"character": "现在几点了？", "pinyin": "Xiànzài jǐ diǎn le?", "translation": "Quelle heure est-il ?"},
            {"character": "现在三点。", "pinyin": "Xiànzài sān diǎn.", "translation": "Il est trois heures."},
            {"character": "你家在哪儿？", "pinyin": "Nǐ jiā zài nǎr?", "translation": "Où habites-tu ?"},
            {"character": "我家在北京。", "pinyin": "Wǒ jiā zài Běijīng.", "translation": "J'habite à Pékin."},
            {"character": "你去哪儿？", "pinyin": "Nǐ qù nǎr?", "translation": "Où vas-tu ?"},
            {"character": "我去学校。", "pinyin": "Wǒ qù xuéxiào.", "translation": "Je vais à l'école."},
            {"character": "这是什么？", "pinyin": "Zhè shì shénme?", "translation": "Qu'est-ce que c'est ?"},
            {"character": "这是一本书。", "pinyin": "Zhè shì yī běn shū.", "translation": "C'est un livre."},
            {"character": "那是什么？", "pinyin": "Nà shì shénme?", "translation": "Qu'est-ce que c'est ?"},
            {"character": "那是一只猫。", "pinyin": "Nà shì yī zhī māo.", "translation": "C'est un chat."},
            {"character": "我很高兴认识你。", "pinyin": "Wǒ hěn gāoxìng rènshi nǐ.", "translation": "Je suis content de te connaître."},
            {"character": "再见！", "pinyin": "Zàijiàn!", "translation": "Au revoir !"},
            {"character": "明天见！", "pinyin": "Míngtiān jiàn!", "translation": "À demain !"},
            {"character": "谢谢！", "pinyin": "Xièxie!", "translation": "Merci !"},
            {"character": "不客气。", "pinyin": "Bù kèqì.", "translation": "De rien."},
            {"character": "对不起。", "pinyin": "Duìbuqǐ.", "translation": "Désolé."},
            {"character": "没关系。", "pinyin": "Méi guānxi.", "translation": "Ce n'est pas grave."},
            {"character": "请坐。", "pinyin": "Qǐng zuò.", "translation": "Asseyez-vous, s'il vous plaît."},
            {"character": "请进。", "pinyin": "Qǐng jìn.", "translation": "Entrez, s'il vous plaît."},
            {"character": "请喝茶。", "pinyin": "Qǐng hē chá.", "translation": "Prenez du thé, s'il vous plaît."},
            {"character": "请等一下。", "pinyin": "Qǐng děng yīxià.", "translation": "Attendez un instant, s'il vous plaît."},
            {"character": "我可以去吗？", "pinyin": "Wǒ kěyǐ qù ma?", "translation": "Puis-je y aller ?"},
            {"character": "当然可以。", "pinyin": "Dāngrán kěyǐ.", "translation": "Bien sûr."},
            {"character": "不行。", "pinyin": "Bù xíng.", "translation": "Non, pas possible."},
            {"character": "我不知道。", "pinyin": "Wǒ bù zhīdào.", "translation": "Je ne sais pas."},
            {"character": "我明白了。", "pinyin": "Wǒ míngbái le.", "translation": "Je comprends."},
            {"character": "我不明白。", "pinyin": "Wǒ bù míngbái.", "translation": "Je ne comprends pas."},
            {"character": "请再说一遍。", "pinyin": "Qǐng zài shuō yī biàn.", "translation": "Répétez, s'il vous plaît."},
            {"character": "你说什么？", "pinyin": "Nǐ shuō shénme?", "translation": "Qu'est-ce que tu as dit ?"},
            {"character": "请慢一点说。", "pinyin": "Qǐng màn yīdiǎn shuō.", "translation": "Parlez plus lentement, s'il vous plaît."},
            {"character": "你会说英语吗？", "pinyin": "Nǐ huì shuō Yīngyǔ ma?", "translation": "Parlez-vous anglais ?"},
            {"character": "一点点。", "pinyin": "Yīdiǎndiǎn.", "translation": "Un tout petit peu."},
            {"character": "这个怎么用？", "pinyin": "Zhège zěnme yòng?", "translation": "Comment utiliser ceci ?"},
            {"character": "厕所在哪儿？", "pinyin": "Cèsuǒ zài nǎr?", "translation": "Où sont les toilettes ?"}
        ]
    },
    "hsk2": {
        "name": "HSK 2",
        "description": "Niveau élémentaire - 150 mots",
        "characters": [
            {"character": "您", "pinyin": "nín", "translation": "vous (poli)"},
            {"character": "大家", "pinyin": "dàjiā", "translation": "tout le monde"},
            {"character": "每", "pinyin": "měi", "translation": "chaque"},
            {"character": "自己", "pinyin": "zìjǐ", "translation": "soi-même"},
            {"character": "别人", "pinyin": "biérén", "translation": "autres personnes"},
            {"character": "其他", "pinyin": "qítā", "translation": "autres"},
            {"character": "别的", "pinyin": "biéde", "translation": "autre"},
            {"character": "有的", "pinyin": "yǒude", "translation": "certains"},
            {"character": "一些", "pinyin": "yīxiē", "translation": "quelques-uns"},
            {"character": "一点", "pinyin": "yīdiǎn", "translation": "un peu"},
            {"character": "所有", "pinyin": "suǒyǒu", "translation": "tous"},
            {"character": "每个", "pinyin": "měi gè", "translation": "chaque"},
            {"character": "任何", "pinyin": "rènhé", "translation": "n'importe quel"},
            {"character": "第一", "pinyin": "dì yī", "translation": "premier"},
            {"character": "第二", "pinyin": "dì èr", "translation": "deuxième"},
            {"character": "第三", "pinyin": "dì sān", "translation": "troisième"},
            {"character": "最后", "pinyin": "zuìhòu", "translation": "dernier"},
            {"character": "最", "pinyin": "zuì", "translation": "le plus"},
            {"character": "比较", "pinyin": "bǐjiào", "translation": "comparer, relativement"},
            {"character": "非常", "pinyin": "fēicháng", "translation": "très"},
            {"character": "太", "pinyin": "tài", "translation": "trop"},
            {"character": "更", "pinyin": "gèng", "translation": "plus"},
            {"character": "很", "pinyin": "hěn", "translation": "très"},
            {"character": "真", "pinyin": "zhēn", "translation": "vraiment"},
            {"character": "特别", "pinyin": "tèbié", "translation": "spécialement"},
            {"character": "一般", "pinyin": "yībān", "translation": "généralement"},
            {"character": "可能", "pinyin": "kěnéng", "translation": "possible"},
            {"character": "一定", "pinyin": "yīdìng", "translation": "certainement"},
            {"character": "必须", "pinyin": "bìxū", "translation": "devoir, falloir"},
            {"character": "应该", "pinyin": "yīnggāi", "translation": "devoir"},
            {"character": "可以", "pinyin": "kěyǐ", "translation": "pouvoir"},
            {"character": "能够", "pinyin": "nénggòu", "translation": "pouvoir"},
            {"character": "愿意", "pinyin": "yuànyì", "translation": "être disposé à"},
            {"character": "可能", "pinyin": "kěnéng", "translation": "possible"},
            {"character": "可能", "pinyin": "kěnéng", "translation": "probable"},
            {"character": "或者", "pinyin": "huòzhě", "translation": "ou"},
            {"character": "还是", "pinyin": "háishì", "translation": "ou (dans une question)"},
            {"character": "但是", "pinyin": "dànshì", "translation": "mais"},
            {"character": "可是", "pinyin": "kěshì", "translation": "mais"},
            {"character": "虽然", "pinyin": "suīrán", "translation": "bien que"},
            {"character": "因为", "pinyin": "yīnwèi", "translation": "parce que"},
            {"character": "所以", "pinyin": "suǒyǐ", "translation": "donc"},
            {"character": "如果", "pinyin": "rúguǒ", "translation": "si"},
            {"character": "只要", "pinyin": "zhǐyào", "translation": "tant que"},
            {"character": "只有", "pinyin": "zhǐyǒu", "translation": "seulement si"},
            {"character": "除了", "pinyin": "chúle", "translation": "excepté"},
            {"character": "从", "pinyin": "cóng", "translation": "de"},
            {"character": "往", "pinyin": "wǎng", "translation": "vers"},
            {"character": "向", "pinyin": "xiàng", "translation": "vers"},
            {"character": "朝", "pinyin": "cháo", "translation": "vers"},
            {"character": "沿着", "pinyin": "yánzhe", "translation": "le long de"},
            {"character": "经过", "pinyin": "jīngguò", "translation": "passer par"},
            {"character": "通过", "pinyin": "tōngguò", "translation": "par, via"},
            {"character": "为了", "pinyin": "wèile", "translation": "pour"},
            {"character": "关于", "pinyin": "guānyú", "translation": "concernant"},
            {"character": "对于", "pinyin": "duìyú", "translation": "en ce qui concerne"},
            {"character": "根据", "pinyin": "gēnjù", "translation": "selon"},
            {"character": "按照", "pinyin": "ànzhào", "translation": "selon"},
            {"character": "由于", "pinyin": "yóuyú", "translation": "en raison de"},
            {"character": "关于", "pinyin": "guānyú", "translation": "à propos de"},
            {"character": "拿", "pinyin": "ná", "translation": "prendre"},
            {"character": "带", "pinyin": "dài", "translation": "apporter"},
            {"character": "送", "pinyin": "sòng", "translation": "envoyer"},
            {"character": "给", "pinyin": "gěi", "translation": "donner"},
            {"character": "收到", "pinyin": "shōudào", "translation": "recevoir"},
            {"character": "接受", "pinyin": "jiēshòu", "translation": "accepter"},
            {"character": "拒绝", "pinyin": "jùjué", "translation": "refuser"},
            {"character": "同意", "pinyin": "tóngyì", "translation": "être d'accord"},
            {"character": "反对", "pinyin": "fǎnduì", "translation": "s'opposer"},
            {"character": "支持", "pinyin": "zhīchí", "translation": "soutenir"},
            {"character": "帮助", "pinyin": "bāngzhù", "translation": "aider"},
            {"character": "照顾", "pinyin": "zhàogù", "translation": "prendre soin"},
            {"character": "关心", "pinyin": "guānxīn", "translation": "se soucier"},
            {"character": "担心", "pinyin": "dānxīn", "translation": "s'inquiéter"},
            {"character": "害怕", "pinyin": "hàipà", "translation": "avoir peur"},
            {"character": "希望", "pinyin": "xīwàng", "translation": "espérer"},
            {"character": "期望", "pinyin": "qīwàng", "translation": "s'attendre"},
            {"character": "失望", "pinyin": "shīwàng", "translation": "déçu"},
            {"character": "满意", "pinyin": "mǎnyì", "translation": "satisfait"},
            {"character": "不满意", "pinyin": "bù mǎnyì", "translation": "insatisfait"},
            {"character": "高兴", "pinyin": "gāoxìng", "translation": "content"},
            {"character": "快乐", "pinyin": "kuàilè", "translation": "heureux"},
            {"character": "难过", "pinyin": "nánguò", "translation": "triste"},
            {"character": "伤心", "pinyin": "shāngxīn", "translation": "triste"},
            {"character": "生气", "pinyin": "shēngqì", "translation": "en colère"},
            {"character": "紧张", "pinyin": "jǐnzhāng", "translation": "nerveux"},
            {"character": "放松", "pinyin": "fàngsōng", "translation": "détendu"},
            {"character": "累", "pinyin": "lèi", "translation": "fatigué"},
            {"character": "困", "pinyin": "kùn", "translation": "somnolent"},
            {"character": "饿", "pinyin": "è", "translation": "affamé"},
            {"character": "渴", "pinyin": "kě", "translation": "assoiffé"},
            {"character": "冷", "pinyin": "lěng", "translation": "froid"},
            {"character": "热", "pinyin": "rè", "translation": "chaud"},
            {"character": "疼", "pinyin": "téng", "translation": "douloureux"},
            {"character": "舒服", "pinyin": "shūfu", "translation": "confortable"},
            {"character": "不舒服", "pinyin": "bù shūfu", "translation": "inconfortable"},
            {"character": "健康", "pinyin": "jiànkāng", "translation": "en bonne santé"},
            {"character": "生病", "pinyin": "shēngbìng", "translation": "tomber malade"},
            {"character": "医院", "pinyin": "yīyuàn", "translation": "hôpital"},
            {"character": "医生", "pinyin": "yīshēng", "translation": "médecin"},
            {"character": "看病", "pinyin": "kànbìng", "translation": "consulter un médecin"},
            {"character": "吃药", "pinyin": "chī yào", "translation": "prendre des médicaments"},
            {"character": "打针", "pinyin": "dǎ zhēn", "translation": "faire une piqûre"},
            {"character": "检查", "pinyin": "jiǎnchá", "translation": "examiner"},
            {"character": "治疗", "pinyin": "zhìliáo", "translation": "traiter"},
            {"character": "预防", "pinyin": "yùfáng", "translation": "prévenir"},
            {"character": "身体", "pinyin": "shēntǐ", "translation": "corps"},
            {"character": "头", "pinyin": "tóu", "translation": "tête"},
            {"character": "眼睛", "pinyin": "yǎnjing", "translation": "yeux"},
            {"character": "鼻子", "pinyin": "bízi", "translation": "nez"},
            {"character": "嘴", "pinyin": "zuǐ", "translation": "bouche"},
            {"character": "耳朵", "pinyin": "ěrduo", "translation": "oreilles"},
            {"character": "手", "pinyin": "shǒu", "translation": "main"},
            {"character": "脚", "pinyin": "jiǎo", "translation": "pied"},
            {"character": "心", "pinyin": "xīn", "translation": "cœur"},
            {"character": "胃", "pinyin": "wèi", "translation": "estomac"},
            {"character": "肺", "pinyin": "fèi", "translation": "poumons"},
            {"character": "肝", "pinyin": "gān", "translation": "foie"},
            {"character": "肾", "pinyin": "shèn", "translation": "reins"},
            {"character": "血液", "pinyin": "xuèyè", "translation": "sang"},
            {"character": "骨头", "pinyin": "gǔtou", "translation": "os"},
            {"character": "肌肉", "pinyin": "jīròu", "translation": "muscle"},
            {"character": "皮肤", "pinyin": "pífū", "translation": "peau"},
            {"character": "头发", "pinyin": "tóufa", "translation": "cheveux"},
            {"character": "指甲", "pinyin": "zhǐjia", "translation": "ongles"},
            {"character": "牙齿", "pinyin": "yáchǐ", "translation": "dents"}
        ],
        "sentences": [
            {"character": "您在做什么？", "pinyin": "Nín zài zuò shénme?", "translation": "Que faites-vous ?"},
            {"character": "我在学习中文。", "pinyin": "Wǒ zài xuéxí Zhōngwén.", "translation": "J'étudie le chinois."},
            {"character": "你从哪里来？", "pinyin": "Nǐ cóng nǎlǐ lái?", "translation": "D'où viens-tu ?"},
            {"character": "我从法国来。", "pinyin": "Wǒ cóng Fǎguó lái.", "translation": "Je viens de France."},
            {"character": "你去过中国吗？", "pinyin": "Nǐ qùguo Zhōngguó ma?", "translation": "Es-tu allé en Chine ?"},
            {"character": "我去过一次。", "pinyin": "Wǒ qùguo yī cì.", "translation": "J'y suis allé une fois."},
            {"character": "你最喜欢吃什么？", "pinyin": "Nǐ zuì xǐhuan chī shénme?", "translation": "Qu'est-ce que tu préfères manger ?"},
            {"character": "我最喜欢吃面条。", "pinyin": "Wǒ zuì xǐhuan chī miàntiáo.", "translation": "Je préfère manger des nouilles."},
            {"character": "你每天几点起床？", "pinyin": "Nǐ měitiān jǐ diǎn qǐchuáng?", "translation": "À quelle heure te lèves-tu chaque jour ?"},
            {"character": "我通常七点起床。", "pinyin": "Wǒ tōngcháng qī diǎn qǐchuáng.", "translation": "Je me lève généralement à sept heures."},
            {"character": "明天你有空吗？", "pinyin": "Míngtiān nǐ yǒu kòng ma?", "translation": "Es-tu libre demain ?"},
            {"character": "明天我有事。", "pinyin": "Míngtiān wǒ yǒu shì.", "translation": "Demain, j'ai quelque chose à faire."},
            {"character": "周末你想做什么？", "pinyin": "Zhōumò nǐ xiǎng zuò shénme?", "translation": "Que veux-tu faire ce week-end ?"},
            {"character": "我想去看电影。", "pinyin": "Wǒ xiǎng qù kàn diànyǐng.", "translation": "Je veux aller voir un film."},
            {"character": "你家有几口人？", "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?", "translation": "Combien de personnes y a-t-il dans ta famille ?"},
            {"character": "我家有四口人。", "pinyin": "Wǒ jiā yǒu sì kǒu rén.", "translation": "Il y a quatre personnes dans ma famille."},
            {"character": "你爸爸做什么工作？", "pinyin": "Nǐ bàba zuò shénme gōngzuò?", "translation": "Quel travail fait ton père ?"},
            {"character": "我爸爸是工程师。", "pinyin": "Wǒ bàba shì gōngchéngshī.", "translation": "Mon père est ingénieur."},
            {"character": "你妈妈呢？", "pinyin": "Nǐ māma ne?", "translation": "Et ta mère ?"},
            {"character": "我妈妈是老师。", "pinyin": "Wǒ māma shì lǎoshī.", "translation": "Ma mère est enseignante."},
            {"character": "你有兄弟姐妹吗？", "pinyin": "Nǐ yǒu xiōngdì jiěmèi ma?", "translation": "As-tu des frères et sœurs ?"},
            {"character": "我有一个哥哥和一个妹妹。", "pinyin": "Wǒ yǒu yī gè gēge hé yī gè mèimei.", "translation": "J'ai un grand frère et une petite sœur."},
            {"character": "你现在住在哪里？", "pinyin": "Nǐ xiànzài zhù zài nǎlǐ?", "translation": "Où habites-tu maintenant ?"},
            {"character": "我住在巴黎。", "pinyin": "Wǒ zhù zài Bālí.", "translation": "J'habite à Paris."},
            {"character": "你住的房子大吗？", "pinyin": "Nǐ zhù de fángzi dà ma?", "translation": "La maison où tu habites est-elle grande ?"},
            {"character": "不大，但是很舒服。", "pinyin": "Bù dà, dànshì hěn shūfu.", "translation": "Pas grande, mais très confortable."},
            {"character": "你喜欢你的工作吗？", "pinyin": "Nǐ xǐhuan nǐ de gōngzuò ma?", "translation": "Aimes-tu ton travail ?"},
            {"character": "我很喜欢我的工作。", "pinyin": "Wǒ hěn xǐhuan wǒ de gōngzuò.", "translation": "J'aime beaucoup mon travail."},
            {"character": "你每天工作几个小时？", "pinyin": "Nǐ měitiān gōngzuò jǐ gè xiǎoshí?", "translation": "Combien d'heures travailles-tu chaque jour ?"},
            {"character": "我每天工作八个小时。", "pinyin": "Wǒ měitiān gōngzuò bā gè xiǎoshí.", "translation": "Je travaille huit heures par jour."},
            {"character": "你周末休息吗？", "pinyin": "Nǐ zhōumò xiūxi ma?", "translation": "Te reposes-tu le week-end ?"},
            {"character": "是的，我周末休息。", "pinyin": "Shì de, wǒ zhōumò xiūxi.", "translation": "Oui, je me repose le week-end."},
            {"character": "你平时做什么运动？", "pinyin": "Nǐ píngshí zuò shénme yùndòng?", "translation": "Quel sport pratiques-tu habituellement ?"},
            {"character": "我经常跑步和游泳。", "pinyin": "Wǒ jīngcháng pǎobù hé yóuyǒng.", "translation": "Je cours et nage souvent."},
            {"character": "你最喜欢什么颜色？", "pinyin": "Nǐ zuì xǐhuan shénme yánsè?", "translation": "Quelle est ta couleur préférée ?"},
            {"character": "我最喜欢蓝色。", "pinyin": "Wǒ zuì xǐhuan lán sè.", "translation": "Ma couleur préférée est le bleu."},
            {"character": "你的生日是什么时候？", "pinyin": "Nǐ de shēngrì shì shénme shíhòu?", "translation": "Quand est ton anniversaire ?"},
            {"character": "我的生日是五月十号。", "pinyin": "Wǒ de shēngrì shì wǔ yuè shí hào.", "translation": "Mon anniversaire est le 10 mai."},
            {"character": "你今年多大了？", "pinyin": "Nǐ jīnnián duō dà le?", "translation": "Quel âge as-tu cette année ?"},
            {"character": "我今年二十五岁。", "pinyin": "Wǒ jīnnián èrshíwǔ suì.", "translation": "J'ai vingt-cinq ans cette année."},
            {"character": "你结婚了吗？", "pinyin": "Nǐ jiéhūn le ma?", "translation": "Es-tu marié ?"},
            {"character": "还没有，我单身。", "pinyin": "Hái méiyǒu, wǒ dānshēn.", "translation": "Pas encore, je suis célibataire."},
            {"character": "你有男朋友吗？", "pinyin": "Nǐ yǒu nán péngyou ma?", "translation": "As-tu un petit ami ?"},
            {"character": "不，我没有男朋友。", "pinyin": "Bù, wǒ méiyǒu nán péngyou.", "translation": "Non, je n'ai pas de petit ami."},
            {"character": "你有女朋友吗？", "pinyin": "Nǐ yǒu nǚ péngyou ma?", "translation": "As-tu une petite amie ?"},
            {"character": "是的，我有女朋友。", "pinyin": "Shì de, wǒ yǒu nǚ péngyou.", "translation": "Oui, j'ai une petite amie."},
            {"character": "你会开车吗？", "pinyin": "Nǐ huì kāichē ma?", "translation": "Sais-tu conduire ?"},
            {"character": "会，我有驾照。", "pinyin": "Huì, wǒ yǒu jiàzhào.", "translation": "Oui, j'ai un permis de conduire."},
            {"character": "你喜欢旅行吗？", "pinyin": "Nǐ xǐhuan lǚxíng ma?", "translation": "Aimes-tu voyager ?"},
            {"character": "非常喜欢，我去过很多国家。", "pinyin": "Fēicháng xǐhuan, wǒ qùguo hěn duō guójiā.", "translation": "J'aime beaucoup, je suis allé dans de nombreux pays."}
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
# FONCTION POUR OBTENIR UN MOT NON VU
# ============================================================================
def get_unseen_word(niveau_id):
    """Retourne un mot aléatoire non encore vu dans ce niveau"""
    niveau_data = st.session_state.donnees[niveau_id]
    
    # Si c'est la première fois pour ce niveau, initialiser les listes
    if niveau_id not in st.session_state.unseen_words:
        # Créer toutes les combinaisons possibles (caractères + phrases)
        all_items = []
        
        # Ajouter les caractères avec leur type
        for char in niveau_data['characters']:
            item = char.copy()
            item['type'] = 'character'
            item['level'] = niveau_id
            item['original_index'] = niveau_data['characters'].index(char)
            all_items.append(item)
        
        # Ajouter les phrases avec leur type
        for sent in niveau_data['sentences']:
            item = sent.copy()
            item['type'] = 'sentence'
            item['level'] = niveau_id
            item['original_index'] = niveau_data['sentences'].index(sent)
            all_items.append(item)
        
        st.session_state.unseen_words[niveau_id] = all_items
        st.session_state.seen_words[niveau_id]['characters'] = set()
        st.session_state.seen_words[niveau_id]['sentences'] = set()
    
    # Obtenir les mots non vus
    unseen_list = st.session_state.unseen_words[niveau_id]
    
    if not unseen_list:
        # Si tous les mots ont été vus, réinitialiser
        st.session_state.reinitialisation_niveau = niveau_id
        return None
    
    # Choisir un mot aléatoire parmi les non vus
    if unseen_list:
        nouvel_item = random.choice(unseen_list)
        
        # Retirer ce mot de la liste des non vus
        st.session_state.unseen_words[niveau_id] = [item for item in unseen_list 
                                                   if not (item['character'] == nouvel_item['character'] 
                                                          and item['type'] == nouvel_item['type'])]
        
        # Ajouter aux mots vus
        if nouvel_item['type'] == 'character':
            st.session_state.seen_words[niveau_id]['characters'].add(nouvel_item['character'])
        else:
            st.session_state.seen_words[niveau_id]['sentences'].add(nouvel_item['character'])
        
        return nouvel_item
    
    return None

# ============================================================================
# INITIALISATION DE LA SESSION
# ============================================================================
if 'donnees' not in st.session_state:
    st.session_state.donnees = charger_donnees()

if 'grammar_data' not in st.session_state:
    # S'assurer que HSK3_GRAMMAR a la clé 'author'
    if 'author' not in HSK3_GRAMMAR:
        HSK3_GRAMMAR['author'] = 'RATOKIHARISON HERIVONJY'
    st.session_state.grammar_data = HSK3_GRAMMAR

if 'current_level' not in st.session_state:
    st.session_state.current_level = 'hsk3'

if 'current_item' not in st.session_state:
    try:
        if ('hsk3' in st.session_state.donnees and 
            'characters' in st.session_state.donnees['hsk3'] and
            len(st.session_state.donnees['hsk3']['characters']) > 0):
            
            item = st.session_state.donnees['hsk3']['characters'][0].copy()
            item['type'] = 'character'
            item['level'] = 'hsk3'
            st.session_state.current_item = item
            
        else:
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

# NOUVEAUX ÉTATS POUR LE SUIVI DES MOTS VUS
if 'seen_words' not in st.session_state:
    st.session_state.seen_words = {
        'hsk1': {'characters': set(), 'sentences': set()},
        'hsk2': {'characters': set(), 'sentences': set()},
        'hsk3': {'characters': set(), 'sentences': set()}
    }

if 'unseen_words' not in st.session_state:
    st.session_state.unseen_words = {}

if 'reinitialisation_niveau' not in st.session_state:
    st.session_state.reinitialisation_niveau = None

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
    else:
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
                    # Utiliser la nouvelle fonction get_unseen_word
                    nouvel_item = get_unseen_word(level_id)
                    if nouvel_item:
                        st.session_state.current_item = nouvel_item
                    else:
                        # Si aucun mot disponible, prendre un aléatoire
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
                # Afficher le nombre de mots non vus
                if level_id in st.session_state.unseen_words:
                    unseen_count = len(st.session_state.unseen_words[level_id])
                    st.caption(f"{unseen_count}/{total}")
                else:
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
    
    # Bouton pour réinitialiser le niveau actuel
    if st.session_state.mode == 'vocab' and st.session_state.current_level:
        niveau_data = st.session_state.donnees[st.session_state.current_level]
        if st.button(f"🔄 Réinitialiser {niveau_data['name']}", use_container_width=True):
            # Réinitialiser les listes pour le niveau actuel
            all_items = []
            
            # Caractères
            for char in niveau_data['characters']:
                item = char.copy()
                item['type'] = 'character'
                item['level'] = st.session_state.current_level
                item['original_index'] = niveau_data['characters'].index(char)
                all_items.append(item)
            
            # Phrases
            for sent in niveau_data['sentences']:
                item = sent.copy()
                item['type'] = 'sentence'
                item['level'] = st.session_state.current_level
                item['original_index'] = niveau_data['sentences'].index(sent)
                all_items.append(item)
            
            st.session_state.unseen_words[st.session_state.current_level] = all_items
            st.session_state.seen_words[st.session_state.current_level]['characters'] = set()
            st.session_state.seen_words[st.session_state.current_level]['sentences'] = set()
            
            st.success(f"✅ {niveau_data['name']} réinitialisé !")
            st.rerun()
    
    if st.button("🔄 Réinitialiser stats", use_container_width=True):
        st.session_state.stats = {'total_viewed': 0, 'grammar_viewed': 0, 'by_level': {'hsk1': 0, 'hsk2': 0, 'hsk3': 0}}
        st.success("✅ Statistiques réinitialisées !")
        st.rerun()
    
    st.divider()
    st.caption(f"💾 {DATA_FILE}")
    
    # CORRECTION ICI : Utiliser get() pour éviter KeyError
    author_name = st.session_state.grammar_data.get('author', 'RATOKIHARISON HERIVONJY')
    st.caption(f"👤 Développé par {author_name}")

# ============================================================================
# PAGE À PROPOS
# ============================================================================
if st.session_state.mode == 'about':
    st.header("ℹ️ À propos de cette application")
    
    with st.container(border=True):
        author_name = st.session_state.grammar_data.get('author', 'RATOKIHARISON HERIVONJY')
        
        st.markdown(f"""
        ## 🇨🇳 **Flashcards Chinois HSK**
        
        ### 👨‍💻 **Développeur**
        **{author_name}**
        
        ### 📚 **Description**
        Application web pour apprendre le chinois, développée avec **Streamlit**.
        
        ### ✨ **Nouveautés**
        - **🔄 Système sans répétition** : Les mots ne se répètent qu'après avoir tous été vus
        - **📈 Suivi de progression** : Visualisez les mots déjà étudiés
        - **🎯 Révision efficace** : Optimisé pour la mémorisation à long terme
        
        ### 📊 **Statistiques avancées**
        - Nombre de mots restants par niveau
        - Pourcentage de complétion
        - Réinitialisation par niveau
        
        ### 🔧 **Technologies utilisées**
        - **Python** avec **Streamlit** pour l'interface web
        - **JSON** pour le stockage des données
        - **Session state** pour le suivi en temps réel
        
        ### 📁 **Contenu inclus**
        - **HSK 1** : 150 mots + phrases d'exemple
        - **HSK 2** : 150 mots + phrases d'exemple  
        - **HSK 3** : Système d'ajout de vos mots personnels
        - **Grammaire HSK 3** : 10+ points grammaticaux essentiels
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
    st.caption("**Version 2.1** • Système sans répétition • Décembre 2024 • 🇨🇳 加油！")

# ============================================================================
# MODE VOCABULAIRE
# ============================================================================
elif st.session_state.mode == 'vocab':
    niveau_actuel = st.session_state.donnees[st.session_state.current_level]
    
    st.header(f"📖 {niveau_actuel['name']}")
    st.caption(f"{niveau_actuel['description']}")
    
    # Afficher une alerte si réinitialisation nécessaire
    if st.session_state.reinitialisation_niveau == st.session_state.current_level:
        st.success(f"""
        🎉 **Félicitations !** 
        
        Vous avez vu tous les mots du **{niveau_actuel['name']}** !
        
        La liste va maintenant être réinitialisée pour recommencer.
        """)
        st.session_state.reinitialisation_niveau = None
    
    # Métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Caractères", len(niveau_actuel['characters']))
    with col2:
        st.metric("Phrases", len(niveau_actuel['sentences']))
    with col3:
        total_niveau = len(niveau_actuel['characters']) + len(niveau_actuel['sentences'])
        st.metric("Total", total_niveau)
    
    # Indicateur de progression
    if st.session_state.current_level in st.session_state.unseen_words:
        total_words = len(niveau_actuel['characters']) + len(niveau_actuel['sentences'])
        
        if st.session_state.current_level in st.session_state.seen_words:
            seen_chars = len(st.session_state.seen_words[st.session_state.current_level]['characters'])
            seen_sents = len(st.session_state.seen_words[st.session_state.current_level]['sentences'])
            seen_total = seen_chars + seen_sents
        else:
            seen_total = 0
        
        # Calculer le pourcentage
        if total_words > 0:
            progress_percent = (seen_total / total_words) * 100
            
            st.divider()
            col_prog1, col_prog2 = st.columns([3, 1])
            with col_prog1:
                st.progress(progress_percent / 100, text=f"Progression : {seen_total}/{total_words} mots")
            with col_prog2:
                st.caption(f"{progress_percent:.0f}% complété")
    
    st.divider()
    
    # FLASHCARD VOCABULAIRE
    st.subheader("🎴 Flashcard")
    
    with st.container(border=True):
        # Boutons d'action
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🔄 Nouvelle carte", type="primary", use_container_width=True, key="new_card_vocab"):
                # Utiliser la nouvelle fonction get_unseen_word
                nouvel_item = get_unseen_word(st.session_state.current_level)
                
                if nouvel_item:
                    st.session_state.current_item = nouvel_item
                    st.session_state.show_answer = False
                    
                    # Mettre à jour les stats
                    st.session_state.stats['total_viewed'] += 1
                    st.session_state.stats['by_level'][st.session_state.current_level] += 1
                    
                    st.rerun()
                else:
                    # Si tous les mots ont été vus, réinitialiser
                    niveau_data = st.session_state.donnees[st.session_state.current_level]
                    
                    # Recréer la liste complète
                    all_items = []
                    for char in niveau_data['characters']:
                        item = char.copy()
                        item['type'] = 'character'
                        item['level'] = st.session_state.current_level
                        item['original_index'] = niveau_data['characters'].index(char)
                        all_items.append(item)
                    
                    for sent in niveau_data['sentences']:
                        item = sent.copy()
                        item['type'] = 'sentence'
                        item['level'] = st.session_state.current_level
                        item['original_index'] = niveau_data['sentences'].index(sent)
                        all_items.append(item)
                    
                    st.session_state.unseen_words[st.session_state.current_level] = all_items
                    st.session_state.seen_words[st.session_state.current_level]['characters'] = set()
                    st.session_state.seen_words[st.session_state.current_level]['sentences'] = set()
                    
                    # Choisir un nouvel item
                    if all_items:
                        nouvel_item = random.choice(all_items)
                        
                        # Retirer de la liste des non vus
                        st.session_state.unseen_words[st.session_state.current_level] = [
                            item for item in all_items 
                            if not (item['character'] == nouvel_item['character'] 
                                   and item['type'] == nouvel_item['type'])
                        ]
                        
                        st.session_state.current_item = nouvel_item
                        st.session_state.show_answer = False
                        
                        # Mettre à jour les stats
                        st.session_state.stats['total_viewed'] += 1
                        st.session_state.stats['by_level'][st.session_state.current_level] += 1
                        
                        st.rerun()
        
        with col2:
            if st.button("👁️ Voir réponse", use_container_width=True, key="show_answer_vocab"):
                st.session_state.show_answer = True
                st.rerun()
        
        st.divider()
        
        # Affichage de la carte
        if st.session_state.current_item:
            item = st.session_state.current_item
            
            # Afficher le numéro si disponible
            if 'original_index' in item:
                st.caption(f"Mot n°{item['original_index'] + 1}")
            
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
                        # Mettre à jour la liste des mots non vus
                        if 'hsk3' in st.session_state.unseen_words:
                            # Ajouter le nouveau mot aux non vus
                            nouveau_item = {
                                'character': caractere,
                                'pinyin': pinyin,
                                'translation': traduction,
                                'type': 'character' if type_item == 'character' else 'sentence',
                                'level': 'hsk3',
                                'original_index': len(st.session_state.donnees['hsk3']['characters' if type_item == 'character' else 'sentences']) - 1
                            }
                            st.session_state.unseen_words['hsk3'].append(nouveau_item)
                        
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
    with st.expander("📋 Détails du suivi"):
        if st.session_state.current_level in st.session_state.seen_words:
            seen_chars = len(st.session_state.seen_words[st.session_state.current_level]['characters'])
            seen_sents = len(st.session_state.seen_words[st.session_state.current_level]['sentences'])
            unseen_count = len(st.session_state.unseen_words.get(st.session_state.current_level, []))
            
            st.write(f"**Statistiques pour {niveau_actuel['name']}:**")
            st.write(f"- Caractères vus : {seen_chars}/{len(niveau_actuel['characters'])}")
            st.write(f"- Phrases vues : {seen_sents}/{len(niveau_actuel['sentences'])}")
            st.write(f"- Mots restants : {unseen_count}")
            
            if seen_chars > 0:
                st.write("\n**Caractères déjà vus :**")
                for i, char in enumerate(list(st.session_state.seen_words[st.session_state.current_level]['characters'])[:10], 1):
                    st.write(f"{i}. {char}")
                if seen_chars > 10:
                    st.caption(f"... et {seen_chars - 10} autres")

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
    
    if niveau in st.session_state.unseen_words:
        unseen_count = len(st.session_state.unseen_words[niveau])
        st.caption(f"""
        📌 **Mode Vocabulaire** • {niveau.upper()}: {unseen_count} mots restants sur {mots+phrases} total
        • **Nouvelle carte** pour pratiquer • **Voir réponse** pour révéler
        """)
    else:
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
    author_name = st.session_state.grammar_data.get('author', 'RATOKIHARISON HERIVONJY')
    st.caption(f"🇨🇳 Application développée par {author_name} • Version 1.0 • Décembre 2025")
