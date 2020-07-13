from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, TemplateView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from pyfb_company.models import Customer
from pyfb_did.models import Did, RoutesDid
from pyfb_endpoint.models import CustomerEndpoint
from pyfb_rating.models import CustomerRcAllocation
from pyfb_routing.models import CustomerRoutingGroup
from pyfb_reporting.models import CDR

User = get_user_model()


class HomePageView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        # try:
        #     usercompany = Person.objects.get(user=self.request.user)
        #     try:
        #         context['company'] = Company.objects.get(name=usercompany.company)
        #         if context['company'].low_credit_alert > context['company'].customer_balance:
        #             messages.warning(self.request,
        #                              _(u'ALERT : Low balance (credit alert level : %s)') % context['company'].low_credit_alert)
        #         if context['company'].account_blocked_alert_sent:
        #             messages.error(self.request,
        #                            _(u'ALERT : Account blocked - no remaining credit - Please make an urgent payment'))
        #         context['ratecards'] = CustomerRateCards.objects.filter(
        #             company=context['company'].pk)\
        #             .filter(ratecard__enabled=True)\
        #             .order_by('priority')
        #     except Company.DoesNotExist:
        #         pass
        # except Person.DoesNotExist:
        # messages.error(
        #     self.request,
        #     _(u"""This user is not linked to a customer !""")
        # )

        try:
            context['customers'] = Customer.objects.filter(customer_enabled=True)[:10]
        except:
            pass

        # integrer panneau contact et stats
        # integrer facture
        # integrer prestation
        return context


class CustomerView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/customer_list.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)

        try:
            context['customers'] = Customer.objects.filter(customer_enabled=True)[:10]
        except:
            pass

        return context


class CustomerDetailView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/customer.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)

        context['customer'] = get_object_or_404(Customer, id=kwargs['pk'])
        try:
            context['endpoints'] = CustomerEndpoint.objects.filter(customer=kwargs['pk'])
        except:
            pass

        try:
            context['dids'] = Did.objects.filter(customer=kwargs['pk'])
        except:
            pass

        try:
            context['ratecards'] = CustomerRcAllocation.objects.filter(customer=kwargs['pk'])
        except:
            pass

        try:
            context['rules'] = CustomerRoutingGroup.objects.filter(customer=kwargs['pk'])
        except:
            pass

        return context


class CustomerEndpointDetailView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/customerendpoint.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerEndpointDetailView, self).get_context_data(**kwargs)

        context['endpoint'] = get_object_or_404(CustomerEndpoint, id=kwargs['pk'])

        try:
            context['dids'] = RoutesDid.objects.select_related('contract_did').filter(trunk=kwargs['pk'])
        except:
            pass

        return context


class CDRView(LoginRequiredMixin, TemplateView):

    template_name = 'pages/cdr.html'

    def get_context_data(self, **kwargs):
        context = super(CDRView, self).get_context_data(**kwargs)

        try:
            context['cdrs'] = CDR.objects.all()
        except:
            pass

        return context
