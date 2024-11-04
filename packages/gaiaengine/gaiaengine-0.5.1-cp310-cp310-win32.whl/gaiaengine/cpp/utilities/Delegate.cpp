#include "Delegate.h"

#include "utils.h"

#include <string>

void Delegate::bind(const Callback& callback) {
  if (!callback.isNone())
    _callbacks.push_back(callback);
}

void Delegate::unbind(const Callback& callback) {
  std::erase_if(_callbacks, [callback](const Callback& currentCallback) { return currentCallback.isNone() || callback == currentCallback; });
}

void Delegate::broadcast(py::args args) {
  for (int i = 0; i < _callbacks.size(); i++) {
    try {
      _callbacks[i](args);
    }
    catch (py::error_already_set& exception) {
      if (exception.matches(PyExc_TypeError))
        throw py::type_error(std::string("Invalid broadcast arguments when calling callback ") + ut::pyPrintToString(_callbacks[i]) + exception.what());
      else
        throw exception;
    }
  }
}

void Delegate::pythonBindings(py::module& m) {
  py::class_<Delegate, std::shared_ptr<Delegate>>(m, "Delegate")
    .def(py::init<>())
    .def("clear", &Delegate::clear)
    .def("bind", &Delegate::bind)
    .def("unbind", &Delegate::unbind)
    .def("broadcast", &Delegate::broadcast);
}
