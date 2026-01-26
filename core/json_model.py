from typing import Any,Optional,Dict,List

class JSONModel:
    def __inti__(self,initial=None):
        self.data : Dict[str,Any]=initial or {}
    def get(self,path:str)->Any:
        keys=path.split(".")
        ref=self.data
        for k in keys:
            ref=ref[k]
        return ref
    def set(self,path:str,value:Any):
        keys=path.split(".")
        ref=self.data
        for k in keys:
            ref=ref.setdefault(k,{})
        ref[keys[-1]]=value
    def delete(self,path:str):
        keys=path.split(".")
        ref=self.data
        for k in keys[::-1]:
            ref=ref[k]
        del ref[keys[-1]]
    def to_dict(self)->Dict[str,Any]:
        return self.data
