from typing import Callable, Optional, Set, Literal, Any, Dict
from functools import wraps
import threading
import time
import ast
import inspect
import logging

from synth_sdk.tracing.abstractions import (
    Event,
    AgentComputeStep,
    EnvironmentComputeStep,
)
from synth_sdk.tracing.events.store import event_store

logger = logging.getLogger(__name__)

# Thread-local storage for active events
_local = threading.local()


def get_current_event(event_type: str) -> "Event":
    """
    Get the current active event of the specified type.
    Raises ValueError if no such event exists.
    """
    events = getattr(_local, "active_events", {})
    if event_type not in events:
        raise ValueError(f"No active event of type '{event_type}' found")
    return events[event_type]


def set_current_event(event: Optional["Event"]):
    """
    Set the current event, ending any existing events of the same type.
    If event is None, it clears the current event of that type.
    """
    if event is None:
        # Assuming event_type needs to be provided to clear
        raise ValueError("Event cannot be None when setting current event.")
    
    logger.debug(f"Setting current event of type {event.event_type}")

    if not hasattr(_local, "active_events"):
        _local.active_events = {}
        logger.debug("Initialized active_events in thread local storage")

    # If there's an existing event of the same type, end it
    if event.event_type in _local.active_events:
        logger.debug(f"Found existing event of type {event.event_type}")
        existing_event = _local.active_events[event.event_type]
        existing_event.closed = time.time()
        logger.debug(f"Closed existing event of type {event.event_type} at {existing_event.closed}")

        # Store the closed event if system_id is present
        if hasattr(_local, "system_id"):
            logger.debug(f"Storing closed event for system {_local.system_id}")
            try:
                event_store.add_event(_local.system_id, existing_event)
                logger.debug("Successfully stored closed event")
            except Exception as e:
                logger.error(f"Failed to store closed event: {str(e)}")
                raise

    else:
        logger.debug(f"No existing event of type {event.event_type}")

    # Set the new event
    _local.active_events[event.event_type] = event
    logger.debug("New event set as current")


def clear_current_event(event_type: str):
    if hasattr(_local, "active_events"):
        _local.active_events.pop(event_type, None)
        logger.debug(f"Cleared current event of type {event_type}")


def end_event(event_type: str) -> Optional[Event]:
    """End the current event and store it."""
    current_event = get_current_event(event_type)
    if current_event:
        current_event.closed = time.time()
        # Store the event
        if hasattr(_local, "system_id"):
            event_store.add_event(_local.system_id, current_event)
        clear_current_event(event_type)
    return current_event


