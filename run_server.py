__author__ = 'Madison'

from app import app

app.run(debug=True,
        # host='0.0.0.0',
        port=5050)  # do you trust everyone on the local network?

