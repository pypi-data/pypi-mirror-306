#include "Component.h"

#include "Window.h"

Component::Component(Window* window) : ManagedElement(window) {}

Window* Component::getWindow() const {
  return static_cast<Window*>(getManager());
}

void Component::pythonBindings(py::module& m) {
  py::class_<Component, std::shared_ptr<Component>>(m, "Component")
    .def_property_readonly("window", &Component::getWindow);
}
