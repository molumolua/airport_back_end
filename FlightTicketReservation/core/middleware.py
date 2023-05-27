from datetime import date

class RecoverCreditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.last_recover_date is None or request.user.last_recover_date < date.today():
                request.user.credit_score += 10
                request.user.last_recover_date = date.today()
                request.user.save()

        response = self.get_response(request)

        return response
