from typing import Optional

from .types import Theme, CriteriaTreeElement, Criterion, TaskGroup, Task, TaskItem, CriteriaTree


def to_color_hex_string(color):
    """
    Convert a color object to a hex string
    """
    if isinstance(color, str):
        return color
    return f"#{color.red:02x}{color.green:02x}{color.blue:02x}"


def should_hide_code(element: CriteriaTreeElement | str | dict) -> bool:
    """
    Check if a tree element should be hidden in the output
    """
    if element.options is not None and element.options.get('hideCode', False):
        return True

    """
    @deprecated this is the old way of doing it
    """
    if isinstance(element, str):
        return element.startswith('_')
    if isinstance(element, dict):
        code: Optional[str] = element.get('code', None)
        if code is None:
            raise ValueError("Element must have a 'code' key")
        return code.startswith('_')
    return element.code.startswith('_')


def get_qualified_name(element: Theme | Criterion | TaskGroup | Task | dict) -> str:
    """
    Get the qualified name of a tree element, which is the title with the code prepended if it is different
    """
    if isinstance(element, dict):
        title, code = (element.get('title', None), element.get('code', None))
        if title is None or code is None:
            raise ValueError("Element must have 'title' and 'code' keys")
    else:
        title, code = element.title, element.code
    if code.startswith('_'):
        code = code[1:]
    if element.title == code:
        return element.title
    return f"{code} {element.title}"


def resolve_code(element: CriteriaTreeElement | str | dict) -> str:
    """
    Get the code for a tree element, stripping away unnecessary characters
    """
    if isinstance(element, str):
        resolved_code = element
    elif isinstance(element, dict):
        resolved_code = element.get('code', None)
        if resolved_code is None:
            raise ValueError("Element must have a 'code' key")
    else:
        resolved_code = element.code
    return resolved_code[1:] if resolved_code.startswith('_') else resolved_code


def find_in_tree(tree: CriteriaTree, code: str) -> Optional[CriteriaTreeElement]:
    """
    Find an element in the criteria tree by its code
    """
    def _search_elements(elements: list[CriteriaTreeElement]):
        for element in elements:
            if element.code == code:
                return element
            if not isinstance(element, TaskItem):
                element = _search_elements(element.items)
                if element is not None:
                    return element
        return None

    return _search_elements(tree.themes)
