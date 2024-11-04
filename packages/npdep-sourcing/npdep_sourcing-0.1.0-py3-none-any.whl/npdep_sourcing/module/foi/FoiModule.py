from foi.search.Search import Search as FoiSearch

from npdep_common.interface.Interface import Interface

from npdep_sourcing.base.Sourcing import Sourcing

class FoiModule(Sourcing):
    def __init__(self, options, registration):
        super().__init__("FoiModule", options, registration)

    def init(self):
        pass

    def get(self):
        s = FoiSearch(self.options["files"])
        paths = s.getFilePaths(self.options["path"])
        return Interface.process(files=paths)
    
    def end(self):
        pass