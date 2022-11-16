from flask import url_for


class Paginator:
    """
    Clase paginador de registros

    ...

    Atributos
    ----------
    query : <class 'flask_sqlalchemy.BaseQuery'>
        la query de todos los registros
    page : int
        la pagina requerida del paginador
    items_per_page : int
        la cantidad de items por pagina a devolver
    endpoint : str
        endpoint para armar la url de las paginas

    Methods
    -------
    next_url
        retorna la pagina siguiente del paginador con el endpoint y los valores dados
    prev_url
        retorna la pagina anterior del paginador con el endpoint y los valores dados
    items
        retorna un lista con las disciplinas a mostrar

    """

    def __init__(self, query, page, items_per_page, endpoint, member_id=None, filter="", search=""):
        self._query = query.paginate(page, items_per_page, False)
        self._endpoint = endpoint
        self._page = page
        self._items_per_page = items_per_page
        self._member_id = member_id
        self._filter = filter
        self._search = search


    def _next_page(self):
        if not self._query.has_next:
            return None
        return self._query.next_num

    def _prev_page(self):
        if not self._query.has_prev:
            return None
        return self._query.prev_num

    @property
    def page(self):
        return self._page

    @property
    def next_url(self):
        if not self._next_page():
            return None
        
        if self.member_id:
            return url_for(
                self._endpoint,
                member_id=self.member_id,
                page=self._next_page(),
                filter=self._filter,
                search=self._search,
                )
        return url_for(
            self._endpoint,
            page=self._next_page(),
            filter=self._filter,
            search=self._search,
        )

    @property
    def pages(self):
        if not list(self._query.iter_pages()):
            return None
        return self._query.iter_pages()

    @property
    def prev_url(self):
        if not self._prev_page():
            return None

        if self.member_id:
            return url_for(
                self._endpoint,
                member_id=self.member_id,
                page=self._prev_page(),
                filter=self._filter,
                search=self._search,
                )
        return url_for(
            self._endpoint,
            page=self._prev_page(),
            filter=self._filter,
            search=self._search,
        )

    @property
    def items(self):
        return self._query.items

    @property
    def filter(self):
        return self._filter

    @property
    def search(self):
        return self._search
    
    @property
    def member_id(self):
        return self._member_id
