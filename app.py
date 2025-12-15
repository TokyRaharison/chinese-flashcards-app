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
# GRAMMAIRE HSK 3 COMPLÈTE - VERSION CORRIGÉE ET COMPLÈTE
# ============================================================================
HSK3_GRAMMAR = {
    "name": "Grammaire HSK 3 Complète",
    "description": "Tous les points de grammaire du niveau HSK 3 avec exemples détaillés",
    "author": "RATOKIHARISON HERIVONJY",
    "lessons": [
        # === LEÇON 1 ===
        {
            "id": "L1-1",
            "lesson": "HSK3-L1",
            "title": "结果补语'好' (Complément de résultat '好')",
            "structure": "V + 好",
            "example_ch": "我还没想好要不要跟你去呢。",
            "example_pinyin": "Wǒ hái méi xiǎng hǎo yào bu yào gēn nǐ qù ne.",
            "example_fr": "Je n'ai pas encore décidé si je veux aller avec toi.",
            "explanation": "Le complément '好' indique que l'action est bien faite ou terminée."
        },
        {
            "id": "L1-2", 
            "lesson": "HSK3-L1",
            "title": "否定 totale avec '一...也/都' (Négation totale)",
            "structure": "一 + M + N + 也/都 + 不/没 + V",
            "example_ch": "我一个苹果也不吃。/ 我一个苹果也没吃。",
            "example_pinyin": "Wǒ yí gè píngguǒ yě bù chī. / Wǒ yí gè píngguǒ yě méi chī.",
            "example_fr": "Je ne mange pas une seule pomme. / Je n'ai mangé aucune pomme.",
            "explanation": "Exprime une négation absolue. '不' pour les habitudes, '没' pour le passé."
        },
        {
            "id": "L1-3",
            "lesson": "HSK3-L1",
            "title": "否定 avec '一点儿' (Négation avec '一点儿')",
            "structure": "一点儿 + N + 也/都 + 不/没 + V",
            "example_ch": "我一点儿东西也不吃。/ 我一点儿东西也没吃。",
            "example_pinyin": "Wǒ yìdiǎnr dōngxi yě bù chī. / Wǒ yìdiǎnr dōngxi yě méi chī.",
            "example_fr": "Je ne mange rien du tout. / Je n'ai rien mangé du tout.",
            "explanation": "Exprime une négation complète, équivalent à 'rien du tout'."
        },
        {
            "id": "L1-4",
            "lesson": "HSK3-L1",
            "title": "否定 d'adjectif avec '一点儿' (Négation d'adjectif)",
            "structure": "一点儿也/都 + 不 + Adj",
            "example_ch": "我一点儿也不着急。",
            "example_pinyin": "Wǒ yìdiǎnr yě bù zháojí.",
            "example_fr": "Je ne suis pas du tout pressé.",
            "explanation": "Exprime une négation complète d'un état ou d'une qualité."
        },
        {
            "id": "L1-5",
            "lesson": "HSK3-L1", 
            "title": "连词'那' (Conjonction '那')",
            "structure": "A : phrase. B : 那 + phrase.",
            "example_ch": "A：我不想去看电影。 B：那我也不去了。",
            "example_pinyin": "A: Wǒ bù xiǎng qù kàn diànyǐng. B: Nà wǒ yě bú qù le.",
            "example_fr": "A: Je ne veux pas aller au cinéma. B: Alors moi non plus je n'irai pas.",
            "explanation": "'那' signifie 'alors', 'dans ce cas', utilisé pour exprimer une conséquence."
        },
        {
            "id": "L1-6",
            "lesson": "HSK3-L1",
            "title": "简单趋向补语 (Complément directionnel simple)",
            "structure": "V + 来/去",
            "example_ch": "我们过去那边坐一下吧。",
            "example_pinyin": "Wǒmen guòqù nà biān zuò yíxià ba.",
            "example_fr": "Allons nous asseoir là-bas.",
            "explanation": "'来' = mouvement vers le locuteur, '去' = mouvement loin du locuteur."
        },
        {
            "id": "L1-7",
            "lesson": "HSK3-L1",
            "title": "V + 来/去 avec complément de lieu",
            "structure": "V + O(lieu) + 来/去",
            "example_ch": "我上楼去。",
            "example_pinyin": "Wǒ shàng lóu qù.",
            "example_fr": "Je monte à l'étage.",
            "explanation": "Le complément de lieu précède '来/去'."
        },
        {
            "id": "L1-8",
            "lesson": "HSK3-L1",
            "title": "V + 来/去 avec complément d'objet",
            "structure": "V + O(chose) + 来/去  OU  V + 来/去 + O(chose)",
            "example_ch": "明天要带你的作业来。/ 明天要带来你的作业。",
            "example_pinyin": "Míngtiān yào dài nǐ de zuòyè lái. / Míngtiān yào dài lái nǐ de zuòyè.",
            "example_fr": "Apporte tes devoirs demain.",
            "explanation": "Deux positions possibles pour l'objet avec '来/去'."
        },
        
        # === LEÇON 2 ===
        {
            "id": "L2-1",
            "lesson": "HSK3-L2",
            "title": "两个动作连续发生 (Actions successives)",
            "structure": "S + V1了... + 就 V2...",
            "example_ch": "你每天晚上吃了饭就睡觉。",
            "example_pinyin": "Nǐ měitiān wǎnshàng chīle fàn jiù shuìjiào.",
            "example_fr": "Tu vas dormir immédiatement après avoir mangé chaque soir.",
            "explanation": "Exprime qu'une action suit immédiatement une autre."
        },
        {
            "id": "L2-2",
            "lesson": "HSK3-L2",
            "title": "Actions successives avec deux sujets",
            "structure": "S1 + V1了... + S2 + 就 V2...",
            "example_ch": "他到了办公室我就告诉他。",
            "example_pinyin": "Tā dàole bàngōngshì wǒ jiù gàosu tā.",
            "example_fr": "Je lui dirai dès qu'il arrivera au bureau.",
            "explanation": "Quand deux actions ont des sujets différents."
        },
        {
            "id": "L2-3",
            "lesson": "HSK3-L2",
            "title": "反问句'能...吗?' (Phrase rhétorique)",
            "structure": "能...吗？",
            "example_ch": "你每天吃了就睡，能不胖吗？",
            "example_pinyin": "Nǐ měitiān chīle jiù shuì, néng bú pàng ma?",
            "example_fr": "Tu manges et tu dors immédiatement chaque jour, comment ne pas grossir ?",
            "explanation": "Question rhétorique qui exprime une affirmation forte."
        },
        {
            "id": "L2-4",
            "lesson": "HSK3-L2",
            "title": "'或者' pour les choix (Choix ouverts)",
            "structure": "A 或者 B",
            "example_ch": "今晚吃米饭或者面条都可以。",
            "example_pinyin": "Jīnwǎn chī mǐfàn huòzhě miàntiáo dōu kěyǐ.",
            "example_fr": "Tu peux manger du riz ou des nouilles ce soir.",
            "explanation": "'或者' exprime un choix entre alternatives dans une phrase déclarative."
        },
        
        # === LEÇON 3 ===
        {
            "id": "L3-1",
            "lesson": "HSK3-L3",
            "title": "'还是' pour les questions (Choix exclusifs)",
            "structure": "A 还是 B？",
            "example_ch": "明天是晴天还是阴天？",
            "example_pinyin": "Míngtiān shì qíngtiān háishì yīntiān?",
            "example_fr": "Demain il fera beau ou nuageux ?",
            "explanation": "'还是' est utilisé dans les questions pour proposer des choix."
        },
        {
            "id": "L3-2",
            "lesson": "HSK3-L3",
            "title": "'还是' avec incertitude",
            "structure": "phrase + 还是 + phrase",
            "example_ch": "我不知道这个人是男的还是女的。",
            "example_pinyin": "Wǒ bù zhīdào zhège rén shì nán de háishì nǚ de.",
            "example_fr": "Je ne sais pas si cette personne est un homme ou une femme.",
            "explanation": "Exprime l'incertitude entre deux possibilités."
        },
        {
            "id": "L3-3",
            "lesson": "HSK3-L3",
            "title": "存在的表达 (Expression de l'existence)",
            "structure": "Lieu + (没) + V着 + NP",
            "example_ch": "桌子上(没)放着饮料。",
            "example_pinyin": "Zhuōzi shàng (méi) fàngzhe yǐnliào.",
            "example_fr": "Il y a (n'a pas) des boissons sur la table.",
            "explanation": "Décrit ce qui existe ou se trouve à un endroit."
        },
        {
            "id": "L3-4",
            "lesson": "HSK3-L3",
            "title": "'会'表示可能 (Possibilité)",
            "structure": "会 + V/Adj + (的)",
            "example_ch": "喝杯热茶会很舒服。",
            "example_pinyin": "Hē bēi rè chá huì hěn shūfu.",
            "example_fr": "Boire une tasse de thé chaud sera très agréable.",
            "explanation": "'会' exprime une possibilité ou une probabilité."
        },
        
        # === LEÇON 4 ===
        {
            "id": "L4-1",
            "lesson": "HSK3-L4",
            "title": "'又...又...' (À la fois... et...)",
            "structure": "又 + Adj1 + 又 + Adj2",
            "example_ch": "她工作又热情又认真。",
            "example_pinyin": "Tā gōngzuò yòu rèqíng yòu rènzhēn.",
            "example_fr": "Elle travaille avec à la fois enthousiasme et sérieux.",
            "explanation": "Exprime deux qualités simultanées."
        },
        {
            "id": "L4-2",
            "lesson": "HSK3-L4",
            "title": "动作的伴随 (Action accompagnée)",
            "structure": "V1着 + (O1) + V2 + (O2)",
            "example_ch": "她总是笑着跟客人说话。",
            "example_pinyin": "Tā zǒngshì xiàozhe gēn kèrén shuōhuà.",
            "example_fr": "Elle parle toujours aux clients en souriant.",
            "explanation": "La première action (avec 着) accompagne la seconde action."
        },
        {
            "id": "L4-3",
            "lesson": "HSK3-L4",
            "title": "'了'表示变化 ('了' pour exprimer un changement)",
            "structure": "phrase + 了",
            "example_ch": "这条裙子是去年买的，今年就不能穿了。",
            "example_pinyin": "Zhè tiáo qúnzi shì qùnián mǎi de, jīnnián jiù bù néng chuān le.",
            "example_fr": "J'ai acheté cette jupe l'année dernière, mais cette année je ne peux plus la porter.",
            "explanation": "'了' en fin de phrase indique un changement d'état."
        },
        {
            "id": "L4-4",
            "lesson": "HSK3-L4",
            "title": "'越来越...' (De plus en plus...)",
            "structure": "越来越 + Adj/V mental + (了)",
            "example_ch": "我做的饭越来越好吃了。",
            "example_pinyin": "Wǒ zuò de fàn yuè lái yuè hǎo chī le.",
            "example_fr": "Ma cuisine devient de plus en plus délicieuse.",
            "explanation": "Exprime une progression graduelle dans le temps."
        },
        
        # === LEÇON 5 ===
        {
            "id": "L5-1",
            "lesson": "HSK3-L5",
            "title": "可能补语 positif (Complément de possibilité positif)",
            "structure": "V + 得 + complément de résultat/direction",
            "example_ch": "我看得清楚那个汉字。",
            "example_pinyin": "Wǒ kàn dé qīngchǔ nàge hànzì.",
            "example_fr": "Je peux voir ce caractère clairement.",
            "explanation": "Exprime la capacité de faire quelque chose."
        },
        {
            "id": "L5-2",
            "lesson": "HSK3-L5",
            "title": "可能补语 négatif (Complément de possibilité négatif)",
            "structure": "V + 不 + complément de résultat/direction",
            "example_ch": "我上不去那个地方。",
            "example_pinyin": "Wǒ shàng bú qù nàge dìfang.",
            "example_fr": "Je ne peux pas monter à cet endroit.",
            "explanation": "Exprime l'impossibilité de faire quelque chose."
        },
        
        # === LEÇON 6 ===
        {
            "id": "L6-1",
            "lesson": "HSK3-L6",
            "title": "Question avec 可能补语 (Question avec complément de possibilité)",
            "structure": "V + 不 + V + 得 + complément ?  OU  V + 得 + complément + V + 不 + complément ?",
            "example_ch": "老师说的话你听不听得见？ / 老师说的话你听得见听不见？",
            "example_pinyin": "Lǎoshī shuō de huà nǐ tīng bu tīng dé jiàn? / Lǎoshī shuō de huà nǐ tīng dé jiàn tīng bú jiàn?",
            "example_fr": "Entends-tu ce que dit le professeur ?",
            "explanation": "Deux formes de questions pour interroger sur la possibilité."
        },
        {
            "id": "L6-2",
            "lesson": "HSK3-L6",
            "title": "'呢'询问处所 ('呢' pour demander le lieu)",
            "structure": "N + 呢？",
            "example_ch": "我的眼镜呢？你看见了吗？",
            "example_pinyin": "Wǒ de yǎnjìng ne? Nǐ kànjiàn le ma?",
            "example_fr": "Où sont mes lunettes ? Les as-tu vues ?",
            "explanation": "'呢' seul après un nom signifie 'où est...?'"
        },
        {
            "id": "L6-3",
            "lesson": "HSK3-L6",
            "title": "'刚' pour une action récente",
            "structure": "S + 刚 + V",
            "example_ch": "儿子刚做完作业。",
            "example_pinyin": "Érzi gāng zuò wán zuòyè.",
            "example_fr": "Mon fils vient juste de finir ses devoirs.",
            "explanation": "'刚' indique qu'une action vient de se terminer."
        },
        {
            "id": "L6-4",
            "lesson": "HSK3-L6",
            "title": "'刚才' pour le passé immédiat",
            "structure": "刚才 + S + V  OU  S + 刚才 + V",
            "example_ch": "刚才儿子在做作业。",
            "example_pinyin": "Gāngcái érzi zài zuò zuòyè.",
            "example_fr": "Mon fils faisait ses devoirs tout à l'heure.",
            "explanation": "'刚才' se réfère à un moment passé récent."
        },
        
        # === LEÇON 7 ===
        {
            "id": "L7-1",
            "lesson": "HSK3-L7",
            "title": "Durée d'action complétée",
            "structure": "S + V + 了 + DURÉE + O",
            "example_ch": "我们唱了两个小时歌。",
            "example_pinyin": "Wǒmen chàngle liǎng gè xiǎoshí gē.",
            "example_fr": "Nous avons chanté pendant deux heures.",
            "explanation": "Exprime la durée d'une action terminée."
        },
        {
            "id": "L7-2",
            "lesson": "HSK3-L7",
            "title": "Durée d'action en cours",
            "structure": "S + V + 了 + DURÉE + O + 了",
            "example_ch": "我们唱了两个小时歌了。",
            "example_pinyin": "Wǒmen chàngle liǎng gè xiǎoshí gē le.",
            "example_fr": "Nous chantons depuis deux heures.",
            "explanation": "Exprime la durée d'une action qui continue."
        },
        {
            "id": "L7-3",
            "lesson": "HSK3-L7",
            "title": "Expression du temps avec '半'",
            "structure": "heure + 半",
            "example_ch": "十点半",
            "example_pinyin": "Shí diǎn bàn",
            "example_fr": "10h30",
            "explanation": "'半' signifie 'demi-heure'."
        },
        {
            "id": "L7-4",
            "lesson": "HSK3-L7",
            "title": "Expression du temps avec '刻'",
            "structure": "heure + 一刻",
            "example_ch": "十点一刻",
            "example_pinyin": "Shí diǎn yí kè",
            "example_fr": "10h15",
            "explanation": "'一刻' signifie 'quart d'heure'."
        },
        {
            "id": "L7-5",
            "lesson": "HSK3-L7",
            "title": "Expression du temps avec '差'",
            "structure": "差 + minutes + (钟) + heure + 了",
            "example_ch": "差十分钟八点了！",
            "example_pinyin": "Chà shí fēnzhōng bā diǎn le!",
            "example_fr": "Il est dix heures moins huit !",
            "explanation": "'差' exprime le temps restant avant l'heure."
        },
        {
            "id": "L7-6",
            "lesson": "HSK3-L7",
            "title": "Expression d'intérêt (1)",
            "structure": "对... (不)感兴趣",
            "example_ch": "我对打篮球(不)感兴趣。",
            "example_pinyin": "Wǒ duì dǎ lánqiú (bù) gǎn xìngqù.",
            "example_fr": "Je (ne) suis (pas) intéressé par le basketball.",
            "explanation": "Exprime l'intérêt ou le désintérêt pour quelque chose."
        },
        {
            "id": "L7-7",
            "lesson": "HSK3-L7",
            "title": "Expression d'intérêt (2)",
            "structure": "对... (没)有兴趣",
            "example_ch": "我对打篮球(没)有兴趣。",
            "example_pinyin": "Wǒ duì dǎ lánqiú (méi) yǒu xìngqù.",
            "example_fr": "Je (n')ai (pas) d'intérêt pour le basketball.",
            "explanation": "Autre façon d'exprimer l'intérêt."
        },
        
        # === LEÇON 8 ===
        {
            "id": "L8-1",
            "lesson": "HSK3-L8",
            "title": "'又' pour la répétition dans le passé",
            "structure": "又 + V (passé)",
            "example_ch": "我昨天看了一个电影，今天又看一个。",
            "example_pinyin": "Wǒ zuótiān kànle yí gè diànyǐng, jīntiān yòu kàn yí gè.",
            "example_fr": "J'ai vu un film hier, et j'en ai vu un autre aujourd'hui.",
            "explanation": "'又' exprime la répétition d'une action dans le passé."
        },
        {
            "id": "L8-2",
            "lesson": "HSK3-L8",
            "title": "'再' pour la répétition dans le futur",
            "structure": "再 + V (futur)",
            "example_ch": "我今天看了一个电影，明天要再看一个。",
            "example_pinyin": "Wǒ jīntiān kànle yí gè diànyǐng, míngtiān yào zài kàn yí gè.",
            "example_fr": "J'ai vu un film aujourd'hui, et je vais en voir un autre demain.",
            "explanation": "'再' exprime la répétition d'une action dans le futur."
        },
        {
            "id": "L8-3",
            "lesson": "HSK3-L8",
            "title": "疑问代词活用 (1) (Utilisation indéfinie des pronoms interrogatifs)",
            "structure": "S + Q + 就 + Q",
            "example_ch": "你哪天有时间就哪天来我家吧。",
            "example_pinyin": "Nǐ nǎ tiān yǒu shíjiān jiù nǎ tiān lái wǒ jiā ba.",
            "example_fr": "Viens chez moi le jour où tu as du temps.",
            "explanation": "Les pronoms interrogatifs utilisés indéfiniment."
        },
        {
            "id": "L8-4",
            "lesson": "HSK3-L8",
            "title": "疑问代词活用 avec deux sujets",
            "structure": "S1 + Q + S2 + 就 + Q",
            "example_ch": "你坐哪儿我就坐哪儿。",
            "example_pinyin": "Nǐ zuò nǎr wǒ jiù zuò nǎr.",
            "example_fr": "Je m'assiérai là où tu t'assieds.",
            "explanation": "Même structure avec deux sujets différents."
        },
        {
            "id": "L8-5",
            "lesson": "HSK3-L8",
            "title": "Structure '越A越B'",
            "structure": "越 A 越 B",
            "example_ch": "山越高越难走。",
            "example_pinyin": "Shān yuè gāo yuè nán zǒu.",
            "example_fr": "Plus la montagne est haute, plus elle est difficile à gravir.",
            "explanation": "Exprime une corrélation entre deux éléments."
        },
        
        # === LEÇON 9 ===
        {
            "id": "L9-1",
            "lesson": "HSK3-L9",
            "title": "Comparaison d'égalité",
            "structure": "A 跟/和 B 一样 (+ Adj)",
            "example_ch": "她的汉语说得跟/和中国人一样好。",
            "example_pinyin": "Tā de Hànyǔ shuō dé gēn/hé Zhōngguó rén yíyàng hǎo.",
            "example_fr": "Elle parle chinois aussi bien qu'un Chinois.",
            "explanation": "Comparaison d'égalité avec '一样'."
        },
        {
            "id": "L9-2",
            "lesson": "HSK3-L9",
            "title": "Comparaison de différence",
            "structure": "A 跟/和 B 不一样",
            "example_ch": "这本书跟/和那本书不一样。",
            "example_pinyin": "Zhè běn shū gēn/hé nà běn shū bù yíyàng.",
            "example_fr": "Ce livre est différent de ce livre-là.",
            "explanation": "Exprime la différence entre deux choses."
        },
        {
            "id": "L9-3",
            "lesson": "HSK3-L9",
            "title": "Comparaison de supériorité avec '比'",
            "structure": "A 比 B + Adj + (complément de degré)",
            "example_ch": "数学比历史难一点儿/一些/得多/多了。",
            "example_pinyin": "Shùxué bǐ lìshǐ nán yìdiǎnr/yìxiē/dé duō/duō le.",
            "example_fr": "Les mathématiques sont un peu/un peu/beaucoup/beaucoup plus difficiles que l'histoire.",
            "explanation": "Comparaison de supériorité avec différents compléments de degré."
        },
        {
            "id": "L9-4",
            "lesson": "HSK3-L9",
            "title": "Comparaison d'infériorité avec '没有'",
            "structure": "A 没有 B + 这么/那么 + Adj",
            "example_ch": "数学没有历史这么/那么难。",
            "example_pinyin": "Shùxué méiyǒu lìshǐ zhème/nàme nán.",
            "example_fr": "Les mathématiques ne sont pas aussi difficiles que l'histoire.",
            "explanation": "Comparaison d'infériorité avec '没有'."
        },
        {
            "id": "L9-5",
            "lesson": "HSK3-L9",
            "title": "Expression des nombres approximatifs (1)",
            "structure": "Num + Num + 1 (ex: 一两、三四、五六...)",
            "example_ch": "学校附近有三四个车站。",
            "example_pinyin": "Xuéxiào fùjìn yǒu sān-sì gè chēzhàn.",
            "example_fr": "Il y a trois ou quatre arrêts de bus près de l'école.",
            "explanation": "Deux nombres consécutifs expriment une approximation."
        },
        
        # === LEÇON 10 ===
        {
            "id": "L10-1",
            "lesson": "HSK3-L10",
            "title": "Phrase en '把' (1)",
            "structure": "A 把 B + V + 了",
            "example_ch": "我把爸爸的生日忘了。",
            "example_pinyin": "Wǒ bǎ bàba de shēngrì wàng le.",
            "example_fr": "J'ai oublié l'anniversaire de papa.",
            "explanation": "Structure '把' pour exprimer le déplacement ou la transformation."
        },
        {
            "id": "L10-2",
            "lesson": "HSK3-L10",
            "title": "Phrase en '把' avec négation",
            "structure": "A + 没/想/希望 + 把 B + V + 了",
            "example_ch": "我没/想/希望/把书看了。",
            "example_pinyin": "Wǒ méi/xiǎng/xīwàng/bǎ shū kàn le.",
            "example_fr": "Je n'ai pas/Je pense/Je souhaite avoir lu le livre.",
            "explanation": "La négation ou les verbes modaux se placent avant '把'."
        },
        
        # === LEÇON 11 ===
        {
            "id": "L11-1",
            "lesson": "HSK3-L11",
            "title": "Expression des nombres approximatifs (2)",
            "structure": "Num + M + N + 左右",
            "example_ch": "王经理两点左右来了个电话。",
            "example_pinyin": "Wáng jīnglǐ liǎng diǎn zuǒyòu láile gè diànhuà.",
            "example_fr": "Le directeur Wang a téléphoné vers deux heures.",
            "explanation": "'左右' après un nombre exprime une approximation."
        },
        {
            "id": "L11-2",
            "lesson": "HSK3-L11",
            "title": "'才' pour actions tardives ou difficiles",
            "structure": "才 + V",
            "example_ch": "来机场的路上我才发现忘记带护照了。",
            "example_pinyin": "Lái jīchǎng de lùshang wǒ cái fāxiàn wàngjì dài hùzhào le.",
            "example_fr": "C'est seulement sur le chemin de l'aéroport que j'ai réalisé avoir oublié mon passeport.",
            "explanation": "'才' expresse qu'une action est tardive, lente ou insatisfaisante."
        },
        {
            "id": "L11-3",
            "lesson": "HSK3-L11",
            "title": "'就' pour actions précoces ou faciles",
            "structure": "就 + V",
            "example_ch": "你怎么这么早就要睡觉了？",
            "example_pinyin": "Nǐ zěnme zhème zǎo jiù yào shuìjiào le?",
            "example_fr": "Pourquoi vas-tu déjà dormir si tôt ?",
            "explanation": "'就' expresse qu'une action est précoce, rapide ou satisfaisante."
        },
        {
            "id": "L11-4",
            "lesson": "HSK3-L11",
            "title": "Phrase en '把' avec lieu (在)",
            "structure": "A 把 B + V + 在 + lieu",
            "example_ch": "老师把作业放在桌子上了。",
            "example_pinyin": "Lǎoshī bǎ zuòyè fàng zài zhuōzi shàng le.",
            "example_fr": "Le professeur a mis les devoirs sur la table.",
            "explanation": "Structure '把' pour placer quelque chose à un endroit."
        },
        {
            "id": "L11-5",
            "lesson": "HSK3-L11",
            "title": "Phrase en '把' avec déplacement (到)",
            "structure": "A 把 B + V + 到 + lieu",
            "example_ch": "我帮你把衣服放到行李箱里吧。",
            "example_pinyin": "Wǒ bāng nǐ bǎ yīfu fàng dào xínglixiāng lǐ ba.",
            "example_fr": "Laisse-moi t'aider à mettre tes vêtements dans la valise.",
            "explanation": "Structure '把' pour déplacer quelque chose vers un endroit."
        },
        {
            "id": "L11-6",
            "lesson": "HSK3-L11",
            "title": "Phrase en '把' avec transfert (给)",
            "structure": "A 把 B + V + 给 + quelqu'un",
            "example_ch": "我把鲜花送给老师了。",
            "example_pinyin": "Wǒ bǎ xiānhuā sòng gěi lǎoshī le.",
            "example_fr": "J'ai offert les fleurs au professeur.",
            "explanation": "Structure '把' pour donner ou transférer quelque chose à quelqu'un."
        },
        
        # === LEÇON 12 ===
        {
            "id": "L12-1",
            "lesson": "HSK3-L12",
            "title": "复合趋向补语 simple (Complément directionnel composé)",
            "structure": "V1 + V2来/去",
            "example_ch": "小狗从房间跑出来。",
            "example_pinyin": "Xiǎo gǒu cóng fángjiān pǎo chūlai.",
            "example_fr": "Le petit chien est sorti de la pièce en courant.",
            "explanation": "Combinaison d'un verbe de direction avec '来/去'."
        },
        {
            "id": "L12-2",
            "lesson": "HSK3-L12",
            "title": "复合趋向补语 avec lieu",
            "structure": "V1 + V2 + O(lieu) + 来/去",
            "example_ch": "弟弟跑下楼去。",
            "example_pinyin": "Dìdi pǎo xià lóu qù.",
            "example_fr": "Le petit frère a couru en bas de l'escalier.",
            "explanation": "Le complément de lieu précède '来/去'."
        },
        {
            "id": "L12-3",
            "lesson": "HSK3-L12",
            "title": "复合趋向补语 avec objet",
            "structure": "V1 + V2 + O(chose) + 来/去  OU  V1 + V2来/去 + O(chose)",
            "example_ch": "老师拿出一本书来。/ 老师拿出来一本书。",
            "example_pinyin": "Lǎoshī ná chū yì běn shū lái. / Lǎoshī ná chūlai yì běn shū.",
            "example_fr": "Le professeur a sorti un livre.",
            "explanation": "Deux positions possibles pour l'objet."
        },
        {
            "id": "L12-4",
            "lesson": "HSK3-L12",
            "title": "复合趋向补语 avec action terminée",
            "structure": "V1(terminé) + V2来/去 + O(chose)",
            "example_ch": "爸爸买回来了一个西瓜。",
            "example_pinyin": "Bàba mǎi huílai le yí gè xīguā.",
            "example_fr": "Papa a acheté et rapporté une pastèque.",
            "explanation": "Quand la première action est terminée."
        },
        {
            "id": "L12-5",
            "lesson": "HSK3-L12",
            "title": "'一边...一边...' (En même temps)",
            "structure": "一边 + V1 + 一边 + V2",
            "example_ch": "我丈夫喜欢一边看报纸一边吃早饭。",
            "example_pinyin": "Wǒ zhàngfu xǐhuan yìbiān kàn bàozhǐ yìbiān chī zǎofàn.",
            "example_fr": "Mon mari aime lire le journal en prenant le petit déjeuner.",
            "explanation": "Exprime deux actions simultanées."
        },
        
        # === LEÇON 13 ===
        {
            "id": "L13-1",
            "lesson": "HSK3-L13",
            "title": "Phrase en '把' avec complément de résultat",
            "structure": "A 把 B + V + complément de résultat",
            "example_ch": "我把衣服洗干净了。",
            "example_pinyin": "Wǒ bǎ yīfu xǐ gānjìng le.",
            "example_fr": "J'ai lavé les vêtements jusqu'à ce qu'ils soient propres.",
            "explanation": "Structure '把' avec résultat de l'action."
        },
        {
            "id": "L13-2",
            "lesson": "HSK3-L13",
            "title": "Phrase en '把' avec complément de direction",
            "structure": "A 把 B + V + complément de direction",
            "example_ch": "请同学们把铅笔拿出来。",
            "example_pinyin": "Qǐng tóngxuémen bǎ qiānbǐ ná chūlai.",
            "example_fr": "S'il vous plaît, sortez vos crayons.",
            "explanation": "Structure '把' avec direction du mouvement."
        },
        {
            "id": "L13-3",
            "lesson": "HSK3-L13",
            "title": "Séquence d'actions",
            "structure": "先..., 再/又..., 然后...",
            "example_ch": "回家以后，我先做作业，再吃饭，然后看电视。",
            "example_pinyin": "Huí jiā yǐhòu, wǒ xiān zuò zuòyè, zài chīfàn, ránhòu kàn diànshì.",
            "example_fr": "Après être rentré à la maison, je fais d'abord mes devoirs, puis je mange, et ensuite je regarde la télé.",
            "explanation": "Exprime l'ordre chronologique des actions."
        },
        
        # === LEÇON 14 ===
        {
            "id": "L14-1",
            "lesson": "HSK3-L14",
            "title": "'除了...以外，...都...' (Exception)",
            "structure": "除了...以外，...都...",
            "example_ch": "除了他，其他人都来了。",
            "example_pinyin": "Chúle tā, qítā rén dōu lái le.",
            "example_fr": "Tout le monde est venu sauf lui.",
            "explanation": "Exprime une exception (tous... sauf...)."
        },
        {
            "id": "L14-2",
            "lesson": "HSK3-L14",
            "title": "'除了...以外，...也/还...' (Addition)",
            "structure": "除了...以外，...也/还...",
            "example_ch": "除了汉语以外，我也/还会说英语。",
            "example_pinyin": "Chúle Hànyǔ yǐwài, wǒ yě/hái huì shuō Yīngyǔ.",
            "example_fr": "En plus du chinois, je parle aussi anglais.",
            "explanation": "Exprime l'addition (en plus de...)."
        },
        
        # === LEÇON 15 ===
        {
            "id": "L15-1",
            "lesson": "HSK3-L15",
            "title": "疑问代词活用 (2)",
            "structure": "...什么... (sans changer le sens)",
            "example_ch": "以后有什么不明白的地方，可以给我打电话。",
            "example_pinyin": "Yǐhòu yǒu shénme bù míngbai de dìfang, kěyǐ gěi wǒ dǎ diànhuà.",
            "example_fr": "Si tu as des choses que tu ne comprends pas à l'avenir, tu peux m'appeler.",
            "explanation": "'什么' utilisé de manière indéfinie, équivalent à 'des choses que'."
        },
        {
            "id": "L15-2",
            "lesson": "HSK3-L15",
            "title": "Expression du degré '极了'",
            "structure": "Adj + 极了",
            "example_ch": "他满意极了。",
            "example_pinyin": "Tā mǎnyì jí le.",
            "example_fr": "Il est extrêmement satisfait.",
            "explanation": "'极了' exprime le degré le plus élevé."
        },
        {
            "id": "L15-3",
            "lesson": "HSK3-L15",
            "title": "Structure conditionnelle '如果...就...'",
            "structure": "如果...(的话)，就...",
            "example_ch": "如果不舒服(的话)，就去医院检查一下吧。",
            "example_pinyin": "Rúguǒ bù shūfu (de huà), jiù qù yīyuàn jiǎnchá yíxià ba.",
            "example_fr": "Si tu ne te sens pas bien, va à l'hôpital pour un examen.",
            "explanation": "Structure conditionnelle standard."
        },
        {
            "id": "L15-4",
            "lesson": "HSK3-L15",
            "title": "Structure conditionnelle avec deux sujets",
            "structure": "S1 + 如果..., S2 + 就...",
            "example_ch": "如果你喜欢，我就给你买。",
            "example_pinyin": "Rúguǒ nǐ xǐhuan, wǒ jiù gěi nǐ mǎi.",
            "example_fr": "Si tu aimes ça, je te l'achète.",
            "explanation": "Conditionnelle avec sujets différents pour chaque proposition."
        },
        
        # === LEÇON 16 ===
        {
            "id": "L16-1",
            "lesson": "HSK3-L16",
            "title": "Complément d'état complexe",
            "structure": "Adj/V + 得 + proposition",
            "example_ch": "人们忙得没时间跟别人见面。",
            "example_pinyin": "Rénmen máng dé méi shíjiān gēn bié rén jiànmiàn.",
            "example_fr": "Les gens sont trop occupés pour voir les autres.",
            "explanation": "Complément d'état qui décrit le degré ou le résultat."
        },
        {
            "id": "L16-2",
            "lesson": "HSK3-L16",
            "title": "Redoublement d'adjectifs monosyllabiques",
            "structure": "Adj + Adj + 的",
            "example_ch": "你的女儿白白的、胖胖的，真可爱。",
            "example_pinyin": "Nǐ de nǚ'ér bái bái de, pàng pàng de, zhēn kě'ài.",
            "example_fr": "Ta fille, toute blanche et potelée, est vraiment mignonne.",
            "explanation": "Redoublement pour exprimer une qualité atténuée ou affective."
        },
        {
            "id": "L16-3",
            "lesson": "HSK3-L16",
            "title": "Redoublement de verbes bisyllabiques",
            "structure": "V(AB) → V(ABAB)",
            "example_ch": "我真应该多锻炼锻炼了。",
            "example_pinyin": "Wǒ zhēn yīnggāi duō duànliàn duànliàn le.",
            "example_fr": "Je devrais vraiment faire plus d'exercice.",
            "explanation": "Redoublement pour exprimer une action brève ou légère."
        },
        
        # === LEÇON 17 ===
        {
            "id": "L17-1",
            "lesson": "HSK3-L17",
            "title": "疑问代词表示任指 (tous les mêmes)",
            "structure": "Q + 都 (pour montrer que tout est identique)",
            "example_ch": "最近我觉得哪儿都不舒服。",
            "example_pinyin": "Zuìjìn wǒ juéde nǎr dōu bù shūfu.",
            "example_fr": "Ces derniers temps, je ne me sens bien nulle part.",
            "explanation": "Les pronoms interrogatifs avec '都' expriment la totalité."
        },
        {
            "id": "L17-2",
            "lesson": "HSK3-L17",
            "title": "Structure conditionnelle '只要...就...'",
            "structure": "S1 + 只要..., S2 + 就...",
            "example_ch": "只要我喜欢，我就买。",
            "example_pinyin": "Zhǐyào wǒ xǐhuan, wǒ jiù mǎi.",
            "example_fr": "Tant que j'aime ça, je l'achète.",
            "explanation": "'只要' exprime une condition suffisante."
        },
        {
            "id": "L17-3",
            "lesson": "HSK3-L17",
            "title": "Phrase avec '使', '叫', '让'",
            "structure": "A + 使/叫/让 + B + Adj/V",
            "example_ch": "运动使他更年轻。",
            "example_pinyin": "Yùndòng shǐ tā gèng niánqīng.",
            "example_fr": "Le sport le rend plus jeune.",
            "explanation": "Ces verbes signifient 'faire faire', 'causer'."
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
