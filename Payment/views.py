from django.shortcuts import render
from django.views import View
from Shopping.models import Order

class Checkout(View):
    def get(self, request):
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            'object': order
        }
        for orderitem in order.items.all():
            print("this!!!!!!!!!!!!!!!")
        return render(request, 'checkout.html', context)