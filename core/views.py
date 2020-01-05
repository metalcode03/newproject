from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from .models import Item, OrderItem, Order

from django.utils import timezone
# Create your views here.
# def home_page(request):
#     context = {
#         'items':Item.objects.all()
#     }
#     # return render(request, 'item_list.htm', context)
#     return render(request, "home-page.htm", context)
class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home-page.htm'

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'order_summary.htm', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'you do not have an active order')
            return redirect("/")


def checkout_page(request):
    return render(request, "checkout-page.htm")

# def product_page(request):
#     context = {
#         'items':Item.objects.all()
#      }
#     return render(request, 'product.htm', context)

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.htm"
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        items=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item  is in thee order
        if order.items.filter(items__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'this item quantity was updated')
        else:
            messages.info(request, 'this item was added to your Cart')
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'this item was added to your Cart')
    return redirect("core:product", slug=slug)
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(items__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                items=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, 'this item was removed from your Cart')
        else:
            messages.info(request, 'this item was not in your Cart')
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, 'you donot have and order')
        #add a message saying user doesnt have  an order
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)
