#pragma once

#include <pybind11/pybind11.h>

#include <functional>
#include <memory>
#include <vector>

namespace py = pybind11;

template <class T>
class Manager;

template <class T>
class ManagedElement {
public:
  void deleteElement();
  inline Manager<T>* getManager() const { return _manager; }
  inline bool isElementDeleted() const { return _isDeleted; }

protected:
  ManagedElement(Manager<T>* manager) : _manager(manager) {}

private:
  friend class Manager<T>;
  void setLocationInManager(size_t val) { _indexInManager = val; }
  void setIsPendingAdd(bool val) { _isPendingAdd = val; }

  Manager<T>* _manager = nullptr;
  size_t _indexInManager = 0;
  bool _isPendingAdd = true;
  bool _isDeleted = false;
};

template <class T>
class Manager {
public:
  Manager() = default;
  virtual ~Manager() = default;

  // Doesn't add the new element directly to the main array of elements (see processElementsPendingUpdates),
  // so that if an element is created while iterating over the list, it won't invalidate the iterators
  virtual std::shared_ptr<T> createElement(const py::object& myClass, const py::args& args = py::args());

  // Guaranteed to return valid elements
  virtual std::vector<std::shared_ptr<T>> getElements() { processElementsPendingUpdates(); return _managedElements; }
  virtual std::vector<std::shared_ptr<T>> getElementsByFilter(const std::function<bool(const std::shared_ptr<T>)>& filter);

private:
  // Adds pending elements and remove invalid ones
  void processElementsPendingUpdates();

  friend class ManagedElement<T>;
  void deleteElement(size_t index, bool isPendingAdd);

  std::vector<std::shared_ptr<T>> _managedElements;
  std::vector<std::shared_ptr<T>> _managedElementsPendingAdd;
  bool _managedElementsDirty = false;
  bool _managedElementsPendingAddDirty = false;
};

#include "Manager.ipp"
