from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import __version__ as TG_VER

import logging
import dotenv
dotenv.load_dotenv()
from functools import wraps
import asyncio
import nest_asyncio
nest_asyncio.apply()

import brownie
from token_wrapper import Token
from trackers import track_eth_transfers, track_erc20_transfers
import config as cfg

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
    
# Decorator for checking user ID matches chat ID
def auth(user_id):
    def outer_wrapper(func):
        @wraps(func)
        async def wrapper(update, context):
            if update.effective_user.id == user_id:
                await func(update, context)
            else:
                await update.message.reply_text("This Chat ID is not authorized. User ID needs to match your Chat ID.")
        return wrapper
    return outer_wrapper

# Define a few command handlers. These usually take the two arguments update and context.
@auth(cfg.USER_ID)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    cfg.SILENCE = False
    await cfg.application.bot.send_message(chat_id=cfg.USER_ID,text="Started event monitor.")
    

@auth(cfg.USER_ID)
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:    
    cfg.SILENCE = True
    await cfg.application.bot.send_message(chat_id=cfg.USER_ID,text="Stopped event monitor.")

def init_bot() -> None:
    """Start the bot."""
    # on different commands - answer in Telegram
    cfg.application.add_handler(CommandHandler("start", start))
    cfg.application.add_handler(CommandHandler("stop", stop))

    # Run the bot until the user presses Ctrl-C
    cfg.application.run_polling()


async def main():
    brownie.network.connect(cfg.BROWNIE_NETWORK)

    ##convert to checksummed format
    for key,val in cfg.WALLETS_TRACKED.items():
        cfg.WALLETS_TRACKED[brownie.convert.to_address(key)] = val
    for key,val in cfg.ERC20_TOKENS.items():
        cfg.ERC20_TOKENS[brownie.convert.to_address(key)] = brownie.convert.to_address(val)

    ##get ERC20 tokens to use oracle pricing
    for key,val in cfg.ERC20_TOKENS.items():
        cfg.token_dict[key] = Token(address=key,oracle_address=val)
    weth_address = brownie.convert.to_address('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
    weth_oracle = brownie.convert.to_address('0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419')
    if weth_address in cfg.ERC20_TOKENS:
        cfg.weth = cfg.token_dict[weth_address]
    else: cfg.weth = Token(address=weth_address,oracle_address=weth_oracle)
    
    # Create the Application and pass it your bot's token.    
    cfg.application = Application.builder().token(cfg.BOT_TOKEN).build()
        
    await asyncio.gather(
        asyncio.create_task(track_eth_transfers(cfg.USD_THRESHOLD)),
        asyncio.create_task(track_erc20_transfers(cfg.USD_THRESHOLD)), 
        asyncio.create_task(init_bot())
    )

if __name__ == "__main__":    
    asyncio.run(main())
    