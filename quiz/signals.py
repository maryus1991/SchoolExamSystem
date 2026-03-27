from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Sum, F, Count
from .models import Quiz, StudentAnswer, Question
from report.models import Report
from utils.avg_teraz import calculate_teraze, calculate_std_dev

@receiver(post_save, sender=Quiz)
def create_report_for_users(sender, instance, created, **kwargs):
    if not created and instance.start_set_report and instance.status == Quiz.QuizStatus.CORRECTED and instance.student.exists():
        try:
   
            students = instance.student.all()
            percent_list = []


            for student in students:
                score_data = StudentAnswer.objects.filter(quiz=instance, student=student).aggregate(
                    total_score=Sum('score'),
                    total_count=Count('score')
                )
                
                for item in instance.questions.all():
                    StudentAnswer.objects.get_or_create(quiz=instance, student=student, question=item)
    
                
                total_score = score_data['total_score'] or 0
                total_count = score_data['total_count'] or 1
                
                percent = (total_score / total_count) if total_count > 0 else 0
                percent_list.append(percent)
                report, _ = Report.objects.get_or_create(
                    user=student,
                    quiz=instance,
                    defaults={
                        'grade': instance.grade,
                        'major': instance.major,
                        'lession': instance.lession,
                        'score': total_score,
                        'percent': percent,
                    }
                )
                
        
                report.grade = instance.grade
                report.major = instance.major
                report.lession = instance.lession
                report.score = total_score
                report.percent = percent
                report.save()

            if percent_list:
                std_dev = calculate_std_dev(percent_list)
                percent_avg = sum(percent_list) / len(percent_list)
            else:
                std_dev = 0
                percent_avg = 0

    
            reports = Report.objects.filter(quiz=instance)
            
            for report in reports:
        
                new_teraze = calculate_teraze(report.percent, std_dev, 5000, percent_avg)
                report.teraze = new_teraze    
                percent = report.percent
                if percent > 75:
                    report.status = Report.ReportStatus.excellent
                elif 75 >= percent > 50:
                    report.status = Report.ReportStatus.good
                elif 50 >= percent > 25:
                    report.status = Report.ReportStatus.average
                else:
                    report.status = Report.ReportStatus.weak

                report.save()

            ranked_report_ids = Report.objects.filter(quiz=instance).order_by('-teraze').values_list('id', flat=True)
    
            reports_to_update = []
            for rank, report_id in enumerate(ranked_report_ids, start=1):

                temp_report = Report(id=report_id, order=rank)
                reports_to_update.append(temp_report)
            
    
            if reports_to_update:
                Report.objects.bulk_update(reports_to_update, ['order'])

            instance.status = Quiz.QuizStatus.RESULTS_PUBLISHED
            instance.start_set_report = False
            instance.save()

        except Exception as E:
            print('create reports quiz signals error : ', E)