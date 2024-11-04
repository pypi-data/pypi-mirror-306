#pragma once

#include "Callback.h"

#include <vector>

#include <pybind11/pybind11.h>

namespace py = pybind11;

class Delegate {
public:
  Delegate() {}

  inline void clear() { _callbacks.clear(); }

  void bind(const Callback& callback);
  void unbind(const Callback& callback);

  void broadcast(py::args args = py::args());

  static void pythonBindings(py::module& m);
private:
  std::vector<Callback> _callbacks;
};
