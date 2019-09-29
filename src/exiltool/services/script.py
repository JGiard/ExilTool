from flask import render_template, request

from exiltool.backend.decorators import route
from exiltool.model.user import User


class ScriptService:
    @route('/exiltool.user.js')
    def get_user_script(self, user: User):
        name = 'ExilTool-local' if 'localhost' in request.host_url else 'ExilTool'
        return render_template('exiltool.user.js', name=name, site=request.host_url, apikey=user.apikey)
