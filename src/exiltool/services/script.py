from flask import render_template, request

from exiltool.backend.decorators import route, noauth
from exiltool.model.user import User

SCRIPT_VERSION = '0.2.4'


class ScriptService:
    @route('/exiltool.user.js')
    def get_user_script(self, user: User):
        name = 'ExilTool-local' if 'localhost' in request.host_url else 'ExilTool'
        return render_template('exiltool.user.js', name=name, version=SCRIPT_VERSION,
                               site=request.host_url, apikey=user.apikey)

    @noauth
    @route('/api/script/version')
    def script_version(self):
        return SCRIPT_VERSION
