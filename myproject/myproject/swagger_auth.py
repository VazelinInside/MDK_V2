from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

swagger_info = openapi.Info(
    title="Dentistry API",
    default_version="v1",
    description="""
    API для управления стоматологической клиникой.
    
    ## Авторизация
    1. Зарегистрируйтесь через `/register/`
    2. Авторизуйтесь через `/login/` чтобы получить токены
    3. Нажмите кнопку Authorize и введите: `Bearer <ваш_access_token>`
    
    ## Доступы
    - Администраторы: полный доступ ко всем эндпоинтам
    - Врачи: доступ к приемам и диагнозам
    - Пациенты: доступ к своим данным и записям
    """,
    terms_of_service="https://www.example.com/terms/",
    contact=openapi.Contact(email="vi4733425@gmail.com"),
    license=openapi.License(name="Proprietary License"),
)

schema_view = get_schema_view(
    swagger_info,
    public=True,
    permission_classes=[AllowAny],
)