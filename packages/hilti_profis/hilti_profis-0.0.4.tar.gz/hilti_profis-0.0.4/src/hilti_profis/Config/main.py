class MasterModule:
    def __init__(self, basefile: dict, headerpath: list[str], submodules_list: list=[]) -> None:
        self.basefile = basefile
        self.headerpath = headerpath
        self.submodules_list = submodules_list
        
        #This is dict to be modified and applied
        self.data = self.__get_sub_dict(path_to_key=headerpath, basefile=basefile)
        self.__submodules_init(submodules_list=submodules_list)
        
    def __str__(self) -> str:
        return f'Instance of {self.__class__.__name__} module.'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def modified_data(self) -> dict:
        """Returns the full basefile dict with the `data` applied."""
        self.apply()
        return self.__update_subdict(
            base_dict=self.basefile,
            path_to_key=self.headerpath,
            value_to_key=self.data
        )
    
    def __submodules_init(self, submodules_list: list):
        for module in submodules_list:
            setattr(self, module.__class__.__name__, module)
    
    @property
    def submodules(self) -> list:
        return [getattr(self, module.__class__.__name__) for module in self.submodules_list]
    
    def __get_sub_dict(self, path_to_key: list[str], basefile: dict) -> dict:
        """Returns the value from a sub-dictionary given the `path_to_key`"""
        _data = basefile.copy()
        try: 
            for k in path_to_key:
                _data = _data[k]
        except Exception:
            print(f'expected {k=} available {_data.keys()}')
            raise Exception
        return _data
    
    def __overwrite_dict(self, base_dict: dict, override_dict: dict) -> dict:
        """Applies dict values from `override_dict` to `base_dict`"""
        override_dict = override_dict.copy()
        for kb, vb in base_dict.items():
            ko = kb
            vo = override_dict.get(ko)
            if vo is None:
                vo = vb
            if isinstance(vb, dict):
                kb = self.__overwrite_dict(vb, vo)
            else:
                override_dict[ko] = vo
        return override_dict
    
    def apply(self) -> dict:
        """Applies the changes to the basefile"""
        self.__submodules_apply()
        return self.data
        
    def __submodules_apply(self):
        """Applys the changes from submodules before applying base change."""
        for module in self.submodules:
            module.apply()
            self.data = self.__update_subdict(
                base_dict=self.data,
                path_to_key=module.headerpath[-1:],
                value_to_key=module.data
            )
            
    def __update_subdict(self, base_dict: dict, path_to_key: list[str], value_to_key:dict|str|None) -> dict:
        current_dict = base_dict.copy()
        for key in path_to_key[:-1]:
            current_dict = current_dict[key]
        if path_to_key != []:
            current_dict[path_to_key[-1]] = value_to_key
        return current_dict
    
    def __getitem__(self, idx: str) -> str|dict|None:
        if isinstance(idx, str):
            return self.data[idx]
        raise Exception(f'Not Implemented. `_MasterConfig.__getitem__` not implemented for `idx` {type(idx)=}')
    
    def __setitem__(self, idx: str, key) -> None:
        self.data[idx] = key
        
    @property
    def keys(self):
        return self.data.keys()