import os, time, math, shutil, pyromod.listen
from urllib.parse import unquote
from pySmartDL import SmartDL
from urllib.error import HTTPError
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import BadRequest

# Configs
API_HASH = os.environ['API_HASH'] # Api hash
APP_ID = int(os.environ['APP_ID']) # Api id/App id
BOT_TOKEN = os.environ['BOT_TOKEN'] # Bot token
OWNER_ID = os.environ['OWNER_ID'] # Your telegram id
AS_ZIP = bool(os.environ['AS_ZIP']) # Upload method. If True: will Zip all your files and send as zipfile | If False: will send file one by one
BUTTONS = bool(os.environ['BUTTONS']) # Upload mode. If True: will send buttons (Zip or One by One) instead of AZ_ZIP | If False: will do as you've fill on AZ_ZIP

# Buttons
START_BUTTONS=[
    [
         InlineKeyboardButton('🎬𝗠𝗢𝗩𝗜𝗘𝗦🎬', url='https://t.me/joinchat/vii7DDEvKCZkNDVl'),
         InlineKeyboardButton('💢𝗧𝗩 𝗦𝗘𝗥𝗜𝗘𝗦💢', url='https://t.me/joinchat/Qea8OllY2QUzMDY1')
         
    ],
    [
        InlineKeyboardButton("📣📣 BOTS CHANNEL📣📣", url="https://t.me/DeltaBotsOfficial")
    ],
    [
 InlineKeyboardButton(" 𝗠𝗢𝗩𝗜𝗘𝗦 𝗕𝗔𝗖𝗞𝗨𝗣 𝗖𝗛𝗔𝗡𝗡𝗘𝗟𝗦 ", url="https://t.me/joinchat/fWTl8WXeWX5kN2Fl")
                       ],
                       [
                       InlineKeyboardButton("⭐️ 𝐌𝐎𝐕𝐈𝐄𝐒 𝐆𝐑𝐎𝐔𝐏 1⭐️", url="https://t.me/joinchat/RSzvS3qax24wMmNl"),
                       InlineKeyboardButton("⭐️ 𝐌𝐎𝐕𝐈𝐄𝐒 𝐆𝐑𝐎𝐔𝐏 2⭐️", url="https://t.me/joinchat/L_lCa57jPUBhNzU1")
                      ],[
                        InlineKeyboardButton('🙋🙋 𝗜𝗡𝗩𝗜𝗧𝗘 𝗬𝗢𝗨𝗥 𝗙𝗥𝗜𝗘𝗡𝗗𝗦 🙋🙋', url='https://telegram.me/share/url?url=https://t.me/joinchat/vii7DDEvKCZkNDVl')
                    ],
                    ]

CB_BUTTONS=[
    [
        InlineKeyboardButton("🗂 Zip 🗂", callback_data="zip")
    ],
    [
        InlineKeyboardButton("📕 One by one 📕", callback_data="1by1")
    ]
]

# Helpers

# https://github.com/SpEcHiDe/AnyDLBot
async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]


# https://github.com/viperadnan-git/google-drive-telegram-bot/blob/main/bot/helpers/downloader.py
def download_file(url, dl_path):
    try:
        dl = SmartDL(url, dl_path, progress_bar=False)
        dl.start()
        filename = dl.get_dest()
        if '+' in filename:
            xfile = filename.replace('+', ' ')
            filename2 = unquote(xfile)
        else:
            filename2 = unquote(filename)
        os.rename(filename, filename2)
        return True, filename
    except HTTPError as error:
        return False, error


# https://github.com/MysteryBots/UnzipBot/blob/master/UnzipBot/functions.py
async def absolute_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


# Running bot
xbot = Client('BulkLoader', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


if OWNER_ID:
    OWNER_FILTER = filters.chat(int(OWNER_ID)) & filters.incoming
else:
    OWNER_FILTER = filters.incoming

# Start message
@xbot.on_message(filters.command('start') & OWNER_FILTER & filters.private)
async def start(bot, update):
    await update.reply_text(f"I'm 📥📥📥BulkLoader 📥📥📥\nYou can 📤📤📤📤 upload list of urls\n\n/help for more details!", True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))


# Helper msg
@xbot.on_message(filters.command('help') & OWNER_FILTER & filters.private)
async def help(bot, update):
    await update.reply_text(f"How to use BulkLoader?!\n\n2 Methods:\n- send command /link and then send 🔗🔗 urls, separated by new line.\n- send txt file (links), separated by new line.", True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))


@xbot.on_message(filters.command('link') & OWNER_FILTER & filters.private)
async def linkloader(bot, update):
    xlink = await bot.ask(update.chat.id, 'Send your 🔗🔗 links, separated each link by new line exp\n\nLink1\nLink2\nLink3', filters='text', timeout=300)
    if BUTTONS == True:
        return await xlink.reply('🟥 You wanna upload files as? 🟥', True, reply_markup=InlineKeyboardMarkup(CB_BUTTONS))
    elif BUTTONS == False:
        pass
    dirs = f'./downloads/{update.from_user.id}'
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    output_filename = str(update.from_user.id)
    filename = f'./{output_filename}.zip'
    pablo = await update.reply_text('📥📥Downloading...📥📥')
    urlx = xlink.text.split('\n')
    rm, total, up = len(urlx), len(urlx), 0
    await pablo.edit_text(f"Total: {total}\n✅✅Downloaded: {up}\n📥📥Downloading: {rm}")
    for url in urlx:
        download_file(url, dirs)
        up+=1
        rm-=1
        try:
            await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Downloaded: {up}\n📥📥Downloading: {rm}")
        except BadRequest:
            pass
    await pablo.edit_text('📤📤Uploading...📤📤')
    if AS_ZIP == True:
        shutil.make_archive(output_filename, 'zip', dirs)
        start_time = time.time()
        await update.reply_document(
            filename,
            progress=progress_for_pyrogram,
            progress_args=(
                '📤📤Uploading...📤📤',
                pablo,
                start_time
            )
        )
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    elif AS_ZIP == False:
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Uploaded: {up}\n📤📤Uploading: {rm}")
        for files in dldirs:
            start_time = time.time()
            await update.reply_document(
                files,
                progress=progress_for_pyrogram,
                progress_args=(
                    '📤📤Uploading...📤📤',
                    pablo,
                    start_time
                )
            )
            up+=1
            rm-=1
            try:
                await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Uploaded: {up}\n📤📤Uploading: {rm}")
            except BadRequest:
                pass
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)


