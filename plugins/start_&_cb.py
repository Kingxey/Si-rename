from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import db
from config import Config, Txt
import humanize
from time import sleep


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("🚫 Désolé, vous êtes banni.")
        return

    user = message.from_user
    await db.add_user(client, message)

    button = InlineKeyboardMarkup([
        [InlineKeyboardButton('🫧 Mises à Jour', url='https://t.me/AMAZON_ANIME'),
         InlineKeyboardButton('💫 Support', url='https://t.me/SpyWars_chat')],
        [InlineKeyboardButton('✴️ À propos', callback_data='about'),
         InlineKeyboardButton('❗ Aide', callback_data='help')],
        [InlineKeyboardButton('Contact ✨', url='https://t.me/Kingcey')]
    ])

    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)

    if not Config.STRING_SESSION and file.file_size > 4000 * 1024 * 1024:
        return await message.reply_text("❌ Ce bot ne supporte pas les fichiers de plus de 4Go.")

    text = f"""**Que souhaitez-vous faire avec ce fichier ?**\n
📄 **Nom du fichier** : `{filename}`\n
📦 **Taille** : `{filesize}`"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Renommer", callback_data="rename")],
        [InlineKeyboardButton("✖️ Annuler", callback_data="close")]
    ])

    try:
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=buttons)
    except FloodWait as e:
        await sleep(e.value)
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=buttons)
    except:
        pass


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data

    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('🫧 Mises à Jour', url='https://t.me/AMAZON_ANIME'),
                 InlineKeyboardButton('➕ Support', url='https://t.me/SpyWars_chat')],
                [InlineKeyboardButton('✴️ À propos', callback_data='about'),
                 InlineKeyboardButton('❗ Aide', callback_data='help')],
                [InlineKeyboardButton('Contact ✨', url='https://t.me/Kingcey')]
            ])
        )

    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✘ Fermer", callback_data="close"),
                 InlineKeyboardButton("⟪ Retour", callback_data="start")]
            ])
        )

    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✘ Fermer", callback_data="close"),
                 InlineKeyboardButton("⟪ Retour", callback_data="start")]
            ])
        )

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass
