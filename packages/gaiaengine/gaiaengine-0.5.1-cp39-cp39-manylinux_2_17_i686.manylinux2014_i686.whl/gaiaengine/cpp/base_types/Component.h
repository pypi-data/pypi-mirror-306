#pragma once

#include "Manager.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

class Camera;
class Window;

class Component : public ManagedElement<Component> {
public:
  Component(Window* window);
  virtual void update(int /*msElapsed*/) {}
  virtual void updateVisuals(int /*msElapsed*/, const Camera*) {}
  virtual void render(const Camera*) const {}

  Window* getWindow() const;

  static void pythonBindings(py::module& m);
};
