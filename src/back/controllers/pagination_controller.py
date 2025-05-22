from enum import Enum

# TODO: This should be tested with unit tests.
class PaginationController:
    class Direction(Enum):
        PREV: int = -1
        NEXT: int = 1

    def __init__(self, total_count:int, max_page_size:int, filters_str: str) -> None:
        self.max_page_size: int = max_page_size
        self.last_page: int = self.get_total_pages(total_count, max_page_size) - 1
        self.prev_page: int = None
        self.curr_page: int = 0
        self.next_page: int = None if self.total_pages == 1 else self.curr_page + 1
        self.filters_str: str = filters_str


    @property
    def prev_link(self) -> str|None:
        return self.get_pagination_link('assets', self.prev_page)


    @property
    def next_link(self) -> str|None:
        return self.get_pagination_link('assets', self.next_page)


    def get_pagination_link(self, resource:str, page:int|None) -> str|None:
        # failsafe:
        if page is None:
            return None

        # debug: '?' added between page number and filters_str (does anything need to be adjusted with the filter string passed in?)
        return f'/{resource}/{str(page)}?{self.filters_str}'


    def get_total_pages(self, total_count:int, max_page_size:int) -> int:
        if (total_count > 0):
            total_pages = (total_count + max_page_size - 1) // max_page_size  # ceiling division
        else:
            total_pages = 0

        assert total_count >= total_pages, "There must be at least as many assets as there are pages to show them!"  # TODO: Change this to throw an exception

        return total_pages


    def _update_forward(self) -> None:
        if self.curr_page == self.last_page:
            # do nothing because we are on the last page (cannot move past it)
            # this case should also hold true when there is only one page
            pass
        else:
            # we should be at least one away from the last page
            self.prev_page = self.curr_page # using curr_page because it should never be None
            self.curr_page = self.curr_page + 1 # now that we have updated curr_page, the next check...
            if self.curr_page == self.last_page:
                self.next_page = None # indicating there is not a next page
            else:
                self.next_page = self.curr_page + 1


    def _update_backward(self) -> None:
        if self.curr_page == 0:
            # current page is already at 0, so no movement
            pass
        else:
            # we should be at least one away from the first page
            self.next_page = self.curr_page # using curr_page because it should never be None
            self.curr_page = self.curr_page - 1 # now that we have updated curr_page, the next check...
            if self.curr_page == 0:
                self.prev_page = None # indicating there is not a previous page
            else:
                self.prev_page = self.curr_page - 1


    def update(self, direction: Direction) -> None:
        '''
        TODO: check if this method's logic is correct

        If prev is None, this means we have no previous page to go to.
        Likewise, if next is None, this means we have no next page to go to.
          For example, we may be on the last page with no further pages.
        '''
        if direction == self.Direction.NEXT:
            self._update_forward()
        elif direction == self.Direction.PREV:
            self._update_backward()


    def __repr__(self) -> str:
        return f"PaginationController(max_page_size={self.max_page_size}, total_pages={self.total_pages}, prev_page={self.prev_page}, curr_page={self.curr_page}, next_page={self.next_page})"
