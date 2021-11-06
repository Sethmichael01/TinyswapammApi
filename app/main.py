from flask import Flask, jsonify
from tinyman.v1.client import TinymanTestnetClient

client = TinymanTestnetClient()

# Fetch our two assets of interest
TINYUSDC = client.fetch_asset(21582668)
ALGO = client.fetch_asset(0)
Planet = client.fetch_asset(408947)
YLDY = client.fetch_asset(22847688)

# Fetch the pool we will work with
ALGOTINYUSDCpool = client.fetch_pool(TINYUSDC, ALGO)
ALGOPlanetpool = client.fetch_pool(Planet, ALGO)
YLDYpool = client.fetch_pool(YLDY, ALGO)

# Get a quote for a swap of 1 ALGO to TINYUSDC with 1% slippage tolerance
ALGOTINYUSDCquote = ALGOTINYUSDCpool.fetch_fixed_input_swap_quote(
    ALGO(1_000_000), slippage=0.01)

ALGOPlanetquote = ALGOPlanetpool.fetch_fixed_input_swap_quote(
    ALGO(1_000_000), slippage=0.01)

ALGOYLDYquote = YLDYpool.fetch_fixed_input_swap_quote(
    ALGO(1_000_000), slippage=0.01)


print(ALGOTINYUSDCquote)
print(f'TINYUSDC per ALGO: {ALGOTINYUSDCquote.price}')
print(
    f'TINYUSDC per ALGO (worst case): {ALGOTINYUSDCquote.price_with_slippage}')

app = Flask(__name__)

swapassets = [
    {
        'assettoswap': "ALGOTINYUSDC",
        'TINYUSDC per ALGO': ALGOTINYUSDCquote.price,
        'assetswap_id': "1"
    },
    {
        'assettoswap': "ALGOPlanet",
        'Planet per ALGO': ALGOPlanetquote.price,
        'assetswap_id': "2"
    },
    {
        'assettoswap': "ALGOYLDY",
        'YLDY per ALGO': ALGOYLDYquote.price,
        'assetswap_id': "3"
    }
]


@app.route('/')
def index():
    return "Hello World"


@app.route('/swapassets', methods=['GET'])
def get():
    return jsonify({'Swapassets': swapassets})
    
@app.route("/swapassets/<int:assetswap_id>", methods=['GET'])
def get_course(assetswap_id):
    return jsonify({'assetpair': swapassets[assetswap_id]})


if __name__ == "__main__":
    app.run(debug=True)
