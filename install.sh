rm -rf ./.venv/
python3 -m venv .venv
source ./.venv/bin/activate
pip install --quiet python-dotenv==0.21.0
pip install --quiet nest-asyncio==1.5.6
pip install --quiet python-telegram-bot==20.0a6
pip install --quiet eth-brownie
pip install --quiet --upgrade websockets

