from django.db import models
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.




CATEGORY_CHOICES= (
    ('F','Flavours'),
    ('M','Marvel'),
    ('DC','DC'),
    ('TV','TV'),
    ('MOV','Movie'),
)

LABEL_CHOICES =(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)



class Item(models.Model):
    title = models.CharField(max_length=100)
    price=models.FloatField()
    discount_price=models.FloatField(null=True , blank=True)
    description=models.TextField()
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=3)
    label=models.CharField(choices=LABEL_CHOICES,max_length=3)
    slug = models.SlugField()
    


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product_details", kwargs={
            'slug':self.slug

        })


    def get_add_to_cart_url(self):
        return reverse("shop:add_to_cart" , kwargs={'slug':self.slug})


    def get_remove_from_cart_url(self):
        return reverse("shop:remove_from_cart" , kwargs={'slug':self.slug})

    
    


class OrderItem(models.Model):
    ordered=models.BooleanField(default=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


    def get_total_item_price(self):
        return self.quantity * self.item.price


    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price


    def get_amount_saved(self):
        return self.get_total_item_price()- self.get_total_discount_item_price()


    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='buyers')


    def __str__(self):
        return self.user.username


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total