from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Order, OrderDetail
from quiz.models import Quiz
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.timezone import now

# Create your views here.


class AddToOrder(LoginRequiredMixin, RedirectView):
    """to add quiz to order"""

    def get_redirect_url(self, *args, **kwargs):
        
        try:
            quiz_id = kwargs.get('pk')

            quiz = get_object_or_404(Quiz, pk=quiz_id)

            if quiz.stop_at < now():
                messages.warning(self.request, 'این ازمون به پایان رسیده')
                return reverse('quiz:detail', kwargs={'pk':quiz_id}) 
            
            if quiz.status == Quiz.QuizStatus.WAITING_START:

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

            return reverse('quiz:detail', kwargs={'pk':quiz_id}) 
    
        except Exception as E:
            print(self.__class__.__name__, E)
            messages.error(
                self.request, 'مشکلی پیش امده لطفا دوباره تلاش فرمایید'
            )
            return reverse('quiz:list') 


class StartPayment(LoginRequiredMixin, RedirectView):
    """ for start payment """
    
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk, user=self.request.user)        
        price = order.get_payment_price()
        order.save()
        
        # todo: if price > 0 should redirect to payment if price == 0 should redirect to verify payment

        return reverse('orders:verfiy-payment',  kwargs={'pk':pk})

class VerifyPayment(LoginRequiredMixin, RedirectView):
    """ for start payment """
    
    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        order = get_object_or_404(Order, pk=pk, user=self.request.user)
        order.update_at = now()
        order.status = Order.OrderStatus.paid
        order.save()

        for item in order.details.filter(is_active=True).all():
            quiz: Quiz = item.quiz
            quiz.student.add(
                self.request.user
            ) 
            quiz.save()

        messages.success(self.request, 'از اینکه مارو انتخاب کردید متشکریم امیدواریم که نهایت استفاده را بکنید')

        return reverse('dashboard:order-detail', kwargs={'pk':pk})