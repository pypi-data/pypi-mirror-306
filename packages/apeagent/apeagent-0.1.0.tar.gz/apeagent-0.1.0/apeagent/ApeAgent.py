# ApeAgent.py

from typing import List, Callable, Dict, Any, Union, Optional
import json
import inspect
import concurrent.futures
import logging
from openai import OpenAI

logger = logging.getLogger("ApeAgent")

class Agent:
    client = None

    @classmethod
    def openai_client(cls, api_key: str):
        cls.client = OpenAI(api_key=api_key)

    @classmethod
    def tool(cls, func: Callable):
        return cls.Tool(func)
    
    class Tool:
        def __init__(self, func: Callable):
            self.func = func
            self.name = func.__name__
            self.description = func.__doc__ or "No description provided"
            self.schema = self._create_schema(strict=True)

        def _create_schema(self, strict: bool = False) -> Dict[str, Any]:
            sig = inspect.signature(self.func)
            parameters = {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
            for name, param in sig.parameters.items():
                param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
                parameters["properties"][name] = {
                    "type": self._get_json_type(param_type),
                    "description": f"Parameter {name}"
                }
                if param.default == inspect.Parameter.empty:
                    parameters["required"].append(name)
            return {
                "type": "function",
                "function": {
                    "name": self.name,
                    "description": self.description,
                    "parameters": parameters,
                    "strict": strict
                }
            }

        def _get_json_type(self, py_type: type) -> str:
            type_map = {
                str: "string",
                int: "integer",
                float: "number",
                bool: "boolean",
                list: "array",
                dict: "object"
            }
            return type_map.get(py_type, "string")

        def __call__(self, *args, **kwargs) -> Any:
            try:
                result = self.func(*args, **kwargs)
                logger.info(f"Executed tool '{self.name}' with args={args} kwargs={kwargs} -> result={result}")
                return result
            except Exception as e:
                logger.error(f"Error executing function {self.name}: {str(e)}")
                raise

    def __init__(
        self,
        name: str,
        instructions: str,
        functions: List[Union[Callable, 'Agent']],
        model: str = "gpt-4o",
        parallel_tool_calls: Optional[bool] = None,
        temperature: float = 0.5,
        memory_enabled: bool = False,
        memory_max_conversations: int = 100,  # Limitar el historial de conversación (si se habilita la memoria)
        debug: bool = False
    ):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.parallel_tool_calls = parallel_tool_calls
        self.temperature = temperature
        self.memory_enabled = memory_enabled
        self.memory_max_conversations = memory_max_conversations  # Asigna el límite de memoria de conversaciones
        self.memory = {}  # Diccionario para almacenar el contexto por usuario
        self.functions = []
        self.debug = debug
        self._process_functions(functions)

        self.logger = logging.getLogger(f"ApeAgent.{name}")
        self.logger.setLevel(logging.DEBUG if self.debug else logging.WARNING)

        if self.debug:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
            self.logger.info(f"Initialized agent '{self.name}' with {len(self.functions)} functions")

    def _wrap_agent_as_tool(self, agent: 'Agent') -> 'Agent.Tool':
        def wrapped_agent(message: str) -> str:
            return agent.call(message)
        
        wrapped_agent.__name__ = agent.name
        wrapped_agent.__doc__ = f"Agent that can: {agent.instructions}"
        
        tool = self.Tool(wrapped_agent)
        tool.schema = {
            "type": "function",
            "function": {
                "name": agent.name,
                "description": agent.instructions,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to send to the agent"
                        }
                    },
                    "required": ["message"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
        return tool

    def _process_functions(self, functions: List[Union[Callable, 'Agent']]):
        for func in functions:
            if isinstance(func, Agent):
                self.functions.append(self._wrap_agent_as_tool(func))
            elif isinstance(func, Agent.Tool):
                self.functions.append(func)
            elif callable(func):
                self.functions.append(self.Tool(func))

    def _get_tools_schema(self) -> List[Dict[str, Any]]:
        return [func.schema for func in self.functions]

    def _execute_tool_calls(self, tool_calls, user_input: str) -> List[Dict[str, Any]]:
        function_results = []
        function_executions = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            try:
                function_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                self.logger.error(f"Error parsing arguments: {str(e)}")
                continue

            for function in self.functions:
                if function.name == function_name:
                    args = {"message": function_args.get('message', user_input)} if isinstance(function.func, type(self.call)) else function_args
                    function_executions.append({
                        "function": function,
                        "args": args,
                        "tool_call": tool_call
                    })
                    break

        if self.parallel_tool_calls and len(function_executions) > 1:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for execution in function_executions:
                    future = executor.submit(execution["function"].__call__, **execution["args"])
                    futures.append((future, execution["tool_call"]))
                
                for future, tool_call in futures:
                    self.logger.debug(f"Executing parallel tool '{tool_call.function.name}'")
                    try:
                        result = future.result()
                        function_results.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result)
                        })
                        self.logger.debug(f"Parallel tool '{tool_call.function.name}' executed successfully.")
                    except Exception as e:
                        self.logger.error(f"Error in parallel execution: {str(e)}")
                        function_results.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": f"Error executing function: {str(e)}"
                        })
        else:
            for execution in function_executions:
                try:
                    result = execution["function"](**execution["args"])
                    function_results.append({
                        "role": "tool",
                        "tool_call_id": execution["tool_call"].id,
                        "content": str(result)
                    })
                    self.logger.debug(f"Sequential tool '{execution['function'].name}' executed successfully.")
                except Exception as e:
                    self.logger.error(f"Error in sequential execution: {str(e)}")
                    function_results.append({
                        "role": "tool",
                        "tool_call_id": execution["tool_call"].id,
                        "content": f"Error executing function: {str(e)}"
                    })

        self.logger.debug(f"Tool calls executed: {function_results}")
        return function_results

    def _trim_memory(self, messages: List[Dict[str, Any]]):
        """Limpia la memoria eliminando mensajes antiguos si exceden el límite."""
        # Si el límite se excede, recorta manteniendo el mensaje de sistema inicial
        if len(messages) > self.memory_max_conversations + 1:
            messages[:] = [messages[0]] + messages[-self.memory_max_conversations:]

    def call(self, user_input: str, user_id: Optional[str] = None) -> str:
        """Procesa un mensaje del usuario y mantiene el contexto de la conversación por usuario."""
        try:
            # Recupera o inicia el contexto de memoria para el usuario
            if self.memory_enabled and user_id:
                if user_id not in self.memory:
                    self.memory[user_id] = [
                        {"role": "system", "content": self.instructions}
                    ]
                messages = self.memory[user_id]  # Usar el contexto de memoria para este usuario
            else:
                messages = [{"role": "system", "content": self.instructions}]

            # Añade el mensaje del usuario actual
            messages.append({"role": "user", "content": user_input})

            # Limita el número de mensajes en memoria si excede el máximo
            if self.memory_enabled and user_id:
                self._trim_memory(messages)

            while True:
                api_params = {
                    "model": self.model,
                    "messages": messages,
                    "tools": self._get_tools_schema(),
                    "tool_choice": "auto",
                    "temperature": self.temperature
                }

                if self.parallel_tool_calls is not None:
                    api_params["parallel_tool_calls"] = self.parallel_tool_calls

                response = self.client.chat.completions.create(**api_params)

                assistant_message = response.choices[0].message
                finish_reason = response.choices[0].finish_reason

                if finish_reason == "length":
                    self.logger.warning("Response was truncated due to length limits")
                elif finish_reason == "content_filter":
                    self.logger.warning("Response was filtered due to content policy")

                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": assistant_message.tool_calls
                })

                if self.memory_enabled and user_id:
                    self.memory[user_id] = messages  # Actualiza la memoria con el contexto actual

                if not assistant_message.tool_calls:
                    return assistant_message.content or ""

                function_results = self._execute_tool_calls(assistant_message.tool_calls, user_input)
                messages.extend(function_results)

        except Exception as e:
            error_msg = f"Error in agent '{self.name}': {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
