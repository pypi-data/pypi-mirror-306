import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Union

import ipywidgets as widgets
from IPython.display import HTML, display

from .handler import (
    BooleanComponent,
    ComponentBase,
    FloatComponent,
    IntComponent,
    NestedComponent,
    SelectComponent,
    TextComponent,
    UIHandler,
    create_ui_handler,
)

logger = logging.getLogger("hypster.ui.ipywidgets")


class IPyComponent(ABC):
    """Base class for IPyWidgets UI components."""

    def __init__(self, component: Union[ComponentBase, NestedComponent], on_change: Callable):
        self.component = component
        self.on_change = on_change
        self.widget = self._create_widget()

    @abstractmethod
    def _create_widget(self) -> widgets.Widget:
        """Create the IPyWidget."""
        pass

    def render(self) -> widgets.Widget:
        """Render the widget."""
        return self.widget

    def update(self, component: Union[ComponentBase, NestedComponent]) -> None:
        """Update the component and widget."""
        self.component = component
        self._update_widget()

    @abstractmethod
    def _update_widget(self) -> None:
        """Update the widget with current component state."""
        pass


class IPySelectComponent(IPyComponent):
    def _create_widget(self) -> widgets.Widget:
        widget_cls = widgets.SelectMultiple if not self.component.single_value else widgets.Dropdown
        description = self.component.label
        if not self.component.single_value:
            description += " (hold ctrl/cmd for multiple choices)"

        initial_value = (
            list(self.component.value)
            if not self.component.single_value and self.component.value
            else self.component.value
        )

        widget = widget_cls(
            options=self.component.options,
            value=initial_value,
            description=description,
            style={"description_width": "initial"},
            layout=widgets.Layout(background_color="transparent"),
        )

        widget.observe(
            lambda change: self.on_change(
                self.component.id,
                list(change["new"]) if not self.component.single_value else change["new"],
                delay=not self.component.single_value,
            ),
            names="value",
        )
        return widget

    def _update_widget(self) -> None:
        self.widget.options = self.component.options
        self.widget.value = (
            list(self.component.value)
            if not self.component.single_value and self.component.value
            else self.component.value
        )
        self.widget.description = (
            self.component.label + " (hold ctrl/cmd for multiple choices)"
            if not self.component.single_value
            else self.component.label
        )


class IPyNumericComponent(IPyComponent):
    def _create_widget(self) -> widgets.Widget:
        bounds = self.component.bounds
        is_int = isinstance(self.component, IntComponent)

        if not bounds:
            widget_cls = widgets.IntText if is_int else widgets.FloatText
            widget = widget_cls(
                value=self.component.value,
                description=self.component.label,
                step=1 if is_int else 0.01,
                style={"description_width": "initial"},
                layout=widgets.Layout(background_color="transparent"),
            )
        else:
            widget_cls = widgets.BoundedIntText if is_int else widgets.BoundedFloatText
            min_val = bounds.min_val if bounds.min_val is not None else -99999
            max_val = bounds.max_val if bounds.max_val is not None else 99999

            widget = widget_cls(
                value=self.component.value,
                description=self.component.label,
                min=min_val,
                max=max_val,
                step=1 if is_int else 0.01,
                style={"description_width": "initial"},
                layout=widgets.Layout(background_color="transparent"),
            )

        widget.observe(lambda change: self.on_change(self.component.id, change["new"]), names="value")
        return widget

    def _needs_widget_recreation(self) -> bool:
        """Check if widget needs to be recreated due to bounds changes."""
        current_bounds = self.component.bounds
        is_bounded = isinstance(self.widget, (widgets.BoundedIntText, widgets.BoundedFloatText))
        should_be_bounded = current_bounds is not None

        if is_bounded != should_be_bounded:
            return True

        if is_bounded and should_be_bounded:
            current_min = self.widget.min
            current_max = self.widget.max
            new_min = current_bounds.min_val if current_bounds.min_val is not None else -99999
            new_max = current_bounds.max_val if current_bounds.max_val is not None else 99999
            return current_min != new_min or current_max != new_max

        return False

    def _update_widget(self) -> None:
        if self._needs_widget_recreation():
            new_widget = self._create_widget()
            old_widget = self.widget
            self.widget = new_widget
            if hasattr(old_widget, "parent") and old_widget.parent:
                parent = old_widget.parent
                idx = parent.children.index(old_widget)
                parent.children = list(parent.children[:idx]) + [new_widget] + list(parent.children[idx + 1 :])
        else:
            self.widget.value = self.component.value
            self.widget.description = self.component.label


class IPyTextComponent(IPyComponent):
    def _create_widget(self) -> widgets.Widget:
        widget = widgets.Text(
            value=str(self.component.value),
            description=self.component.label,
            style={"description_width": "initial"},
            layout=widgets.Layout(background_color="transparent"),
            continuous_update=False,
        )
        widget.observe(
            lambda change: self.on_change(self.component.id, change["new"], delay=True),
            names="value",
        )
        return widget

    def _update_widget(self) -> None:
        self.widget.value = str(self.component.value)
        self.widget.description = self.component.label


