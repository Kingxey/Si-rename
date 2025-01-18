import re
import os
import time

id_pattern = re.compile(r'^.\d+$')


class Config(object):
    # pyro client config
    API_ID = os.environ.get("API_ID", "24817837")  # ⚠️ Required
    API_HASH = os.environ.get("API_HASH", "acd9f0cc6beb08ce59383cf250052686")  # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8115314705:AAGaYTT0jQDl3hqcFC9rijeJlmcacaNVBjg")  # ⚠️ Required

    # premium 4g renaming client
    STRING_API_ID = os.environ.get("STRING_API_ID", "")
    STRING_API_HASH = os.environ.get("STRING_API_HASH", "")
    STRING_SESSION = os.environ.get("STRING_SESSION", "")

    # database config
    DB_NAME = os.environ.get("DB_NAME", "Antiflix")
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://Aniflix:Lipun123@aniflix.q2wina5.mongodb.net/?retryWrites=true&w=majority&appName=Aniflix")
    # other configs
    BOT_UPTIME = time.time()
    START_PIC = os.environ.get("START_PIC", " https://envs.sh/HAv.jpg")
    ADMIN = [int(admin) if id_pattern.search(
        admin) else admin for admin in os.environ.get('ADMIN', '8190849763 7428552084').split()]  # ⚠️ Required
    
    FORCE_SUB = os.environ.get("FORCE_SUB", "Animes_French") # ⚠️ Required Username without @
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002376378205"))  # ⚠️ Required
    FLOOD = int(os.environ.get("FLOOD", '105'))
    BANNED_USERS = set(int(x) for x in os.environ.get(
        "BANNED_USERS", "5267548838").split())

    # wes response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))


class Txt(object):
    # part of text configuration
    START_TXT = """<b>Salut {} ♡゙,\n\n◈ Je suis un bot de renommage de fichier surpuissant.
◈ Je peux renommer des fichiers jusqu'à 4 Go, changer des vignettes, convertir entre vidéo et fichier, et supporter des vignettes personnalisées et des légendes.\n\n• Maintenu par : @Animes_French
"""

    ABOUT_TXT = """<b>━━━━━━━━━━━➣
┣⬡ ᴍy ɴᴀᴍᴇ : {}
┣⬡ ᴘʀᴏɢʀᴀᴍᴇʀ : <a href=https://t.me/kingcey>Kingcey</a>
┣⬡ ɴᴇᴛᴡᴏʀᴋ : <a href=https://t.me/AntiFlix_A>ANTIFLIX</a>
┣⬡ ᴄʜᴀᴛ ɢʀᴏᴜᴘ: <a href=https://t.me/kingcey1>SUPPORT</a>
┣⬡ ᴍʏ ᴏᴡɴᴇʀ / ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/kingcey>Kingcey</a>
━━━━━━━━━━━➣ """

    HELP_TXT = """
🌌 <b><u>Comment Ajouter Une Miniature ?</u></b>
  
<b>•></b> /start Démarrer le bot et envoyé une photo. Et, la miniature sera automatiquement ajouté.
<b>•></b> /del_thumb Utiliser cette commande pour supprimer votre miniature.
<b>•></b> /view_thumb Utiliser cette commande pour voir votre miniature récemment ajouter.


📑 <b><u>Comment ajouter une LEGENDE ? </u></b>

<b>•></b> /set_caption - Utiliser cette Commande pour ajouter une Légende 
<b>•></b> /see_caption - Utiliser cette Commande pour voir votre Légende
<b>•></b> /del_caption - Utiliser cette Commande pour supprimer votre Légende
Exeᴍᴩʟᴇ:- <code> /set_caption 📕 Nom du fichier: {filename}
💾 Sɪᴢᴇ: {filesize}
⏰ Dᴜʀᴀᴛɪᴏɴ: {duration} </code>

✏️ <b><u>Comment Renommer un fichier</u></b>
<b>•></b> Envoyez n'importe quel fichier et tapez le nouveau nom de fichier \n et sélectionnez le format [document, vidéo, audio].           


<b>➜ Kingcey:</b> <a href=https://t.me/Otakukingcey1>Kingcey</a>
"""

    SEND_METADATA = """
❪ SET CUSTOM METADATA ❫

☞ Fᴏʀ Exᴀᴍᴘʟᴇ:-

◦ <code> -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Powered By:- @Otakukingcey1" -metadata author="@straw_hat_bots" -metadata:s:s title="Subtitled By :- @Straw_Hat_Bots" -metadata:s:a title="By :- @Straw_Hat_Bots" -metadata:s:v title="By:- @Straw_Hat_bots" </code>

📥 Fᴏʀ Hᴇʟᴘ Cᴏɴᴛ. @Otakikingcey1
"""

    PROGRESS_BAR = """<b>\n
━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱➜
➪ 🗃️ sɪᴢᴇ: {1} | {2}
➪ ⏳️ ᴅᴏɴᴇ : {0}%
➪ 🚀 sᴘᴇᴇᴅ: {3}/s
➪ ⏰️ ᴇᴛᴀ: {4}
╰━━━━━━━━━━━➜ </b>"""
