from django.utils.translation import get_language
from django.utils.encoding import smart_str


class Menu(object):
    namespace = None
    
    def __init__(self):
        if not self.namespace:
            self.namespace = self.__class__.__name__

    def get_nodes(self, request):
        """
        should return a list of NavigationNode instances
        """ 
        raise NotImplementedError
    
class Modifier(object):
    
    def modify(self, request, nodes, namespace, root_id,  post_cut, breadcrumb):
        pass
    
class NavigationNode(object):
    '''
    A NavigationNode is an abstract representation of where the user can 
    navigate. Roughly put, this is what the menu will "point to" when it's 
    generated.
    '''
    title = None
    url = None
    attr = {}
    namespace = None
    id = None
    parent_id = None
    parent_namespace = None
    parent = None # do not touch
    visible = True
    
    def __init__(self, title, url, id, parent_id=None, parent_namespace=None, attr=None, visible=True):
        self.children = [] # must be initialized to an empty list.
        self.title = title
        self.url = self._remove_current_root(url)
        self.id = id
        self.parent_id = parent_id
        self.parent_namespace = parent_namespace
        self.visible = visible
        if attr:
            self.attr = attr
            
    def __repr__(self):
        return "<Navigation Node: %s>" % smart_str(self.title)
    
    def _remove_current_root(self, url):
        '''If the url starts with current_root, remove current_root'''
        current_root = "/%s/" % get_language()
        if url.startswith(current_root):
            url = url[len(current_root) - 1:] # -1 since we want to keep the '/'
        return url
    
    def get_menu_title(self):
        return self.title
    
    def get_absolute_url(self):
        return self.url
    
    def get_attribute(self, name):
        return self.attr[name]
    
    def get_descendants(self):
        nodes = []
        for node in self.children:
            nodes.append(node)
            nodes += node.get_descendants()
        return nodes
