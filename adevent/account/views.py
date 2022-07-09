from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from django.conf import settings
from .forms import UserCreationForm
from django.contrib import messages
from django.views import View

User = get_user_model()


class SignUpView(CreateView):

    template_name = 'account/registration/signup.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # メールにURLを添付して送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('mail/account/create/subject.txt', context)
        message = render_to_string('mail/account/create/body.txt', context)

        user.email_user(subject, message)
        submit_url = reverse_lazy('account:signup_submit')
        return HttpResponseRedirect(submit_url)

sign_up = SignUpView.as_view()

class SignUpSubmitView(TemplateView):

    template_name = 'account/registration/signup_submit.html'

signup_submit = SignUpSubmitView.as_view()

class SignUpCompleteView(View):
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # 期限は24時間以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_id = loads(token, max_age=self.timeout_seconds)

        # 期限切れの場合
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている場合
        except BadSignature:
            return HttpResponseBadRequest()

        else:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    messages.success(request, 'アカウントの作成が完了しました。登録した情報でログインを行なってください。')
                    login_url = reverse_lazy('account:login')
                    return HttpResponseRedirect(login_url)

        return HttpResponseBadRequest()

sign_up_complete = SignUpCompleteView.as_view()
