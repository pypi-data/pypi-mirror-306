import inspect
import json
import logging
from functools import wraps
from itertools import islice
import re
from typing import Final

from duck_agents.llm.session_factory import SessionFactory

_logger = logging.getLogger(__name__)

_required_interface_explanation_template : Final = """
        To gather Information before providing your answer to a function call, you may perform function calls yourself.
        Apart from returning a result, you must only communicate in the form of these function calls.
        You may perform at most {call_limit} function calls after a user's function call before you return the result.
        If you have gathered sufficient information before reaching this limit, you should return earlier.
        You may spread your function calls across multiple responses to use information from past calls when making new calls.

        If you decide to invoke any of the function(s), you MUST put it in the JSON format of [{{"name": func_name_1, "args": {{params_name_1: params_value_1, params_name_2: params_value_2, ...}}}}, {{"name": func_name2, "args":{{...}}}}, ...]\n
        You MUST NOT include any other text in the response.
        
        You will receive the list of results appended to the call signatures in the JSON format of [{{"name": func_name_1, "result":result_1}}, {{"name": func_name2, "result":result_2}}, ...]\n

        Here is a list of functions in JSON format that you can invoke.\n\n{functions}\n
        """

_provided_interface_explanation_template  : Final = """
        The user will only communicate with you via function calls. 
        The user will call the functions in the format {{"name": func_name1, "args":{{params_name1=params_value1, params_name2=params_value2...}}}}, func_name2:{{params}}}}\n
        
        You MUST use the provided function description to accurately calculate the function's result for the provided arguments.
        You MUST include an integer confidence value between 0 and 100 (inclusive) in your answer, 0 indicating that you are not at all confident that your provided result is correct, 100 indicating that you are extremely confident.
        You MUST provide the returning function's name.
        You MUST respond in the JSON format of {{ "name" name_value, "value": return_value, "confidence": confidence_value }} 
        You SHOULD NOT include any other text in the response.

        Here is a list of functions in JSON format that the user may invoke.\n\n{functions}\n
        """

_system_prompt_template = """
{task_description}\n\n\n
{provided}\n\n\n
{required}
"""

def extract_descriptions(doc: str) -> dict[str, str]:
    if not doc:
        return {}
    split_docs = re.split(r"Args:|Returns:", doc)
    if len(split_docs) < 2:
        return {}

    method_description = re.sub(r'\n+', ' ', re.sub(r' +', ' ', split_docs[0])).strip()
    return_description = re.sub(r'\n+', ' ', re.sub(r' +', ' ', split_docs[2])).strip()

    param_descriptions = dict(re.findall(r"(\w+):(.+)", split_docs[1]))
    param_descriptions = {key.strip(): value.strip() for key, value in param_descriptions.items()}

    return {
        "method": method_description,
        "parameters": param_descriptions,
        "return": return_description
    }

#TODO: add logging to decorators?
#TODO: properly implement required interface
def required(func):
    @wraps(func)
    async def wrapped_function(*args, **kwargs):
        return await func(*args, **kwargs)

    wrapped_function.meta = {
        "interface_direction": "required"
    }
    return wrapped_function

#TODO: add logging to decorators?
def provided(max_retries=0):
    def provided_decorator(func):
        @wraps(func)
        async def wrapped_function(*args, **kwargs):
            marshalled_call = __marshal_llm_func_call(func, *args[1:], **kwargs)
            _logger.info("Trying to query {agent_type} with the following call: {marshalled_call}".format(agent_type=type(args[0]).__name__, marshalled_call=marshalled_call))
            result = await args[0].call_method(marshalled_call, max_retries=max_retries)
            _logger.info("{agent_type} returned the following result: {result}".format(agent_type=type(args[0]).__name__, result=result))
            return result
        wrapped_function.meta = {
            "interface_direction": "provided"
        }
        return wrapped_function
    return provided_decorator

