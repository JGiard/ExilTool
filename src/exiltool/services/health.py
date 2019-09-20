from exiltool.backend.decorators import route, noauth


class HealthService:
    @noauth
    @route('/health')
    def health(self):
        return '', 200
