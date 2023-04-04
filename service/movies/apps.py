from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "movies"
    verbose_name = "Cinema together"

    def ready(self):
        import movies.models.user  # noqa: F401
