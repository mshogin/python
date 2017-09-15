"""Common decorators."""


class autosetter_property(property):  # noqa
    """Property with autosetter.

    This property allows to not implement setter for the propery.
    Usage:
        class A:
            @autosetter_property
            def config(self):
                 return self._config

        ....
        a = A()
        config = {'t': 1}
        a.config = config
        assert a.config == config
    """
    class NotDefined:
        pass

    _not_defined = NotDefined()
    _var_prefix = "__auto_property__"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        super().__init__(fget, fset, fdel, doc)
        self._attr_name = self._var_prefix + fget.__name__
        if not hasattr(self, self._attr_name):
            setattr(self, self._attr_name, self._not_defined)
        if fset and hasattr(self, self._attr_name):
            delattr(self, self._attr_name)

    def __set__(self, instance, value):
        if getattr(self, 'fset'):
            self.fset(instance, value)
        setattr(self, self._attr_name, value)

    def __get__(self, instance, owner):
        value = getattr(self, self._attr_name, self._not_defined)
        if value is self._not_defined:
            return self.fget(instance)
        return value
