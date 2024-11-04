#pragma once

template <class T>
void ManagedElement<T>::deleteElement() {
  if (!isElementDeleted()) {
    _manager->deleteElement(_indexInManager, _isPendingAdd);
    _isDeleted = true;
  }
}

template <class T>
std::shared_ptr<T> Manager<T>::createElement(const py::object& myClass, const py::args& args /*= py::args()*/) {
  std::shared_ptr<py::object> pyElement = std::make_shared<py::object>(myClass(*(py::make_tuple(this) + args)));

  // pybind11's cast operator doesn't transfer the ownership of the python object handler, so we have to use the aliasing constructor to take care of it
  // https://github.com/pybind/pybind11/issues/1120
  std::shared_ptr<T> newElement(pyElement, pyElement->cast<T*>());

  newElement->setLocationInManager(_managedElementsPendingAdd.size());
  _managedElementsPendingAdd.push_back(newElement);

  return newElement;
}

template <class T>
std::vector<std::shared_ptr<T>> Manager<T>::getElementsByFilter(const std::function<bool(const std::shared_ptr<T>)>& filter) {
  std::vector<std::shared_ptr<T>> result;

  processElementsPendingUpdates();

  for (auto& element : _managedElements) {
    if (filter(element)) {
      result.push_back(element);
    }
  }

  return result;
}

template <class T>
void Manager<T>::deleteElement(size_t index, bool isPendingAdd) {
  if (isPendingAdd) {
    _managedElementsPendingAdd[index].reset();
    _managedElementsPendingAddDirty = true;
  }
  else {
    _managedElements[index].reset();
    _managedElementsDirty = true;
  }
}

template <class T>
void Manager<T>::processElementsPendingUpdates() {
  if (_managedElementsDirty) {
    int lastCleanIndex = 0;
    for (int i = 0; i < _managedElements.size(); i++) {
      if (_managedElements[i].get()) {
        _managedElements[lastCleanIndex] = _managedElements[i];
        _managedElements[lastCleanIndex]->setLocationInManager(lastCleanIndex);
        lastCleanIndex++;
      }
    }
    _managedElements.resize(lastCleanIndex);
    _managedElementsDirty = false;
  }

  if (_managedElementsPendingAddDirty) {
    int lastCleanIndex = 0;
    for (int i = 0; i < _managedElementsPendingAdd.size(); i++) {
      if (_managedElementsPendingAdd[i].get()) {
        _managedElementsPendingAdd[lastCleanIndex] = _managedElementsPendingAdd[i];
        _managedElementsPendingAdd[lastCleanIndex]->setLocationInManager(lastCleanIndex);
        lastCleanIndex++;
      }
    }
    _managedElementsPendingAdd.resize(lastCleanIndex);
    _managedElementsPendingAddDirty = false;
  }

  // Adding the pending elements to the main array and updating their indices
  size_t managedElementsPreviousSize = _managedElements.size();
  _managedElements.resize(managedElementsPreviousSize + _managedElementsPendingAdd.size());

  for (int i = 0; i < _managedElementsPendingAdd.size(); i++) {
    _managedElementsPendingAdd[i]->setLocationInManager(managedElementsPreviousSize + i);
    _managedElementsPendingAdd[i]->setIsPendingAdd(false);
    _managedElements[managedElementsPreviousSize + i] = _managedElementsPendingAdd[i];
  }
  _managedElementsPendingAdd.clear();
}

