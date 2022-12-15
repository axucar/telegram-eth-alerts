# Telegram Bot to Track ETH/ERC20 transfers

## How to use:
1. Run `install.sh` to setup Python virtual environment with necessary packages, then `source .venv/bin/activate`
2. Edit `.env` file similar to `.env_example`. Get your user's "Chat ID" from Telegram for `TELEGRAM_USER_ID`, and `TELEGRAM_API_KEY` corresponding to your bot API token
3. Set wallets and ERC20 tokens you want to track in `config.py`, set `BROWNIE_NETWORK` (defined in `~/.brownie/network_config.yaml`), and USD transfer threshold to monitor
4. Run `python bot.py`, and send `/start` command in Telegram (`/stop` to stop messages)



