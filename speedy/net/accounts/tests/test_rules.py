from django.conf import settings as django_settings

if (django_settings.TESTS):
    if (django_settings.LOGIN_ENABLED):
        import unittest

        from speedy.core.base.test.models import SiteTestCase
        from speedy.core.base.test.decorators import only_on_speedy_net

        from speedy.core.accounts.test.user_factories import InactiveUserFactory, ActiveUserFactory

        from speedy.core.accounts.tests.test_rules import ViewProfileRulesTestCaseMixin


        @only_on_speedy_net
        class ViewProfileRulesTestCase(ViewProfileRulesTestCaseMixin, SiteTestCase):
            def test_doron_and_jennifer_have_access(self):
                self.assertIs(expr1=self.doron.has_perm(perm='accounts.view_profile', obj=self.jennifer), expr2=True)
                self.assertIs(expr1=self.jennifer.has_perm(perm='accounts.view_profile', obj=self.doron), expr2=True)

            @unittest.skip(reason="This test is irrelevant in Speedy Net.")
            def test_doron_and_jennifer_have_no_access(self):
                raise NotImplementedError()


        @only_on_speedy_net
        class DeleteAccountRulesTestCase(SiteTestCase):
            def set_up(self):
                super().set_up()
                self.user = ActiveUserFactory()

            def test_inactive_user_can_delete_his_account_1(self):
                self.assertIs(expr1=self.user.has_perm(perm='accounts.delete_account', obj=self.user), expr2=False)
                self.user.speedy_net_profile.deactivate()
                self.assertIs(expr1=self.user.has_perm(perm='accounts.delete_account', obj=self.user), expr2=True)

            def test_inactive_user_can_delete_his_account_2(self):
                user_2 = InactiveUserFactory()
                self.assertIs(expr1=user_2.has_perm(perm='accounts.delete_account', obj=user_2), expr2=True)

            def test_staff_and_superuser_cannot_delete_their_account(self):
                # ~~~~ TODO: Staff and superuser have all permissions, including accounts.delete_account.
                user_2 = ActiveUserFactory(is_superuser=True, is_staff=True)
                self.assertIs(expr1=user_2.has_perm(perm='accounts.delete_account', obj=user_2), expr2=True)  #### ~~~~ TODO: fails on this line
                user_2.speedy_net_profile.deactivate()
                self.assertIs(expr1=user_2.has_perm(perm='accounts.delete_account', obj=user_2), expr2=True)  #### false
                user_2.is_active = False
                user_2.save_user_and_profile()
                self.assertIs(expr1=user_2.has_perm(perm='accounts.delete_account', obj=user_2), expr2=False)
                user_2.is_superuser, user_2.is_staff = False, False
                user_2.save_user_and_profile()
                self.assertIs(expr1=user_2.has_perm(perm='accounts.delete_account', obj=user_2), expr2=True)

            def test_active_user_cannot_delete_his_account(self):
                self.assertIs(expr1=self.user.has_perm(perm='accounts.delete_account', obj=self.user), expr2=False)
                # Deactivate the user's profile on Speedy Match, but not on Speedy Net.
                self.user.speedy_match_profile.deactivate()
                self.assertIs(expr1=self.user.has_perm(perm='accounts.delete_account', obj=self.user), expr2=False)

            def test_user_cannot_delete_other_user_account(self):
                user_2 = ActiveUserFactory()
                self.assertIs(expr1=self.user.has_perm(perm='accounts.delete_account', obj=user_2), expr2=False)
                user_2.speedy_net_profile.deactivate()
                self.assertIs(expr1=self.user.has_perm(perm='accounts.delete_account', obj=user_2), expr2=False)
                self.user.speedy_net_profile.deactivate()
                self.assertIs(expr1=self.user.has_perm(perm='accounts.delete_account', obj=user_2), expr2=False)
                user_2.speedy_net_profile.activate()
                self.assertIs(expr1=self.user.has_perm(perm='accounts.delete_account', obj=user_2), expr2=False)
                self.user.speedy_net_profile.activate()
                self.assertIs(expr1=self.user.has_perm(perm='accounts.delete_account', obj=user_2), expr2=False)

            def test_1(self):
                raise NotImplementedError()

            def test_2(self):
                raise NotImplementedError()