class IPyBooleanComponent(IPyComponent):
    def _create_widget(self) -> widgets.Widget:
        if not self.component.single_value:
            container = widgets.VBox([])
            self._update_multi_widget(container)
            return container
        return self._create_single_widget()

    def _create_single_widget(self) -> widgets.Widget:
        widget = widgets.Checkbox(
            value=self.component.value,
            description=self.component.label,
            style={"description_width": "initial"},
        )
        widget.observe(lambda change: self.on_change(self.component.id, change["new"]), names="value")
        return widget

    def _update_multi_widget(self, container: widgets.VBox) -> None:
        widgets_list = []
        for i, value in enumerate(self.component.value):
            widget = widgets.Checkbox(
                value=value,
                description=f"{self.component.label}[{i}]",
                style={"description_width": "initial"},
            )
            widget.observe(
                lambda change, idx=i: self.on_change(
                    self.component.id, [v if j != idx else change["new"] for j, v in enumerate(self.component.value)]
                ),
                names="value",
            )
            widgets_list.append(widget)
        container.children = widgets_list

    def _update_widget(self) -> None:
        if not self.component.single_value:
            self._update_multi_widget(self.widget)
        else:
            self.widget.value = self.component.value
            self.widget.description = self.component.label


class IPyMultiValueComponent(IPyComponent):
    def _create_widget(self) -> widgets.Widget:
        num_rows = len(self.component.value)
        height = f"{25 + (num_rows * 15)}px"

        widget = widgets.Textarea(
            value=self._format_value(self.component.value),
            description=self.component.label,
            style={"description_width": "initial"},
            layout=widgets.Layout(
                height=height,
                background_color="transparent",
                min_height="52px",
            ),
            continuous_update=False,
        )
        widget.observe(lambda change: self._handle_value_change(change["new"]), names="value")
        return widget

    def _format_value(self, value: list) -> str:
        return "\n".join(str(v) for v in value)

    def _parse_value(self, text: str) -> list:
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if isinstance(self.component, IntComponent):
            values = [int(line) for line in lines]
        elif isinstance(self.component, FloatComponent):
            values = [float(line) for line in lines]
        else:
            values = lines

        if self.component.bounds:
            for val in values:
                if (
                    self.component.bounds.min_val is not None
                    and val < self.component.bounds.min_val
                    or self.component.bounds.max_val is not None
                    and val > self.component.bounds.max_val
                ):
                    raise ValueError(f"Value {val} outside bounds: {self.component.bounds}")

        return values

    def _handle_value_change(self, text: str) -> None:
        try:
            new_value = self._parse_value(text)
            self.on_change(self.component.id, new_value, delay=True)
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid input: {e}")

    def _update_widget(self) -> None:
        self.widget.value = self._format_value(self.component.value)
        self.widget.description = self.component.label
        num_rows = len(self.component.value)
        self.widget.layout.height = f"{25 + (num_rows * 15)}px"


def create_ipy_component(component: Union[ComponentBase, NestedComponent], on_change: Callable) -> IPyComponent:
    """Create appropriate IPyComponent based on component type."""
    if isinstance(component, NestedComponent):
        return IPyPropagateComponent(component, on_change)
    elif isinstance(component, SelectComponent):
        return IPySelectComponent(component, on_change)
    elif isinstance(component, (IntComponent, FloatComponent)):
        if not component.single_value:
            return IPyMultiValueComponent(component, on_change)
        return IPyNumericComponent(component, on_change)
    elif isinstance(component, TextComponent):
        if not component.single_value:
            return IPyMultiValueComponent(component, on_change)
        return IPyTextComponent(component, on_change)
    elif isinstance(component, BooleanComponent):
        return IPyBooleanComponent(component, on_change)
    else:
        raise ValueError(f"Unsupported component type: {type(component)}")


class IPyPropagateComponent(IPyComponent):
    """Widget for handling nested/propagated configurations."""

    def __init__(self, component: NestedComponent, on_change: Callable):
        self.child_components: Dict[str, IPyComponent] = {}
        super().__init__(component, on_change)

    def _create_widget(self) -> widgets.Widget:
        # Create a container with a border
        container = widgets.VBox(
            layout=widgets.Layout(
                border="0.2px solid #ccc",
                padding="10px",
                margin="5px 0",
                background_color="transparent",
                width="fit-content",  # Adjust to content width
                min_width="300px",  # Minimum width to prevent too narrow boxes
            )
        )

        # Add label with larger font
        label = widgets.HTML(
            f"<span style='font-size: 1.2em; \
                font-weight: bold; margin-bottom: 8px; display: block;'>{self.component.label}</span>"
        )

        # Create container for children
        child_widgets = []
        for name, child in self.component.children.items():
            if name not in self.child_components:
                self.child_components[name] = self._create_child_component(name, child)
            child_widgets.append(self.child_components[name].render())

        # Combine label and children
        container.children = [label] + child_widgets
        return container

    def _create_child_component(self, name: str, child: Union[ComponentBase, NestedComponent]) -> IPyComponent:
        """Create a child component with nested path handling."""

        def nested_change_handler(child_id: str, value: Any, delay: bool = False) -> None:
            nested_value = {name: value}
            self.on_change(self.component.id, nested_value, delay)

        return create_ipy_component(child, nested_change_handler)

    def _update_widget(self) -> None:
        # Update children while preserving the label
        label = self.widget.children[0]
        child_widgets = []
        for name, child in self.component.children.items():
            if name not in self.child_components:
                self.child_components[name] = self._create_child_component(name, child)
            child_widgets.append(self.child_components[name].render())

        self.widget.children = [label] + child_widgets


