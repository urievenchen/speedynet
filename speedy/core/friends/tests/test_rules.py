from django.conf import settings as django_settings

if (django_settings.TESTS):
    if (django_settings.LOGIN_ENABLED):
        from friendship.models import Friend

        from speedy.core.base.test.models import SiteTestCase
        from speedy.core.base.test.decorators import only_on_sites_with_login

        from speedy.core.accounts.test.user_factories import ActiveUserFactory

        from speedy.core.blocks.models import Block


        @only_on_sites_with_login
        class RequestRulesTestCase(SiteTestCase):
            def set_up(self):
                super().set_up()
                self.user = ActiveUserFactory()
                self.other_user = ActiveUserFactory()

            def test_user_can_send_request_to_other_user(self):
                self.assertIs(expr1=self.user.has_perm(perm='friends.request', obj=self.other_user), expr2=True)

            def test_user_cannot_send_request_to_other_user_if_blocked(self):
                Block.objects.block(blocker=self.other_user, blocked=self.user)
                self.assertIs(expr1=self.user.has_perm(perm='friends.request', obj=self.other_user), expr2=False)
                self.assertIs(expr1=self.other_user.has_perm(perm='friends.request', obj=self.user), expr2=False)

            def test_user_cannot_send_request_to_themself(self):
                self.assertIs(expr1=self.user.has_perm(perm='friends.request', obj=self.user), expr2=False)

            def test_user_cannot_send_second_request(self):
                Friend.objects.add_friend(from_user=self.user, to_user=self.other_user)
                self.assertIs(expr1=self.user.has_perm(perm='friends.request', obj=self.other_user), expr2=False)


        @only_on_sites_with_login
        class ViewRequestsRulesTestCase(SiteTestCase):
            def set_up(self):
                super().set_up()
                self.user = ActiveUserFactory()
                self.other_user = ActiveUserFactory()

            def test_user_cannot_view_incoming_requests_for_other_user(self):
                self.assertIs(expr1=self.user.has_perm(perm='friends.view_requests', obj=self.other_user), expr2=False)

            def test_user_can_view_incoming_requests(self):
                self.assertIs(expr1=self.user.has_perm(perm='friends.view_requests', obj=self.user), expr2=True)


        @only_on_sites_with_login
        class ViewFriendListRulesTestCaseMixin(object):
            def set_up(self):
                super().set_up()
                self.user = ActiveUserFactory()
                self.other_user = ActiveUserFactory()

            def test_user_can_view_his_own_friend_list(self):
                self.assertIs(expr1=self.user.has_perm(perm='friends.view_friend_list', obj=self.user), expr2=True)

            def test_user_can_view_another_user_friend_list(self):
                raise NotImplementedError()

            def test_user_cannot_view_another_user_friend_list(self):
                raise NotImplementedError()


        @only_on_sites_with_login
        class RemoveRulesTestCase(SiteTestCase):
            def set_up(self):
                super().set_up()
                self.user = ActiveUserFactory()
                self.other_user = ActiveUserFactory()
                Friend.objects.add_friend(from_user=self.user, to_user=self.other_user).accept()

            def test_user_can_remove_other_user(self):
                self.assertIs(expr1=self.user.has_perm(perm='friends.remove', obj=self.other_user), expr2=True)

            def test_other_user_can_remove_user(self):
                self.assertIs(expr1=self.other_user.has_perm(perm='friends.remove', obj=self.user), expr2=True)

            def test_user_cannot_remove_themself(self):
                self.assertIs(expr1=self.user.has_perm(perm='friends.remove', obj=self.user), expr2=False)

            def test_user_cannot_remove_other_user_if_not_friends(self):
                Friend.objects.remove_friend(from_user=self.user, to_user=self.other_user)
                self.assertIs(expr1=self.user.has_perm(perm='friends.remove', obj=self.other_user), expr2=False)


