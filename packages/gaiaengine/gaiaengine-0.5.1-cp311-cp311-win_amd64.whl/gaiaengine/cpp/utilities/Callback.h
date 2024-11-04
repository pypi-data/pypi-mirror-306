#pragma once

#include <pybind11/pybind11.h>

namespace py = pybind11;

class Callback {
public:
  Callback() = default;
  Callback(py::object callbackFunction, bool isWeakMethod);

  inline bool isNone() const { return _callbackFunction.is_none() || (_isWeakMethod && _callbackFunction().is_none()); }

  bool operator==(const Callback& other) const { return _callbackFunction.equal(other._callbackFunction); }
  void operator()(py::args args = py::args()) const;

  static void pythonBindings(py::module& m);
private:
  py::object _callbackFunction = py::none();
  bool _isWeakMethod = false;
};