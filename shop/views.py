from django.shortcuts import get_object_or_404, redirect, render , reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from . models import Item , OrderItem , Order
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

# Create your views here.

class HomeView(ListView):
    model = Item
    paginate_by= 4
    template_name = 'shop/home.html'




def check_out_item(request):
    return render(request, 'shop/checkout.html')



class Product_detail_view(DetailView):
    model = Item
    template_name = 'shop/product.html'



# cart

class OrderSummary(LoginRequiredMixin,View):
    def get(self , *args , **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return render(self.request, 'shop/order_summary.html',{'object':order})

        except ObjectDoesNotExist:
            messages.error(self.request,"No recent orders")
            return redirect("/")
        

@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_item , created = OrderItem.objects.get_or_create(item=item , user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "added another item to cart")
            return redirect(reverse("shop:order_summary"))
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect(reverse("shop:order_summary"))


    else:
        ordered_date=timezone.now()
        order = Order.objects.create(user=request.user , ordered_date=ordered_date)
        order.items.add(order_item)
        return redirect(reverse("shop:order_summary", kwargs={'slug':slug}))
    

@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item , user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
            return redirect(reverse("shop:order_summary"))
        else:
            messages.info(request, "This item was not in your cart")
            return redirect(reverse("shop:product_details",  kwargs={'slug':slug}))
            
    else:
        messages.info(request, "No placed order")
        return redirect(reverse("shop:product_details", kwargs={'slug':slug}))


def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item , user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
            else:
                order.items.remove(order_item)
            
            messages.info(request, "This item quantity was updated")
            return redirect(reverse("shop:order_summary"))
        else:
            messages.info(request, "This item was not in your cart")
            return redirect(reverse("shop:product_details",  kwargs={'slug':slug}))
            
    else:
        messages.info(request, "No placed order")
        return redirect(reverse("shop:product_details", kwargs={'slug':slug}))
    