class IPyWidgetsUI:
    """IPyWidgets-based UI implementation."""

    def __init__(self, ui_handler: UIHandler):
        self.ui_handler = ui_handler
        self.ui_components: Dict[str, IPyComponent] = {}
        self.container = widgets.VBox([], layout=widgets.Layout(background_color="transparent"))
        self._update_timer: Optional[asyncio.Future] = None
        self.update_delay = 0.1
        logger.debug("Initialized IPyWidgetsUI")

    async def _delayed_update(self, component_id: str, new_value: Any) -> None:
        if self._update_timer:
            self._update_timer.cancel()
        await asyncio.sleep(self.update_delay)
        self._handle_change_impl(component_id, new_value)

    def _handle_change(self, component_id: str, new_value: Any, delay: bool = False) -> None:
        """Handle component changes, building proper nested structure."""
        if not self.ui_handler:
            return

        # Find the top-level component ID and build nested structure
        path_parts = component_id.split(".")
        if len(path_parts) > 1:
            # Build nested structure from path
            nested_value = new_value
            for key in reversed(path_parts[1:]):
                nested_value = {key: nested_value}
            component_id = path_parts[0]
            new_value = nested_value

        logger.debug(f"Scheduling update for {component_id}: {new_value}")
        if delay:
            asyncio.create_task(self._delayed_update(component_id, new_value))
        else:
            self._handle_change_impl(component_id, new_value)

    def _handle_change_impl(self, component_id: str, new_value: Any) -> None:
        if not self.ui_handler:
            return

        logger.debug(f"Handling change for {component_id}: {new_value}")
        affected_components = self.ui_handler.update_components(component_id, new_value)

        for comp_id in affected_components:
            if comp_id in self.ui_components:
                logger.debug(f"Updating UI component: {comp_id}")
                self.ui_components[comp_id].update(self.ui_handler.components[comp_id])
            else:
                logger.debug(f"Creating new UI component: {comp_id}")
                self.ui_components[comp_id] = self._create_ui_component(self.ui_handler.components[comp_id])

        widgets_list = [
            self.ui_components[comp_id].render() for comp_id in affected_components if comp_id in self.ui_components
        ]
        self.container.children = widgets_list

    def _create_ui_component(self, component: Union[ComponentBase, NestedComponent]) -> IPyComponent:
        return create_ipy_component(component, self._handle_change)

    def _update_display(self) -> None:
        if not self.ui_handler:
            logger.warning("No UI handler set")
            return

        logger.debug("Updating display")
        ordered_components = self.ui_handler.get_ordered_components()
        logger.debug(f"Ordered components: {[comp.id for comp in ordered_components]}")

        if not ordered_components:
            logger.warning("No components found in UI handler")
            return

        current_component_ids = {comp.id for comp in ordered_components}

        for comp_id in list(self.ui_components.keys()):
            if comp_id not in current_component_ids:
                logger.debug(f"Removing obsolete component: {comp_id}")
                self.ui_components.pop(comp_id)

        widgets_list = []
        for component in ordered_components:
            logger.debug(f"Processing component: {component.id} ({component.parameter_type})")
            if component.id not in self.ui_components:
                logger.debug(f"Creating new UI component for: {component.id}")
                self.ui_components[component.id] = self._create_ui_component(component)
            widgets_list.append(self.ui_components[component.id].render())

        self.container.children = widgets_list

    def display(self) -> None:
        self._update_display()
        display(self.container)


def create_interactive_config(config_func: Callable, initial_values: Optional[Dict[str, Any]] = None) -> None:
    logger.debug("Creating interactive config")
    handler = create_ui_handler(config_func=config_func, initial_values=initial_values)
    ui = IPyWidgetsUI(ui_handler=handler)
    ui.display()


def apply_vscode_theme() -> None:
    css = """
    <style>
    .cell-output-ipywidget-background {
        background-color: transparent !important;
    }
    :root {
        --jp-widgets-color: var(--vscode-editor-foreground);
        --jp-widgets-font-size: var(--vscode-editor-font-size);
    }
    </style>
    """
    display(HTML(css))
