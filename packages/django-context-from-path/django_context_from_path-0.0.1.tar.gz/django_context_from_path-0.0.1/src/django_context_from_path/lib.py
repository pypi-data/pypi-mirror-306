from typing import Callable, Dict, Any, Optional
from pathlib import Path
from copy import deepcopy
from enum import Enum, unique


@unique
class Node(Enum):
    ROUTES = 1
    VIRTUAL = 2
    MATCH_REST = 3
    MATCH_COMPLETE = 4


class Val:
    def __init__(self, raw: Any, **kwargs):
        self.raw = raw
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __eq__(self, other):
        if not isinstance(other, Val):
            return False
        return all(
            hasattr(other, attr) and getattr(self, attr) == getattr(other, attr)
            for attr in self.__dict__
        )
    
    # so `pytest` don't highlight memory address difference as error
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in vars(self).items())
        return f'{self.__class__.__name__}({attrs})'

def _compile(config: Dict, virtual: bool = False, cur_path: Path = Path()):
    res_routes = {}
    routes = config.pop(Node.ROUTES, {})
    
    # check syntax
    for key, _ in config.items():
        if isinstance(key, Node):
            raise TypeError(
                f"{cur_path} shouldn't contain {key}, which is "
                "of Node type but not Node.ROUTES."
            )

    routes_inside_virtual = {}
    for route_node, route_config in routes.items():
        next_path = cur_path / str(route_node)
        if virtual:
            route_config = config | route_config
            
        if route_node == Node.VIRTUAL:
            routes_inside_virtual.update(_compile(route_config, True, next_path))
        else:
            route_config.update(_compile(route_config, False, next_path))
            res_routes[route_node] = route_config

    res_routes.update(routes_inside_virtual)
    if virtual:
        return res_routes
    else:
        if len(res_routes):
            config[Node.ROUTES] = res_routes

        return config

def compile(configuration: Dict):
    return _compile(deepcopy(configuration), False, Path("<root>"))

@unique
class MatchResult(Enum):
    Equal = 0
    NotEqual = 1
    

def matchRoute(path_seg: str, route: Any):
    if isinstance(route, str):
        return route == path_seg
    elif callable(route):
        return route(path_seg)
    elif isinstance(route, Node):
        if route == Node.MATCH_COMPLETE:
            return False
        else:
            raise ValueError("unreachable")
    else:
        return str(route) == path_seg

def default_process_config_fn(config: Dict, route_config: Optional[Dict], path: Path):
    if not route_config:
        return None

    for field, value in route_config.items():
        if isinstance(field, Node):
            continue
        
        if callable(value):
            value = value(path)
            
        config[field] = value

def genContextDict(
    path: str,
    compiled_config: Dict,
    process_config_fn: Callable[[Dict, Optional[Dict], Path], None] = default_process_config_fn,
) -> Dict[str, Any]:
    config = deepcopy(compiled_config)
    path_segs = path.strip("/").split("/")
    routes = config.pop(Node.ROUTES, {})
    cur_path = Path()
    
    match_complete_config = None
    while path_segs and routes:
        matched = False
        path_seg = path_segs.pop(0)
        cur_path /= path_seg
        
        match_rest_config = routes.pop(Node.MATCH_REST, None)
        for route, route_config in routes.copy().items():
            matched = matchRoute(path_seg, route)
            if matched:
                routes = route_config.pop(Node.ROUTES, {})
                process_config_fn(config, route_config, cur_path)
                break

        if not matched and match_rest_config:
            matched = True
            routes = match_rest_config.pop(Node.ROUTES, {})
            process_config_fn(config, match_rest_config, cur_path)

        # No Match Exist
        if not matched:
            break
                
        # Match Exist
        if not path_segs:
            pass
            
    match_complete_config = routes.get(Node.MATCH_COMPLETE, None)
    process_config_fn(config, match_complete_config, cur_path)

    return config
