import pytest
import django
from django.conf import settings

if __name__ == '__main__':
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'tests'
        ]
    )
    django.setup()
    pytest.main()
