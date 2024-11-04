from rest_api.request.Request import Request

from npdep_common.interface.Interface import Interface

from npdep_sourcing.base.Sourcing import Sourcing

class RestModule(Sourcing):
    def __init__(self, options, registration):
        super().__init__("RestModule", options, registration)

    def init(self):
       pass

    def get(self):
        url = self.options["url"]
        req = Request()
        data = req.get(url)
        return Interface.process(data=data)
    
    def end(self):
        pass