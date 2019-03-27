from django.shortcuts import redirect

from main.models import Item, Statistics


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if Item.objects.filter(is_sold=False).count() == 0 and request.path != '/zero-items':
            return redirect('zero-items')
        response = self.get_response(request)
        return response


class StatisticsUpdate:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            item = Statistics.objects.get(url=request.path)
        except Statistics.DoesNotExist:
            new_statistic = Statistics(url=request.path, amount=1)
            new_statistic.save()
            response = self.get_response(request)
            return response
        item.amount += 1
        item.save()
        response = self.get_response(request)
        return response
