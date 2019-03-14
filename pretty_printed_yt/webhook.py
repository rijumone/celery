from flask import Flask, request, abort
from get_from_q_process import *

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        print(request.args)
        load.delay({'raw': request.json, 'id': request.args.get('id')})
        return '', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run(
    	debug=True,
    	host='0.0.0.0',
    	port=5002,
    	)

