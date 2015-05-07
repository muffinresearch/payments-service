from django.conf.urls import include, url


urlpatterns = [
    url(r'^ui/',
        include('payments_service.ui.urls', namespace='ui')),
    url(r'^braintree/',
        include('payments_service.braintree.urls', namespace='braintree')),
    url(r'',
        include('payments_service.status.urls', namespace='status')),
]

handler500 = 'payments_service.base.views.error_500'
handler404 = 'payments_service.base.views.error_404'
handler403 = 'payments_service.base.views.error_403'
