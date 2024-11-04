#pragma once

#include "Callback.h"
#include "Component.h"

#include <chrono>
#include <functional>
#include <list>
#include <map>
#include <memory>
#include <vector>

#include <pybind11/pybind11.h>

namespace py = pybind11;

class TimerManager;

class Timer : public std::enable_shared_from_this<Timer>{
public:
  Timer() = default;
  Timer(const Callback& callback, float tickRate, bool loop, bool absolute);

  inline int getTickRate() const { return _tickRateMs; }

  inline void cancel() { _active = false; }
  inline bool isActive() const { return _active; }
  void restart(TimerManager* timerManager);

  static void pythonBindings(py::module& m);
private:
  friend class TimerManager;

  void triggerCallback();

  Callback _callback;
  // A tick rate of 0 means that the timer gets called at each update step
  int _tickRateMs = -1;
  bool _loop = false;
  bool _absolute = false;
  bool _active = false;
};

class TimerManager : public Component {
public:
  TimerManager(Window* window);

  void update(int msElapsed) override;
  void updateVisuals(int msElapsed, const Camera* camera) override;

  // Regular timers are based on simulation time. They should be used for logic.
  inline std::shared_ptr<Timer> addTimer(const Callback& callback, float tickRate, bool loop) {
    return addTimer(std::make_shared<Timer>(callback, tickRate, loop, false));
  }

  // Absolute timers are based on real world time. They should be used for visuals and input.
  std::shared_ptr<Timer> addAbsoluteTimer(const Callback& callback, float tickRate, bool loop) {
    return addTimer(std::make_shared<Timer>(callback, tickRate, loop, true));
  }

  std::shared_ptr<Timer> addTimer(std::shared_ptr<Timer> timer);

  static void pythonBindings(py::module& m);
private:
  void updateInternal(std::list<std::shared_ptr<Timer>>& stepTimers, std::multimap<int, std::shared_ptr<Timer>>& activeTimers, int time);

  std::multimap<int, std::shared_ptr<Timer>> _activeTimers;
  std::list<std::shared_ptr<Timer>> _stepTimers;

  std::multimap<int, std::shared_ptr<Timer>> _activeAbsoluteTimers;
  std::list<std::shared_ptr<Timer>> _absoluteStepTimers;
};
