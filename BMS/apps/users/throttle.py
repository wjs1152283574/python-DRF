from rest_framework.throttling import SimpleRateThrottle
# from .serializers import LogonLogSerializers

class UserViewsetThrottle(SimpleRateThrottle):
    scope = "test_casso"

    def get_cache_key(self,request,view):
        # print(dir(request))
        # print(dir(request.data))
        mobile = request.query_params.get('mobile') or request.data.get('mobile')

        if not mobile :   # 不做次数限制
            return None
        
        return 'throttle_%(scope)s_%(ident)s'%{"scope":self.scope,"ident":mobile}

