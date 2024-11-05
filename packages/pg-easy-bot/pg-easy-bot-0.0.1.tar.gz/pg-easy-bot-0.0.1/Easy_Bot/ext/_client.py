from pyrogram import Client as Application
from pyrogram import filters
from pyrogram.handlers import MessageHandler , CallbackQueryHandler , InlineQueryHandler , ChatJoinRequestHandler , ChatMemberUpdatedHandler, chat_join_request_handler , chat_member_updated_handler , user_status_handler,raw_update_handler,chosen_inline_result_handler,deleted_messages_handler,disconnect_handler,edited_message_handler,handler,inline_query_handler,poll_handler
from ._data_classess import Bot , Handlers , MessagesHandlers
from telegram import Bot as ptb_bot
from Easy_Bot.error import NoHandler
from ._commands import get_commands_data
from typing import Optional
from aiohttp import web
from ._web import web_server 
import asyncio
import os


LOGO = """
........................................
.#####...####...##...##...####...#####..
.##..##.##..##..###.###..##..##..##..##.
.#####..######..##.#.##..##..##..##..##.
.##.....##..##..##...##..##..##..##..##.
.##.....##..##..##...##...####...#####..
........................................    
   ├ ᴄᴏᴘʏʀɪɢʜᴛ © 𝟸𝟶𝟸𝟹-𝟸𝟶𝟸𝟺 ᴘᴀᴍᴏᴅ ᴍᴀᴅᴜʙᴀsʜᴀɴᴀ. ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
   ├ ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ  ɢᴘʟ-𝟹.𝟶 ʟɪᴄᴇɴsᴇ.
   └ ʏᴏᴜ ᴍᴀʏ ɴᴏᴛ ᴜsᴇ ᴛʜɪs ғɪʟᴇ ᴇxᴄᴇᴘᴛ ɪɴ ᴄᴏᴍᴘʟɪᴀɴᴄᴇ ᴡɪᴛʜ ᴛʜᴇ ʟɪᴄᴇɴsᴇ.
"""


class client(Application):
    def __init__(
            self,
            bot: Bot,
            start_function: callable,
    ):
        """
        Initialize a client instance.

        Args:
            bot (Bot): The bot class.
        """
        self.token = bot.token
        self.web = bot.web
        self.start_function = start_function
        super().__init__(
            name = bot.name,
            api_id = bot.api_id,
            api_hash = bot.api_hash,
            bot_token = bot.token,
            workers = bot.workers,
            in_memory = bot.in_memory
        )

    async def trigger_callback(self):
        await self.start_function()

    async def start(self):
        await super().start()
        self._bot = await self.get_me()
        self.ptb_bot = ptb_bot(self.token)
        setattr(self, 'ptb_bot', self.ptb_bot)
        os.system('clear')
        print(LOGO + "\n\n" )
        print(f"{self._bot.first_name} - @{self._bot.username} Started")

        if self.web:
            webapp = web.AppRunner(await web_server(self._bot))
            await webapp.setup()
            await web.TCPSite(webapp, "0.0.0.0", 8080).start()
            print(f"Webapp running on http://0.0.0.0:8080")

        if self.start_function:
            await self.trigger_callback()

    async def stop(self, *args):
        os.system('clear')
        print(f"{self._bot.first_name} - @{self._bot.username} Stoped")
        await super().stop()

class pyroClient:
    def __init__(
            self,
            bot: Bot,
            handlers:Handlers = {}
    ):
        """
        Initialize a pyroClient instance.

        Args:
            bot (Bot): The bot class.
            handlers (HANDLERS, optional): Handlers for the bot. Defaults to {}.
        """
        print('Starting...')
        self.app = client(bot = bot ,start_function = handlers.start_function)
        
        if handlers == {} or handlers ==  None:
            raise NoHandler
        
        messages:MessagesHandlers = handlers.messages
        commands = handlers.commands
        callback = handlers.callback
        inline = handlers.inline
        join_request = handlers.join_request
        greeting = handlers.greeting
        self.start_function = handlers.start_function
        self.command_list = []

        if commands:
            commands_dir = commands
            commands = get_commands_data(commands_dir)
            
            for command , cmd_func in commands:
                self.app.add_handler(MessageHandler(cmd_func ,filters.command(command)))
                self.command_list.append(command)
                
        if messages:
            if messages.text:self.app.add_handler(MessageHandler(filters.text & ~filters.command(self.command_list),messages.text))
            if messages.poll:self.app.add_handler(MessageHandler(filters.poll,messages.poll))
            if messages.reply:self.app.add_handler(MessageHandler(filters.reply,messages.reply))
            if messages.audio:self.app.add_handler(MessageHandler(filters.audio,messages.audio))
            if messages.video:self.app.add_handler(MessageHandler(filters.video,messages.video))
            if messages.voice:self.app.add_handler(MessageHandler(filters.voice,messages.voice ))
            if messages.caption:self.app.add_handler(MessageHandler(filters.caption,messages.caption))
            if messages.contact:self.app.add_handler(MessageHandler(filters.contact,messages.contact))
            if messages.location:self.app.add_handler(MessageHandler(filters.location,messages.location))
            if messages.sticker:self.app.add_handler(MessageHandler(filters.sticker,messages.sticker))
            if messages.document:self.app.add_handler(MessageHandler(filters.document,messages.document))
            if messages.new_chat_photo:self.app.add_handler(MessageHandler(filters.new_chat_photo,messages.new_chat_photo))
            if messages.new_chat_title:self.app.add_handler(MessageHandler(filters.new_chat_title,messages.new_chat_title))
            if messages.new_chat_member:self.app.add_handler(MessageHandler(filters.new_chat_members,messages.new_chat_member))
            if messages.left_chat_memeber:self.app.add_handler(MessageHandler(filters.left_chat_member,messages.left_chat_memeber))
            if messages.pinned_message:self.app.add_handler(MessageHandler(filters.pinned_message,messages.pinned_message))
            if messages.all_status:self.app.add_handler(MessageHandler(filters.all,messages.all_status))

        if callback:
            self.app.add_handler(CallbackQueryHandler(callback))

        if inline:
            self.app.add_handler(InlineQueryHandler(inline))

        if join_request:
            self.app.add_handler(ChatJoinRequestHandler(join_request))

        
        if greeting:
            self.app.add_handler(ChatMemberUpdatedHandler(greeting))
    


        
    def stop(self):
        """
        Stop the bot. This method will stop the bot.
        """
        self.app.stop()



    def start(self):
        """
        Start the bot. This method will start the bot in either webhook or polling mode,
        depending on whether a webhook_url is provided.

        Args:
            drop_pending_updates (bool, optional): Whether to drop pending updates. Defaults to None.

        """
        try:
            self.app.run()
        except Exception as e:
            print(e)
            raise


