#include "EventListener.h"

#include "EventManager.h"
#include "Window.h"

EventListener::EventListener(EventManager* eventManager) : ManagedElement(eventManager) {}

EventManager* EventListener::getEventManager() const {
  return static_cast<EventManager*>(getManager());
}

Window* EventListener::getWindow() const {
  return getEventManager()->getWindow();
}

class PyEventListener : public EventListener {
public:
  using EventListener::EventListener;

  bool handleEvent(Window* window, SDL_Event& sdl_event) override {
    PYBIND11_OVERRIDE_NAME(bool, EventListener, "handleEvent_", handleEvent, window, sdl_event);
  }
};

void EventListener::pythonBindings(py::module& m) {
  // Exposing SDL_Event as a buffer so that it can be used as a sdl2.SDL_Event in python (from pysdl2)
  py::class_<SDL_Event>(m, "SDL_Event", py::buffer_protocol())
    .def_buffer([](SDL_Event& event) -> py::buffer_info {
    return py::buffer_info(
      (Uint8*)&event,
      sizeof(Uint8),
      py::format_descriptor<Uint8>::format(),
      1,
      { 56 },
      { sizeof(Uint8) }
    );
  });

  py::class_<EventListener, std::shared_ptr<EventListener>, PyEventListener>(m, "EventListener_")
    .def(py::init<EventManager*>())
    .def_property("active", &EventListener::isActive, &EventListener::setActive)
    .def_property_readonly("eventManager", &EventListener::getEventManager)
    .def_property_readonly("window", &EventListener::getWindow)
    .def_readonly("onSetActive", &EventListener::_onSetActive);
}