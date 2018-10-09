import inspect

from django.conf import settings
from django.core.management import call_command
from django.contrib.sites.models import Site
from django.test import TestCase as DjangoTestCase
from django.test.runner import DiscoverRunner

from speedy.core.settings.utils import env


class SiteDiscoverRunner(DiscoverRunner):
    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        if not test_labels:
            test_labels = [label for label in settings.INSTALLED_APPS if label.startswith('speedy.')]
        return super().build_suite(test_labels=test_labels, extra_tests=extra_tests, **kwargs)


class SpeedyCoreDiscoverRunner(SiteDiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        # We don't run tests on speedy.core
        pass


def conditional_test(test_func):
    def wrapper(method_or_class):
        if inspect.isclass(method_or_class):
            # Decorate class
            if test_func():
                return method_or_class
            else:
                return
        else:
            # Decorate method
            def inner(*args, **kwargs):
                if test_func():
                    return method_or_class(*args, **kwargs)
                else:
                    return

            return inner

    return wrapper


class TestCase(DjangoTestCase):
    client_host = 'en.localhost'
    _incorrect_username_and_password_errors_dict = {'__all__': ['Please enter a correct username and password. Note that both fields may be case-sensitive.']}
    _password_too_short_errors_dict = {'new_password1': ['Password too short.']}
    _password_too_long_errors_dict = {'new_password1': ['Password too long.']}
    _your_old_password_was_entered_incorrectly_errors_dict = {'old_password': ['Your old password was entered incorrectly. Please enter it again.']}
    _the_two_password_fields_didnt_match_errors_dict = {'new_password2': ["The two password fields didn't match."]}
    _this_email_is_already_in_use_errors_dict = {'email': ['This email is already in use.']}
    _this_username_is_already_taken_errors_dict = {'slug': ['This username is already taken.']}
    # ~~~~ TODO: {'username': ['This username is already taken.'], 'slug': ['This username is already taken.']}

    def setUp(self):
        super().setUp()
        self.set_up()

    def set_up(self):
        pass

    def _pre_setup(self):
        super()._pre_setup()
        call_command('loaddata', settings.FIXTURE_DIRS[-1] + '/default_sites_local.json', verbosity=0)
        self.site = Site.objects.get_current()
        self.site.domain = 'localhost'
        self.site.save()
        self.SPEEDY_NET_SITE_ID = settings.SITE_PROFILES.get('net').get('site_id')
        self.SPEEDY_MATCH_SITE_ID = settings.SITE_PROFILES.get('match').get('site_id')
        self.client = self.client_class(HTTP_HOST=self.client_host)


exclude_on_site = lambda site_id: conditional_test(lambda: int(settings.SITE_ID) != int(site_id))
exclude_on_speedy_net = exclude_on_site(env('SPEEDY_NET_SITE_ID'))
exclude_on_speedy_match = exclude_on_site(env('SPEEDY_MATCH_SITE_ID'))
exclude_on_speedy_composer = exclude_on_site(env('SPEEDY_COMPOSER_SITE_ID'))
exclude_on_speedy_mail_software = exclude_on_site(env('SPEEDY_MAIL_SOFTWARE_SITE_ID'))

only_on_site = lambda site_id: conditional_test(lambda: int(settings.SITE_ID) == int(site_id))
only_on_speedy_net = only_on_site(env('SPEEDY_NET_SITE_ID'))
only_on_speedy_match = only_on_site(env('SPEEDY_MATCH_SITE_ID'))
only_on_speedy_composer = only_on_site(env('SPEEDY_COMPOSER_SITE_ID'))
only_on_speedy_mail_software = only_on_site(env('SPEEDY_MAIL_SOFTWARE_SITE_ID'))


