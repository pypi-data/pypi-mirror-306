import ctypes
import windows.generated_def as gdef
from windows.pycompat import int_types

from ..apiproxy import ApiProxy, NeededParameter
from ..error import succeed_on_zero, fail_on_zero

class ComputeCoreProxy(ApiProxy):
    APIDLL = "ComputeCore"
    default_error_check = staticmethod(succeed_on_zero)


@ComputeCoreProxy()
def HcsWaitForOperationResult(operation, timeoutMs, resultDocument):
    return HcsWaitForOperationResult.ctypes_function(operation, timeoutMs, resultDocument)

@ComputeCoreProxy(error_check=fail_on_zero)
def HcsCreateOperation(context, callback):
    return HcsCreateOperation.ctypes_function(context, callback)

@ComputeCoreProxy()
def HcsCloseOperation(operation):
    return HcsCloseOperation.ctypes_function(operation)

@ComputeCoreProxy()
def HcsGetOperationContext(operation):
    return HcsGetOperationContext.ctypes_function(operation)

@ComputeCoreProxy()
def HcsSetOperationContext(operation, context):
    return HcsSetOperationContext.ctypes_function(operation, context)

@ComputeCoreProxy()
def HcsGetOperationId(operation):
    return HcsGetOperationId.ctypes_function(operation)

@ComputeCoreProxy()
def HcsGetOperationResult(operation, resultDocument):
    return HcsGetOperationResult.ctypes_function(operation, resultDocument)

@ComputeCoreProxy()
def HcsCancelOperation(operation):
    return HcsCancelOperation.ctypes_function(operation)

@ComputeCoreProxy()
def HcsEnumerateComputeSystems(query, operation):
    return HcsEnumerateComputeSystems.ctypes_function(query, operation)