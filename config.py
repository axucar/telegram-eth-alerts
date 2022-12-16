import os

token_dict={}
BOT_TOKEN = os.environ.get('TELEGRAM_API_KEY')
USER_ID = int(os.environ.get('TELEGRAM_USER_ID'))


BROWNIE_NETWORK = "mainnet-localnode-ws" #"mainnet-alchemy-wss"
SILENCE = True #By default, show nothing. Send command /start to turn off SILENCE
USD_THRESHOLD=100

#FORMAT :: address: name_label
WALLETS_TRACKED = {
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045":"VITALIK",
    "0xe692869347b9b18Ef2DEED19ae1bBACE303B52B0":"VITALIK",
    "0xf584F8728B874a6a5c7A8d4d387C9aae9172D621":"JUMP_TRADING",
    "0x9507c04B10486547584C37bCBd931B2a4FeE9A41":"JUMP_TRADING_2",
    "0x4f1a5a5d258522254933a6DA9648c57Fe230D17e":"JUMP_TRADING_3",
    "0x641cE4240508eae5dCaeffE991F80941D683Ad64":"DRAGONFLY_CAPITAL",    
    "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe":"ETHEREUM_FOUNDATION",
    "0x11577a8A5bAF1e25B9a2d89f39670F447d75c3cD":"PARADIGM",
    "0xd24400ae8BfEBb18cA49Be86258a3C749cf46853":"GEMINI",
    "0x5f65f7b609678448494De4C87521CdF6cEf1e932":"GEMINI_CONTRACT",
    "0xDBF5E9c5206d0dB70a90108bf936DA60221dC080":"WINTERMUTE",
    "0x4655b7ad0B5f5BaCB9cF960bbFFcEB3f0e51F363":"PARAFI_CAPITAL",
    "0xE7dBE6aa7Edcc38CB5007B87153d236AD879309B":"PARAFI_CAPITAL2",
    "0x7f507739b6242B048Be9185cf462BE816b8eFf1f":"PARAFI_CAPITAL3",
    "0xCD531Ae9EFCCE479654c4926dec5F6209531Ca7b":"COINBASE_CUSTODY_MAIN",
    "0xE11970f2F3dE9d637Fb786f2d869F8FeA44195AC":"AMBER",
    "0xBb98F2A83d78310342dA3e63278cE7515D52619d":"AMBER_OTC",
    "0x58f5F0684C381fCFC203D77B2BbA468eBb29B098":"BLOCKTOWER_CAPITAL",
}

#FORMAT :: token contract: oracle_contract
ERC20_TOKENS = {
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2":"0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419", ##WETH
    "0x6B175474E89094C44Da98b954EedeAC495271d0F":"0xAed0c38402a5d19df6E4c03F4E2DceD6e29c1ee9", ##DAI
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48":"0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6", ##USDC
    "0xdAC17F958D2ee523a2206206994597C13D831ec7":"0x3E7d1eAB13ad0104d2750B8863b489D65364e32D", ##USDT
    "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984":"0x553303d460ee0afb37edff9be42922d8ff63220e", #UNI
    "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0":"0x7bAC85A8a13A4BcD8abb3eB7d6b4d632c5a57676", #MATIC
    "0x514910771AF9Ca656af840dff83E8264EcF986CA":"0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c", #LINK
    "0x4d224452801ACEd8B2F0aebE155379bb5D594381":"0xD10aBbC76679a20055E167BB80A24ac851b37056", #APE
    "0xc00e94Cb662C3520282E6f5717214004A7f26888":"0xdbd020CAeF83eFd542f4De03e3cF0C28A4428bd5", #COMP
    "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2":"0xec1D1B3b0443256cc3860e24a46F108e699484Aa", #MKR
    "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e":"0xA027702dbb89fbd58938e4324ac03B58d812b0E1", #YFI
    "0xD533a949740bb3306d119CC777fa900bA034cd52":"0xCd627aA160A6fA45Eb793D19Ef54f5062F20f33f", #CRV
    "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F":"0xDC3EA94CD0AC27d9A86C180091e7f78C683d3699", #SNX
    "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2":"0xCc70F09A6CC17553b2E31954cD36E4A2d89501f7", #SUSHI
}


