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
                
                if quiz.status != Quiz.QuizStatus.WAITING_START:

                    order = Order.objects.get_or_create(
                        status=Order.OrderStatus.active, 
                        user=self.request.user
                    )[0]
                    result = OrderDetail.objects.get_or_create(
                        quiz=quiz,
                        order=order
                    )
                    if result[1]: messages.success(self.request, 'ازمون با موفقیت به سبد خرید شما اضافه شد')
                    else: messages.warning(self.request, 'این ازمون از قبل در سبد خرید شما موجود میباشد')
                else:
                    messages.warning(self.request, 'این ازمون شروع شده است و برای شرکت در ان لطفا با ادمین یا نماینده خود در ارتباط باشید')

            else:
                messages.info(self.request, 'ازمون رایگان می باشد')
                
        
            return reverse('quiz:detail', kwargs={'pk':quiz_id}) 
    
        except Exception as E:
            print(self.__class__.__name__, E)
            messages.error(
                self.request, 'مشکلی پیش امده لطفا دوباره تلاش فرمایید'
            )
            return reverse('quiz:list') 


