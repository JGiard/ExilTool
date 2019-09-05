from flask import render_template, request

from exiltool.backend.decorators import route


class ScriptService:
    @route('/exiltool.user.js')
    def get_user_script(self):
        return render_template('exiltool.user.js', site=request.host_url)
