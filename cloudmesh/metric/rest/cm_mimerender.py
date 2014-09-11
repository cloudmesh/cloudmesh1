from mimerender import FlaskMimeRender
from flask import jsonify

render_xml = lambda message: '<message>%s</message>' % str(message)
render_json = lambda **args: jsonify(args)
render_html = lambda message: '<html><body>%s</body></html>' % str(message)
render_txt = lambda message: message

mimerender = FlaskMimeRender()(
    default="json",
    html=render_html,
    xml=render_xml,
    json=render_json,
    txt=render_txt
)
