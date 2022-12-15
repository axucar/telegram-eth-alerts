rm -rf ./.venv/
python3 -m venv .venv
source ./.venv/bin/activate
pip install --quiet playwright==1.28.0
pip install --quiet python-dotenv==0.21.0
pip install --quiet nest-asyncio==1.5.6
pip install --quiet python-telegram-bot==20.0a6
pip install --quiet eth-brownie
pip install --quiet --upgrade websockets
pip install --quiet sigfig

# pip install pillow~=9.3.0