#TODO: include kwargs
#TODO: check if number of args matches params
def __marshal_llm_func_call(func, *args, **kwargs) -> str:
    call_dict = {
        "name": func.__name__,
        "args": dict(zip([
            param.name
        for param in islice(inspect.signature(func).parameters.values(), 1, None)], args)),
    }
    return json.dumps(call_dict)

# TODO: Actually implement call limit (limit recursion_depth in answer-queries)
class BaseAgent:
    def __init__(self, llm_session_factory: SessionFactory, task_description: str, retain_history=False, system_prompt=None, call_limit=10):
        self.llm_session_factory = llm_session_factory
        self.retain_history = retain_history
        self.call_limit = call_limit
        if system_prompt is None:
            self.system_prompt = self.__construct_system_prompt(task_description)
        else:
            self.system_prompt = system_prompt
        self.llm_session = self.llm_session_factory.create_session(system_prompt=self.system_prompt)
        self.agent_type = type(self).__name__

    def __methods(self):
        methods = {
            "required": [],
            "provided": []
        }
        for i in inspect.getmembers(self, predicate=inspect.ismethod):
            method = i[1]
            if not hasattr(method, "meta"):
                continue

            descriptions = extract_descriptions(method.__doc__)
            method_metadata = {
                "name": method.__name__,
                "description": descriptions["method"],
                "parameters": {
                    param.name: {
                        "description": descriptions["parameters"][param.name],
                        "type": param.annotation.__name__,
                    } for param in inspect.signature(method).parameters.values()
                },
                "return": {
                    "description": descriptions["return"],
                    "type": method.__annotations__["return"].__name__
                }
            }
            if method.meta["interface_direction"] == "required":
                methods["required"].append(method_metadata)
            elif method.meta["interface_direction"] == "provided":
                methods["provided"].append(method_metadata)
        return methods

    async def call_method(self, call: str, max_retries=0):
        _logger.debug("Agent of type {agent_type} called with signature:\n{signature}".format(agent_type=type(self).__name__, signature=call))
        result = await self.__answer_queries(await self.llm_session.prompt(call))
        if not self.retain_history:
            self.llm_session.clear_history()
        _logger.debug("{agent_type} return value for last function call:\n{result}".format(agent_type=type(self).__name__, result=result))
        return result

    # TODO check if name corresponds to called function
    # TODO: ensure that only the functions are called that are meant to be callable by the llm (i.e. its required interface)
    # TODO: structure returns/function calls in a way to better differentiate between them
    async def __answer_queries(self, llm_response: dict, retries_left=0):
        if "value" in llm_response:
            return llm_response

        if not len(llm_response):
            raise RuntimeError("{agent_type} did not return anything.".format(agent_type=type(self).__name__))

        results = []
        _logger.debug("{agent_type} is trying to make the following function call:\n{call}".format(agent_type=type(self).__name__,call=json.dumps(llm_response,indent=4)))
        for call in llm_response:
            try:
                func = getattr(self, call["name"])
                results.append({"name": call["name"], "result": func(**call["args"])})
            except:
                if retries_left > 0:
                    _logger.warning("LLM-issued call could not be executed. Retrying. \n Call: {call}".format(call=call))
                    return await self.__answer_queries(await self.llm_session.retry_last(), retries_left=retries_left - 1)
                elif retries_left == 0:
                    _logger.warning("LLM-issued call could not be executed. Aborting query after max retries. \n Call: {call}".format(call=call))
                    return

        _logger.debug("Returning results to {agent_type}:\n{results}".format(agent_type=type(self).__name__,results=json.dumps(results,indent=4)))
        return await self.__answer_queries(await self.llm_session.prompt(json.dumps(results)))



    def __construct_system_prompt(self, task_description):
        methods = self.__methods()
        req = _required_interface_explanation_template.format(call_limit=self.call_limit, functions=methods["required"]) if len(methods["required"]) > 0 else ""
        prov = _provided_interface_explanation_template.format(functions=methods["provided"])
        return _system_prompt_template.format(task_description=task_description, required=req, provided=prov)