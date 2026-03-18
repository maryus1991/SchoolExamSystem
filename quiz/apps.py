from django.apps import AppConfig


class QuizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz'
    verbose_name = 'ازمون ها'

    def ready(self, *args, **kwargs):
        import quiz.signals
        return super().ready(*args, **kwargs)