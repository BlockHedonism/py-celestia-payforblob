from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import DEFAULT_NODE_URL, DEFAULT_GAS_LIMIT, DEFAULT_FEE
import datetime
import requests
import logging
import os

app = Flask(__name__)

logger = logging.basicConfig(
    filename='celestia_payforblob.log',
    level=logging.DEBUG
)

@app.route('/node_status', methods=['GET'])
def node_status():
    """ Get status node
    """
    try:
        node = requests.get(DEFAULT_NODE_URL + f'/balance')
        node_data = node.json()

        if not node_data['amount']:
            raise Exception('Not data')

        return jsonify(node_data)

    except Exception as e:
        logging.error(e)
        return jsonify({'error': 500, 'message': str(e)}), 500

@app.route('/height', methods=['POST'])
def height():
    """ Get namespace_shares and height in blockchain
    """
    try:
        data = request.get_json(force=True)

        if (
            not data['height'] or
            not data['namespace']
        ):
           raise Exception('Insufficient data')

        namespace_id = data['namespace']
        height = data['height']

        tx_height = requests.get(
            DEFAULT_NODE_URL + f'/namespaced_shares/{namespace_id}/height/{int(height)}'
        )
        tx_height_data = tx_height.json()

        if not tx_height_data['height']:
            raise Exception('Context deadline exceeded')

        return jsonify(tx_height_data), 200

    except Exception as e:
        logging.error(e)
        return jsonify({'error': 500, 'message': str(e)}), 500

@app.route('/submit_pfb', methods=['POST'])
def submit_pfb():
    """ Create PayForBlob transaction
    """
    try:
        data = request.get_json(force=True)
        node_url = DEFAULT_NODE_URL

        if (
            not data['tx_data'] or
            not data['tx_node_url'] or
            not data['tx_gas_limit'] or
            not data['tx_fee']
        ):
           raise Exception('Insufficient data')

        if node_url != data['tx_node_url']:
            node_url = data['tx_node_url']

        random_bytes = os.urandom(8)
        namespace_id = random_bytes.hex()
        tx_data = data['tx_data'].encode('utf-8').hex()

        tx_submit = requests.post(
            node_url + '/submit_pfb',
            json={'namespace_id': namespace_id, 'data': tx_data, 'gas_limit': int(data['tx_gas_limit']), "fee": int(data['tx_fee'])}
        )
        tx_submit_data = tx_submit.json()

        if not tx_submit_data['txhash']:
            raise Exception('Transaction decline')

        txhash = tx_submit_data['txhash']
        height = tx_submit_data['height']
        gas_wanted = tx_submit_data['gas_wanted']
        gas_used = tx_submit_data['gas_used']

        return jsonify({
                'txhash': txhash,
                'namespace_id': namespace_id,
                "data_hex": tx_data,
                "data": data['tx_data'],
                'gas_wanted': gas_wanted,
                'gas_used': gas_used,
                'height': height,
                'code': tx_submit_data['code'],
                'date': datetime.datetime.now()
               })

    except Exception as e:
        logging.error(e)
        return jsonify({'error': 500, 'message': str(e)}), 500


@app.route('/')
def index():
    """ Home page
    """
    return render_template('index.html', gas_limit=DEFAULT_GAS_LIMIT, fee=DEFAULT_FEE, node_url=DEFAULT_NODE_URL)

if __name__ == '__main__':
    app.run(debug=True)
