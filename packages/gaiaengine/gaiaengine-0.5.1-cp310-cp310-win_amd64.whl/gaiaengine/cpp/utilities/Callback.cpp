#include "Callback.h"

Callback::Callback(py::object callbackFunction, bool isWeakMethod) :
  _callbackFunction(callbackFunction),
  _isWeakMethod(isWeakMethod)
{
  if (callbackFunction.is_none())
    throw std::invalid_argument("Invalid callback function");
}

void Callback::operator()(py::args args) const {
  if (!isNone()) {
    if (_isWeakMethod)
      _callbackFunction()(*args);
    else
      _callbackFunction(*args);
  }
}

void Callback::pythonBindings(py::module& m) {
  py::class_<Callback, std::shared_ptr<Callback>>(m, "Callback_")
    .def(py::init<py::object, bool>());
}
