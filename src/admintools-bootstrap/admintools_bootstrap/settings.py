from appconf import AppConf


class AdminToolsBootstrapConf(AppConf):
    SITE_LINK = '/'

    class Meta:
        prefix = 'ADMINTOOLS_BOOTSTRAP'
