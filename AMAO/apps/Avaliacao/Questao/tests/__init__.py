from django.conf import settings
if not settings.TEST_RUNNER.count('Nose'):
    # Needed so the stock test runner can find these tests.
    # But it tricks Nose into running the tests twice.
    from test_models import *
    from test_views import *
