import random
from helper.ffmpeg import fix_thumb, take_screen_shot
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db
from PIL import Image
import asyncio
import os
import time
from helper.utils import add_prefix_suffix
from config import Config

app = Client("test", api_id=Config.STRING_API_ID,
             api_hash=Config.STRING_API_HASH, session_string=Config.STRING_SESSION)

# Directly prompt the user to enter the new file names
@Client.on_message(filters.private & filters.incoming & filters.media)
async def handle_file(client, message):
    await message.reply_text(
        "__Please enter new file names separated by commas for bulk renaming.__",
        reply_to_message_id=message.id,
        reply_markup=ForceReply(True)
    )

# Define the main message handler for private messages with replies
@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if isinstance(reply_message.reply_markup, ForceReply):
        new_names = message.text.split(',')
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        files = msg.reply_to_message.media_group

        if len(new_names) != len(files):
            return await message.reply("The number of new names does not match the number of files. Please try again.")

        await reply_message.delete()

        for file, new_name in zip(files, new_names):
            new_name = new_name.strip()
            media = getattr(file, file.media.value)
            if not "." in new_name:
                if "." in media.file_name:
                    extn = media.file_name.rsplit('.', 1)[-1]
                else:
                    extn = "mkv"
                new_name = new_name + "." + extn

            await start_conversion(client, message, file, new_name)

# Define the conversion process
async def start_conversion(client, message, file, new_name):
    # Creating Directory for Metadata
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    # Extracting necessary information
    prefix = await db.get_prefix(message.chat.id)
    suffix = await db.get_suffix(message.chat.id)

    try:
        # adding prefix and suffix
        new_filename = add_prefix_suffix(new_name, prefix, suffix)
    except Exception as e:
        return await message.reply(f"⚠️ Something went wrong can't able to set Prefix or Suffix ☹️ \n\n❄️ Contact My Creator -> @Urr_Sanjii\nError: {e}")

    file_path = f"downloads/{new_filename}"
    ms = await message.reply("Trying to download")
    try:
        path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("\n⚠️ __**Please wait...**__\n\n❄️ **Download started....**", ms, time.time()))
    except Exception as e:
        return await ms.edit(e)

    _bool_metadata = await db.get_metadata(message.chat.id)

    if _bool_metadata:
        metadata_path = f"Metadata/{new_filename}"
        metadata = await db.get_metadata_code(message.chat.id)
        if metadata:
            await ms.edit("I found your metadata\n\n__**Adding metadata to file....**")
            cmd = f"""ffmpeg -i "{path}" {metadata} "{metadata_path}" """

            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            er = stderr.decode()

            try:
                if er:
                    return await ms.edit(str(er) + "\n\n**Error**")
            except BaseException:
                pass
        await ms.edit("**Metadata added to the file successfully ✅**\n\n⚠️ __**Trying to upload....**")
    else:
        await ms.edit("⚠️  __**Please wait...**__\n\n\n**Trying to upload....**")

    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        parser.close()
    except:
        pass

    ph_path = None
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(message.chat.id)
    c_thumb = await db.get_thumbnail(message.chat.id)

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(
                media.file_size), duration=convert(duration))
        except Exception as e:
            return await ms.edit(text=f"Your caption error except keyword argument: {e}")
    else:
        caption = f"**{new_filename}**"

    if media.thumbs or c_thumb:
        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            width, height, ph_path = await fix_thumb(ph_path)
        else:
            try:
                ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
                width, height, ph_path = await fix_thumb(ph_path_)
            except Exception as e:
                ph_path = None
                print(e)

    if media.file_size > 4000 * 1024 * 1024:
        try:
            await app.send_video(
                message.chat.id,
                video=metadata_path if _bool_metadata else file_path,
                caption=caption,
                thumb=ph_path,
                width=width,
                height=height,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("⚠️ __**Upload started....**", ms, time.time()))
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            if metadata_path:
                os.remove(metadata_path)
            if path:
                os.remove(path)
            return await ms.edit(f"Error {e}")
    else:
        try:
            await client.send_video(
                message.chat.id,
                video=metadata_path if _bool_metadata else file_path,
                caption=caption,
                thumb=ph_path,
                width=width,
                height=height,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("⚠️ __**Please wait...**__\n\n🌨️ **Upload started....**", ms, time.time()))
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            if metadata_path:
                os.remove(metadata_path)
            if path:
                os.remove(path)
            return await ms.edit(f"Error {e}")

    await ms.delete()

    if ph_path:
        os.remove(ph_path)
    if file_path:
        os.remove(file_path)
    if metadata_path:
        os.remove(metadata_path)

if __name__ == "__main__":
    app.run()
