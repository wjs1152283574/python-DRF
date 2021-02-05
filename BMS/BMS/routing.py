from channels.routing import ProtocolTypeRouter,URLRouter
from django.conf.urls import url

from apps.addrbook import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        #类似drf 路由规则书写
        url(r'^addrbook/',consumers.AddrBookConsumers)
    ])
})

