from admin_controller import home_controller
from flask import Flask
from flask_cors import CORS

webservice = Flask("MediaLibraryWebService", template_folder="templates")
cors = CORS(webservice, resources={r"/api/*": {"origins": "*"}})
"""
---- ROUTES ----
"""

webservice.add_url_rule("/", view_func=home_controller.index)
webservice.add_url_rule("/musics", view_func=home_controller.show_all_musics)
webservice.add_url_rule("/api/musics", view_func=home_controller.get_all_musics)

webservice.add_url_rule("/music-edit/<id>", view_func=home_controller.edit_music_view, methods=['GET'])
webservice.add_url_rule("/music-edit/<id>", view_func=home_controller.edit_music, methods=['POST'])

"""
---- ENd ROUTES ----
"""
