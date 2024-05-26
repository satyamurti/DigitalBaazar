import logging

from flask import render_template

from init import app, HOST, PORT, DEBUG


@app.route('/upload-files-success', methods=['POST'])
def upload_file():
    pass


@app.route('/')
def index():
    return "Working"


# @app.route('/pass-recovery', strict_slashes=False)
# def upload_files():
#     pass
#
#
# @app.route('/file-timeout', methods=['GET'], strict_slashes=False)
# def timeout():
#     return render_template('file-timeout.html')
#
#
# @app.route('/results', methods=['GET'], strict_slashes=False)
# def _requests():
#     pass
#
#
# @app.route('/checkout/order-pay', methods=['GET'], strict_slashes=False)
# def payment_request():
#     pass
#
#
# @app.route('/checkout/order-received', methods=['GET'], strict_slashes=False)
# def payment_success():
#     pass


if __name__ == '__main__':
    # Restart the last job upon server restart
    logging.info(f'Application running in debug={DEBUG} mode')
    if DEBUG:
        app.run(debug=DEBUG, host=HOST, port=PORT)
    else:
        # Running using gunicorn-wsgi
        app.run()
