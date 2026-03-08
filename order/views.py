from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Order, OrderDetail
from quiz.models import Quiz
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import transaction

# Create your views here.


class AddToOrder(LoginRequiredMixin, RedirectView):
    """to add quiz to order"""

    def get_redirect_url(self, *args, **kwargs):
        
        try:
            quiz_id = kwargs.get('pk')

            quiz = get_object_or_404(Quiz, pk=quiz_id)

            if quit.price > 0:

                order = Order.objects.get_or_create(
                    status=Order.OrderStatus.active, 
                    user=self.request.user
                )[0]
                OrderDetail.objects.create(
                    quiz=quiz,
                    order=order
                )

                messages.success(self.request, 'ازمون با موفقیت به سبد خرید شما اضافه شد')
            else:
                messages.info(self.request, 'ازمون رایگان می باشد')
                
        
            return reverse('quiz:detail', kwargs={'pk':quiz_id}) 
    
        except Exception as E:
            print(self.__class__.__name__, E)
            messages.error(
                self.request, 'مشکلی پیش امده لطفا دوباره تلاش فرمایید'
            )
            return reverse('quiz:list') 


