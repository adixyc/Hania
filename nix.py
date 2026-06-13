import os
import re
import asyncio
import random
import time

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.users import GetFullUserRequest


# ---------- TELEGRAM ----------

api_id = 36232961
api_hash = "2c01bde657839aa4dd627c48649e300b"

SESSION = "1BVtsOI8Bu8a33Ztj7sVk-KXY7gvgvyJ69-ltxxwebiSDy3tYxNZ8M_5wwrcPR0Vn5Irx4VC5Hiet3cJo66CsNTG_H0whkKDj2hP-yTXWVR-KytdxPP5PZAREjz6lpeyQEx2afYVBEomWxjLF8Lu9CewzSumLaUDh2ufPZqWiHPdRpx6LzC0V65EJrkXB6xdvGyCGGNSrlKz-Uy7vI4clbVzBBIxQMNxDdFUwJctHU95Fov4czAmNVM-uM0EkUBXZ9WOVMmiE7t2xcs5Jc1jJofoeXnzAJdIqdOF9m5HVkS2I4DCvmO8qUGuz7v7We_K_-Z5UD5KmGgMJpM4lhsvv1VBUpT8I0ZA="

client = TelegramClient(
    StringSession(SESSION),
    api_id,
    api_hash
)


TARGET_GROUP_ID = -1003623091628

replied_users = set()

start_time = time.time()


quotes = [
    "HeIIo ji"
]


ALLOWED_USERNAMES = [
    "@SWAPPINGe_WIFE",
    "@STAR_NAVYA",
    "@niximia"
]


# ---------- BIO CHECK ----------

async def has_link_in_bio(user_id):

    try:

        full = await client(
            GetFullUserRequest(user_id)
        )

        bio = full.full_user.about or ""


        for x in ALLOWED_USERNAMES:
            bio = bio.replace(x, "")


        patterns = [
            r"@\w+",
            r"t\.me/\w+",
            r"https?://",
            r"www\."
        ]


        return any(
            re.search(p,bio,re.I)
            for p in patterns
        )


    except Exception as e:
        print("BIO ERROR:",e)
        return False



# ---------- BACKGROUND ----------

async def fake_typing():

    while True:

        try:

            async with client.action(
                TARGET_GROUP_ID,
                "typing"
            ):
                await asyncio.sleep(
                    random.randint(6,12)
                )

        except Exception as e:
            print(e)

        await asyncio.sleep(10)



async def send_quotes():

    while True:

        try:

            dialogs = await client.get_dialogs()

            for d in dialogs:

                if d.is_group:

                    await client.send_message(
                        d.id,
                        random.choice(quotes)
                    )

                    await asyncio.sleep(40)


        except Exception as e:
            print("QUOTE ERROR:",e)


        await asyncio.sleep(330)



# ---------- PRIVATE AUTO REPLY ----------

@client.on(events.NewMessage(incoming=True))

async def private_reply(event):

    if not event.is_private:
        return

    if event.sender_id in replied_users:
        return


    replied_users.add(event.sender_id)


    await asyncio.sleep(2)


    await event.reply(
"""
Hey dear thank you for messaging me 🥰

Join @GF_SWAPPING

After joining message me again ❤️
"""
)



# ---------- DELETE BIO LINK USERS ----------


@client.on(events.NewMessage(chats=TARGET_GROUP_ID))

async def bio_filter(event):

    try:

        sender = await event.get_sender()


        if sender.bot or sender.is_self:
            return


        perms = await client.get_permissions(
            TARGET_GROUP_ID,
            sender.id
        )


        if perms.is_admin:
            return



        if await has_link_in_bio(sender.id):

            await event.delete()

            print(
                "Deleted:",
                sender.id
            )


    except Exception as e:
        print("FILTER ERROR:",e)



# ---------- DELETE ALL MSG AFTER 60 SEC ----------


@client.on(events.NewMessage(chats=TARGET_GROUP_ID))

async def delete_all(event):

    try:

        await asyncio.sleep(60)

        await event.delete()


    except:
        pass



# ---------- COMMANDS ----------


@client.on(
events.NewMessage(
outgoing=True,
pattern=r"\.hi"
)
)

async def hi(event):

    await event.edit("Online")



@client.on(
events.NewMessage(
outgoing=True,
pattern=r"\.rl"
)
)

async def rate(event):

    await event.edit(
"""
📋 RATE LIST

🇮🇳 India ₹10
🇺🇸 USA ₹20
🇬🇧 UK ₹25

💳 UPI Only
⚡ Instant Delivery
"""
)



# ---------- START ----------


async def start():

    await client.start()

    print(
        "BOT RUNNING"
    )


    asyncio.create_task(
        fake_typing()
    )

    asyncio.create_task(
        send_quotes()
    )


    await client.run_until_disconnected()



while True:

    try:
        asyncio.run(start())

    except Exception as e:

        print(
            "CRASH:",
            e
        )

        time.sleep(5)