@xbot.on_message(filters.document & OWNER_FILTER & filters.private)
async def loader(bot, update):
    if BUTTONS == True:
        return await update.reply('You wanna upload files as?', True, reply_markup=InlineKeyboardMarkup(CB_BUTTONS))
    elif BUTTONS == False:
        pass
    dirs = f'./downloads/{update.from_user.id}'
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    if not update.document.file_name.endswith('.txt'):
        return
    output_filename = update.document.file_name[:-4]
    filename = f'./{output_filename}.zip'
    pablo = await update.reply_text('📥📥Downloading...📥📥')
    fl = await update.download()
    with open(fl) as f:
        urls = f.read()
        urlx = urls.split('\n')
        rm, total, up = len(urlx), len(urlx), 0
        await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Downloaded: {up}\n📥📥Downloading: {rm}")
        for url in urlx:
            download_file(url, dirs)
            up+=1
            rm-=1
            try:
                await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Downloaded: {up}\n📥📥Downloading: {rm}")
            except BadRequest:
                pass
    await pablo.edit_text('📤📤Uploading...📤📤')
    os.remove(fl)
    if AS_ZIP == True:
        shutil.make_archive(output_filename, 'zip', dirs)
        start_time = time.time()
        await update.reply_document(
            filename,
            progress=progress_for_pyrogram,
            progress_args=(
                '📤📤Uploading...📤📤',
                pablo,
                start_time
            )
        )
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    elif AS_ZIP == False:
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"Total: {total}\n✅✅Uploaded: {up}\n📤📤Uploading: {rm}")
        for files in dldirs:
            start_time = time.time()
            await update.reply_document(
                files,
                progress=progress_for_pyrogram,
                progress_args=(
                    '📤📤Uploading...📤📤',
                    pablo,
                    start_time
                )
            )
            up+=1
            rm-=1
            try:
                await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Uploaded: {up}\n📤📤Uploading: {rm}")
            except BadRequest:
                pass
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)


@xbot.on_callback_query()
async def callbacks(bot: Client, updatex: CallbackQuery):
    cb_data = updatex.data
    update = updatex.message.reply_to_message
    await updatex.message.delete()
    dirs = f'./downloads/{update.from_user.id}'
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    if update.document:
        output_filename = update.document.file_name[:-4]
        filename = f'./{output_filename}.zip'
        pablo = await update.reply_text('📥📥Downloading...📥📥')
        fl = await update.download()
        with open(fl) as f:
            urls = f.read()
            urlx = urls.split('\n')
            rm, total, up = len(urlx), len(urlx), 0
            await pablo.edit_text(f"Total: {total}\n✅✅Downloaded: {up}\n📥📥Downloading: {rm}")
            for url in urlx:
                download_file(url, dirs)
                up+=1
                rm-=1
                try:
                    await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Downloaded: {up}\n📥📥Downloading: {rm}")
                except BadRequest:
                    pass
        os.remove(fl)
    elif update.text:
        output_filename = str(update.from_user.id)
        filename = f'./{output_filename}.zip'
        pablo = await update.reply_text('📥📥Downloading...📥📥')
        urlx = update.text.split('\n')
        rm, total, up = len(urlx), len(urlx), 0
        await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Downloaded: {up}\n📥📥Downloading: {rm}")
        for url in urlx:
            download_file(url, dirs)
            up+=1
            rm-=1
            try:
                await pablo.edit_text(f"Total: {total}\n✅✅Downloaded: {up}\n📥📥Downloading: {rm}")
            except BadRequest:
                pass
    await pablo.edit_text('📤📤Uploading...📤📤')
    if cb_data == 'zip':
        shutil.make_archive(output_filename, 'zip', dirs)
        start_time = time.time()
        await update.reply_document(
            filename,
            progress=progress_for_pyrogram,
            progress_args=(
                '📤📤Uploading...📤📤',
                pablo,
                start_time
            )
        )
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    elif cb_data == '1by1':
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Uploaded: {up}\n📤📤Uploading: {rm}")
        for files in dldirs:
            start_time = time.time()
            await update.reply_document(
                files,
                progress=progress_for_pyrogram,
                progress_args=(
                    '📤📤Uploading...📤📤',
                    pablo,
                    start_time
                )
            )
            up+=1
            rm-=1
            try:
                await pablo.edit_text(f"🧲Total🧲: {total}\n✅✅Uploaded: {up}\n📤📤Uploading: {rm}")
            except BadRequest:
                pass
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)



xbot.run()
