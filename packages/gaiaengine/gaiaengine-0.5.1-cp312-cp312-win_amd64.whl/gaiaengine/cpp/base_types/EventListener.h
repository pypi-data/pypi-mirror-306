#pragma once

#include <SDL.h>

#include "Delegate.h"
#include "Manager.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

class EventManager;
class Window;

class EventListener : public ManagedElement<EventListener> {
public:
  EventListener(EventManager* eventManager);

  // Returns whether the event should be consumed or not
  // Consuming an event prevents the rest of the EventListener stack from getting notified
  // Overridden in python to convert SDL_Event to the proper python container
  virtual bool handleEvent(Window*, SDL_Event&) { return false; }

  inline void setActive(bool isActive) { _active = isActive; _onSetActive.broadcast(); }
  inline bool isActive() const { return _active; }

  EventManager* getEventManager() const;
  Window* getWindow() const;

  static void pythonBindings(py::module& m);

private:
  bool _active = true;
  Delegate _onSetActive;
};

