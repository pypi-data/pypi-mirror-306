from typing import Callable, Any, List
import inspect

from . import SuitBuildUtils

from .SuitMethodParameterInfo import TailParameterType

from ..Decorators.DecoratorUtils import get_info
from ..RequestStatus import RequestStatus
from .SuitContext import SuitContext
from .SuitShell import SuitShell, MemberType


class SuitMethodShell(SuitShell):
    """
    Object's Member which may be a method.
    """

    def __init__(self, method: Callable, factory: Callable[[SuitContext], Any], absoluteName=None):
        super().__init__(method, factory, absoluteName)
        self.Method = method
        sig = inspect.signature(method)
        parameters = [param for (_, param) in filter(lambda x: x[0] != 'self', sig.parameters.items())]

        if 'self' not in sig.parameters:
            # For static methods
            self._instanceFactory = lambda _: None
        else:
            self._instanceFactory=factory
        self.Parameters = parameters
        self._suitMethodParameterInfo = SuitBuildUtils.GetMethodParameterInfo(
            self.Method)
        info = get_info(method)
        if info is None:
            # TODO: Auto Info
            self.Type = MemberType.MethodWithoutInfo
            infoSb = ''
            if self._suitMethodParameterInfo.MaxParameterCount > 0:
                for parameter in self.Parameters:
                    infoSb += parameter.name
                    if parameter.annotation == list or parameter.annotation == tuple:

                        infoSb += "[]"
                    elif getattr(parameters[-1].annotation, "IDynamicParameter", None) is not None:

                        infoSb += "{}"
                    elif parameter.default != inspect.Parameter.empty:
                        infoSb += f"={parameter.default}"

                    else:
                        infoSb += ""
                    infoSb += ','
                self._info = infoSb[:-1]
        else:
            self.Type = MemberType.MethodWithInfo
            self._info = info

    @property
    def MemberCount(self):
        return len(self.Parameters)

    @classmethod
    def FromDelegate(cls, methodName, delegate: Callable):
        return cls(delegate, lambda _: None, methodName)

    @classmethod
    def FromInstance(cls, method: Callable, factory: Callable[[SuitContext], Any]):
        return cls(method, factory)

    def MayExecute(self, request: List[str]) -> bool:
        return len(request) > 0 and request[0].lower() in self.FriendlyNames and self.CanFitTo(len(request) - 1)

    async def _Execute(self, context: SuitContext, args):
        try:
            obj = self.GetInstance(context)
            if obj is not None:
                if args:
                    returnValue=self.Method(obj, *args)
                else:
                    returnValue=self.Method(obj)
            else:
                if args:
                    returnValue=self.Method(*args)
                else:
                    returnValue=self.Method()
            if inspect.isawaitable(returnValue):
                returnValue = await returnValue

            if isinstance(returnValue, RequestStatus):
                context.RequestStatus = returnValue
                context.Response = None
            else:
                context.RequestStatus = RequestStatus.Handled
                context.Response = str(
                    returnValue) if returnValue is not None else None
        except Exception as ex:
            context.RequestStatus = RequestStatus.Faulted
            raise ex

    def CanFitTo(self, argumentCount: int) -> bool:
        return self._suitMethodParameterInfo.MinParameterCount <= argumentCount <= self._suitMethodParameterInfo.MaxParameterCount

    async def Execute(self, context: SuitContext):
        if self._suitMethodParameterInfo.TailParameterType == TailParameterType.NoParameter:
            await self._Execute(context, None)
            return

        args = context.Request[1:]
        try:
            pass_ = SuitBuildUtils.GetArgsInternal(
                self.Method, self._suitMethodParameterInfo, args, context)
            if pass_ is None:
                return
            await self._Execute(context, pass_)
        except ValueError:
            pass
