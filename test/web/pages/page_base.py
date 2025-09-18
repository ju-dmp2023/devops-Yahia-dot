from typing import Dict, Callable, Union, Optional
from playwright.sync_api import Page, Locator, expect

locator = Union[str, Locator, Callable[[Page], Locator]]

class PageBase:
    ELEMENTS: Dict[str, locator] = {} 

    def __init__(self, page: Page, elements: Optional[Dict[str, locator]] = None) -> None:
        self.page = page
        self.el: Dict[str, Locator] = {}
        self._add_elements(self.ELEMENTS)
        if elements:
            self._add_elements(elements)

    def _add_elements(self, selectors: Dict[str, locator]) -> None:
        for name, sel in selectors.items():
            if isinstance(sel, Locator):
                self.el[name] = sel
            elif isinstance(sel, str):
                self.el[name] = self.page.locator(sel)
            elif callable(sel):
                self.el[name] = sel(self.page)
            else:
                raise TypeError(
                    f"Selector for '{name}' must be str, Locator, or Callable[[Page], Locator]"
                )

    # helpers
    def element(self, name: str) -> Locator:
        try:
            return self.el[name]
        except KeyError:
            raise KeyError(f"Unknown element '{name}'. Available: {list(self.el)}")