def trace_system(
    origin: Literal["agent", "environment"],
    event_type: str,
    log_vars_input: Optional[Set[str]] = None,
    log_vars_output: Optional[Set[str]] = None,
    log_result: bool = False,
    manage_event: Literal["create", "end", "lazy_end", None] = None,
    increment_partition: bool = False,
    verbose: bool = False,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        # Retrieve the original source code of the function
        try:
            source = inspect.getsource(func)
            logger.debug(f"Original source:\n{source}")
            
            # Split into lines and find the function definition
            lines = source.splitlines()
            logger.debug(f"Number of lines: {len(lines)}")
            
            # Find the actual function definition line
            func_def_idx = -1
            for i, line in enumerate(lines):
                if line.lstrip().startswith(('def ', 'async def ')):
                    func_def_idx = i
                    break
            
            if func_def_idx == -1:
                logger.error("Could not find function definition")
                return func
                
            # Get the indentation of the function definition
            func_def_line = lines[func_def_idx]
            base_indent = len(func_def_line) - len(func_def_line.lstrip())
            logger.debug(f"Base indentation level: {base_indent}")
            
            # Keep only the function definition and body, properly indented
            relevant_lines = lines[func_def_idx:]
            # Remove the base indentation from all lines
            cleaned_lines = []
            for line in relevant_lines:
                if line.strip():  # If line is not empty
                    # Remove only the base indentation level
                    if line.startswith(' ' * base_indent):
                        cleaned_lines.append(line[base_indent:])
                    else:
                        cleaned_lines.append(line)
                else:
                    cleaned_lines.append('')
            
            source = '\n'.join(cleaned_lines)
            logger.debug(f"Processed source before parsing:\n{source}")
            
            # Add artificial indentation to the body if needed
            lines = source.splitlines()
            if len(lines) > 1:  # If there's more than just the function definition
                body_lines = lines[1:]
                # If the first non-empty body line isn't indented
                if any(line.strip() and not line.startswith('    ') for line in body_lines):
                    body = '\n'.join('    ' + line if line.strip() else line for line in body_lines)
                    source = f"{lines[0]}\n{body}"
                    logger.debug(f"Added indentation to body. Final source:\n{source}")
            
        except (OSError, TypeError) as e:
            logger.error(f"Could not retrieve source code for the function: {str(e)}")
            return func

        # Parse the source code into an AST
        try:
            logger.debug("Attempting to parse source code into AST")
            parsed_ast = ast.parse(source)
            logger.debug("Successfully parsed source code into AST")
        except SyntaxError as e:
            logger.error(f"Failed to parse function source code: {e}")
            logger.error(f"Problematic source code:\n{source}")
            return func

        class LoggerInjector(ast.NodeTransformer):
            def __init__(self, input_vars: Set[str], output_vars: Set[str]):
                self.input_vars = input_vars or set()
                self.output_vars = output_vars or set()
                self.logged_inputs = set()
                super().__init__()

            def visit_FunctionDef(self, node):
                return self._process_function(node)

            def visit_AsyncFunctionDef(self, node):
                return self._process_function(node)

            def _process_function(self, node):
                # Keep original node attributes
                new_body = []
                for stmt in node.body:
                    new_body.append(stmt)
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Name):
                                var_name = target.id
                                if var_name in self.input_vars and var_name not in self.logged_inputs:
                                    new_body.append(self.create_log_stmt('input', var_name))
                                    self.logged_inputs.add(var_name)
                                if var_name in self.output_vars:
                                    new_body.append(self.create_log_stmt('output', var_name))
                node.body = new_body
                return node

            def create_log_stmt(self, var_type: str, var_name: str):
                return ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id='logger', ctx=ast.Load()),
                            attr='info',
                            ctx=ast.Load()
                        ),
                        args=[
                            ast.Constant(value=f"Logged {var_type} variable '{var_name}': {{}}"),
                            ast.Name(id=var_name, ctx=ast.Load())
                        ],
                        keywords=[]
                    )
                )

        # Apply the AST transformer to inject logging
        transformer = LoggerInjector(log_vars_input, log_vars_output)
        transformed_ast = transformer.visit(parsed_ast)
        ast.fix_missing_locations(transformed_ast)

        # Compile and execute the modified AST
        try:
            compiled_code = compile(transformed_ast, filename="<ast>", mode="exec")
            func_namespace = {**func.__globals__}
            exec(compiled_code, func_namespace)
            modified_func = func_namespace[func.__name__]
        except Exception as e:
            logger.error(f"Failed to transform function: {e}")
            return func  # Return original function on error

        @wraps(modified_func)
        def wrapper(*args, **kwargs):
            if not hasattr(modified_func, '__self__') or not modified_func.__self__:
                if not args:
                    raise ValueError("Instance method expected, but no arguments were passed.")
                self_instance = args[0]
            else:
                self_instance = modified_func.__self__
            
            if not hasattr(self_instance, 'system_id'):
                raise ValueError("Instance missing required system_id attribute")
            
            _local.system_id = self_instance.system_id
            logger.debug(f"Set system_id in thread local: {_local.system_id}")

            # Initialize active_events if not present
            if not hasattr(_local, 'active_events'):
                _local.active_events = {}
                logger.debug("Initialized active_events in thread local storage")

            event = None
            try:
                if manage_event == "create":
                    logger.debug("Creating new event")
                    event = Event(
                        event_type=event_type,
                        opened=time.time(),
                        closed=None,
                        partition_index=0,
                        agent_compute_steps=[],
                        environment_compute_steps=[]
                    )
                    if increment_partition:
                        event.partition_index = event_store.increment_partition(_local.system_id)
                        logger.debug(f"Incremented partition to: {event.partition_index}")

                    # Use set_current_event to handle existing events
                    set_current_event(event)
                    logger.debug(f"Created and set new event: {event_type}")
                
                # Execute the modified function, which now includes logging
                result = modified_func(*args, **kwargs)

                # Handle event management after function execution
                if manage_event in ["end", "lazy_end"] and event_type in _local.active_events:
                    current_event = _local.active_events[event_type]
                    current_event.closed = time.time()
                    # No need to re-add the event; it's already in the event store
                    logger.debug(f"Closed event {event_type} for system {_local.system_id}")
                    del _local.active_events[event_type]

                return result
            finally:
                if hasattr(_local, 'system_id'):
                    logger.debug(f"Cleaning up system_id: {_local.system_id}")
                    delattr(_local, 'system_id')

        return wrapper

    return decorator
