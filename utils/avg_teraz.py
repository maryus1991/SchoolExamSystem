def calculate_teraze(student_percent, std_dev, target_mean, population_mean):
    """
    محاسبه تراز دانش‌آموز بر اساس فرمول نرمال‌سازی
    
    Args:
        student_percent (float): درصد دانش‌آموز (نمره خام)
        std_dev (float): انحراف معیار گروه
        target_mean (float): میانگین تراز مورد نظر (مثلاً ۵۰۰۰)
        population_mean (float): میانگین درصد گروه
        
    Returns:
        float: تراز محاسبه شده
    """
    
    
    z_score = (student_percent - population_mean) / std_dev
    final_score = target_mean + (z_score * 1000)
    
    return final_score


def calculate_std_dev(scores_list):
    """
    محاسبه انحراف معیار یک لیست از اعداد
    
    Args:
        scores_list (list): لیستی از درصد دانش‌آموزان
        
    Returns:
        float: انحراف معیار محاسبه شده
    """
    
 
    # ۱. محاسبه میانگین
    mean = sum(scores_list) / len(scores_list)
    
    # ۲. محاسبه مجموع مربعات تفاضل هر نمره از میانگین
    sum_squared_diff = 0
    for score in scores_list:
        diff = score - mean
        sum_squared_diff += (diff ** 2)
    
    # ۳. محاسبه واریانس (برای نمونه تقسیم بر n-1 می‌کنیم)
    # اگر می‌خواهید دقیقا مثل فرمول ریاضی مدرسه باشد، می‌توانید (len(scores_list) - 1) را به len(scores_list) تغییر دهید
    variance = sum_squared_diff / ((len(scores_list) - 1) if (len(scores_list) - 1) > 0 else 1)
    
    # ۴. گرفتن ریشه دوم واریانس برای رسیدن به انحراف معیار
    std_dev = variance ** 0.5
    
    return std_dev

 