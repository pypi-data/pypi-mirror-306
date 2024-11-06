from typing import List, Dict, Any, Optional


class Component:
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("Must implement to_dict method.")


class Header(Component):
    def __init__(self, title: str, subtitle: Optional[str] = None, logo: Optional[str] = None):
        self.title = title
        self.subtitle = subtitle
        self.logo = logo

    def to_dict(self):
        return {
            'type': 'header',
            'properties': {
                'title': self.title,
                'subtitle': self.subtitle,
                'logo': self.logo,
            },
        }


class Footer(Component):
    def __init__(self, content: str):
        self.content = content

    def to_dict(self):
        return {
            'type': 'footer',
            'properties': {
                'content': self.content,
            },
        }


class Sidebar(Component):
    def __init__(self, items: List[str]):
        self.items = items

    def to_dict(self):
        return {
            'type': 'sidebar',
            'properties': {
                'items': self.items,
            },
        }

class Text(Component):
    def __init__(self, content: str):
        self.content = content

    def to_dict(self):
        return {
            'type': 'text',
            'properties': {
                'content': self.content,
            },
        }
    

class MainContent(Component):
    def __init__(self, children: List[Component]):
        self.children = children

    def to_dict(self):
        return {
            'type': 'main-content',
            'children': [child.to_dict() for child in self.children],
        }


class ChatWindow(Component):
    def __init__(self, placeholder: str = 'Type your message...', send_button_label: str = 'Send', endpoint_url: str = '/api/chat'):
        self.placeholder = placeholder
        self.send_button_label = send_button_label
        self.endpoint_url = endpoint_url

    def to_dict(self):
        return {
            'type': 'chat-window',
            'properties': {
                'placeholder': self.placeholder,
                'sendButtonLabel': self.send_button_label,
                'endpointUrl': self.endpoint_url,
            },
        }


class DataTable(Component):
    def __init__(
        self,
        columns: List[Dict[str, Any]],
        data_source: str,
        actions: Optional[List[Dict[str, Any]]] = None,
    ):
        self.columns = columns
        self.data_source = data_source
        self.actions = actions or []

    def to_dict(self):
        return {
            'type': 'data-table',
            'properties': {
                'columns': self.columns,
                'dataSource': self.data_source,
                'actions': self.actions,
            },
        }


class Chart(Component):
    def __init__(self, chart_type: str, data_source: str, options: Optional[Dict[str, Any]] = None):
        self.chart_type = chart_type
        self.data_source = data_source
        self.options = options or {}

    def to_dict(self):
        return {
            'type': 'chart',
            'properties': {
                'chartType': self.chart_type,
                'dataSource': self.data_source,
                'options': self.options,
            },
        }


class Form(Component):
    def __init__(self, children: List[Component], on_submit: List[str]):
        self.children = children
        self.on_submit = on_submit

    def to_dict(self):
        return {
            'type': 'form',
            'properties': {
                'onSubmit': self.on_submit,
            },
            'children': [child.to_dict() for child in self.children],
        }


class FormItem(Component):
    def __init__(self, label: str, children: List[Component]):
        self.label = label
        self.children = children

    def to_dict(self):
        return {
            'type': 'form-item',
            'properties': {
                'label': self.label,
            },
            'children': [child.to_dict() for child in self.children],
        }


class Input(Component):
    def __init__(self, name: str, placeholder: str = '', required: bool = False):
        self.name = name
        self.placeholder = placeholder
        self.required = required

    def to_dict(self):
        return {
            'type': 'input',
            'properties': {
                'name': self.name,
                'placeholder': self.placeholder,
                'required': self.required,
            },
        }


class TextArea(Component):
    def __init__(self, name: str, placeholder: str = ''):
        self.name = name
        self.placeholder = placeholder

    def to_dict(self):
        return {
            'type': 'textarea',
            'properties': {
                'name': self.name,
                'placeholder': self.placeholder,
            },
        }


class Upload(Component):
    def __init__(self, name: str, required: bool = False):
        self.name = name
        self.required = required

    def to_dict(self):
        return {
            'type': 'upload',
            'properties': {
                'name': self.name,
                'required': self.required,
            },
        }


class Button(Component):
    def __init__(self, label: str, button_type: str = 'button', disabled: bool = False, on_click: Optional[str] = None):
        self.label = label
        self.button_type = button_type
        self.disabled = disabled
        self.on_click = on_click

    def to_dict(self):
        return {
            'type': 'button',
            'properties': {
                'label': self.label,
                'type': self.button_type,
                'disabled': self.disabled,
                'onClick': self.on_click,
            },
        }


class Tabs(Component):
    def __init__(self, children: List['Tab']):
        self.children = children

    def to_dict(self):
        return {
            'type': 'tabs',
            'children': [child.to_dict() for child in self.children],
        }


class Tab(Component):
    def __init__(self, label: str, children: List[Component]):
        self.label = label
        self.children = children

    def to_dict(self):
        return {
            'type': 'tab',
            'properties': {
                'label': self.label,
            },
            'children': [child.to_dict() for child in self.children],
        }


class ModalDialog(Component):
    def __init__(
        self,
        name: str,
        title: str,
        content: List[Component],
        visible: bool = False,
        on_close: Optional[str] = None,
    ):
        self.name = name 
        self.title = title
        self.content = content
        self.visible = visible
        self.on_close = on_close

    def to_dict(self):
        return {
            'type': 'modal-dialog',
            'properties': {
                'name': self.name,
                'title': self.title,
                'visible': self.visible,
                'onClose': self.on_close,
            },
            'children': [component.to_dict() for component in self.content],
        }


class Page(Component):
    def __init__(self, name: str, path: str, components: List[Component]):
        self.name = name
        self.path = path
        self.components = components

    def to_dict(self):
        return {
            'type': 'page',
            'properties': {
                'name': self.name,
                'path': self.path,
            },
            'children': [component.to_dict() for component in self.components],
        }


class Action:
    def __init__(
        self,
        action_type: str,
        method: str,
        url: Optional[str] = None,
        data: Optional[Any] = None,
        state: Optional[str] = None,
        on_success: Optional[str] = None,
    ):
        self.action_type = action_type
        self.method = method
        self.url = url
        self.data = data
        self.state = state
        self.on_success = on_success

    def to_dict(self):
        return {
            'type': self.action_type,
            'method': self.method,
            'url': self.url,
            'data': self.data,
            'state': self.state,
            'onSuccess': self.on_success,
        }


class CustomInputOutputContent(Component):
    def __init__(
        self,        
        data_source: str,
        actions: Optional[List[Dict[str, Any]]] = None,
    ):        
        self.data_source = data_source
        self.actions = actions or []

    def to_dict(self):
        return {
            'type': 'custom-input-output-content',
            'properties': {                
                'dataSource': self.data_source,
                'actions': self.actions,
            },
        }

def render(
    layout: str,
    components: List[Component],
    actions: Optional[Dict[str, Action]] = None,
    initial_actions: Optional[List[str]] = None,
    pages: Optional[List['Page']] = None,
) -> Dict[str, Any]:
    render_def = {
        'layout': layout,
        'components': [component.to_dict() for component in components],
        'actions': {name: action.to_dict() for name, action in (actions or {}).items()},
        'initialActions': initial_actions or [],
    }
    if pages:
        render_def['pages'] = [page.to_dict() for page in pages]
    return render_def
