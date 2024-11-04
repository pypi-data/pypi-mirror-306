import gaiaengine as gaia

import weakref


class Callback(gaia.Callback_):
    def __init__(self, callbackFunction):
        try:
            return super().__init__(weakref.WeakMethod(callbackFunction), True)
        except:
            return super().__init__(callbackFunction, type(callbackFunction) == weakref.WeakMethod)