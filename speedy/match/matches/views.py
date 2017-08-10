from django.urls import reverse_lazy
from django.views import generic
from rules.contrib.views import LoginRequiredMixin
from speedy.core.accounts.models import User
from speedy.core.base.utils import get_age_ranges_match
from ..accounts.models import SiteProfile
from .forms import MatchSettingsMiniForm, MatchSettingsFullForm, AboutMeForm


class MatchesListView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'matches/match_list.html'
    form_class = MatchSettingsMiniForm
    success_url = reverse_lazy('matches:list')

    def get_matches(self):
        user_profile = self.request.user.profile
        age_ranges = get_age_ranges_match(self.request.user.profile.min_age_match, self.request.user.profile.max_age_match)
        qs = User.objects.active(gender__in=user_profile.gender_to_match, date_of_birth__range=age_ranges).exclude(pk=self.request.user.pk)

        qs = [user for user in qs if (self.request.user.profile.get_matching_rank(other_profile=user.profile) > SiteProfile.RANK_0) and user.profile.is_active]

        qs = sorted(qs, key=lambda user: (user.profile.rank, user.profile.last_visit), reverse=True)
        return qs

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)
        cd.update({
            'matches': self.get_matches(),
        })
        return cd


class EditMatchSettingsView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'matches/settings/matches.html'
    form_class = MatchSettingsFullForm
    success_url = reverse_lazy('matches:list')

    def get_object(self, queryset=None):
        return self.request.user.profile


class EditAboutMeView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'matches/settings/about_me.html'
    form_class = AboutMeForm
    success_url = reverse_lazy('matches:list')

    def get_object(self, queryset=None):
        return self.request.user.profile
