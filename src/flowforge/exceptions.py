class FlowForgeError(Exception): pass
class AuthenticationError(FlowForgeError): pass
class NotFoundError(FlowForgeError): pass
class RateLimitError(FlowForgeError): pass
class ValidationError(FlowForgeError): pass
