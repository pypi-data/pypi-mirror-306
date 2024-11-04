#include "UIElement.h"

#include "UIManager.h"
#include "Window.h"

int UIElement::nextID = 0;

UIElement::UIElement(UIManager* uiManager):
  ManagedElement(uiManager),
  _ID(std::to_string(nextID))
{
  nextID++;
}

UIManager* UIElement::getUIManager() const {
  return static_cast<UIManager*>(getManager());
}

Window* UIElement::getWindow() const {
  return getUIManager()->getWindow();
}

class PyUIElement : public UIElement {
public:
  using UIElement::UIElement;

  void buildFrame() override {
    PYBIND11_OVERRIDE(void, UIElement, buildFrame, );
  }
};

void UIElement::pythonBindings(py::module& m) {
  py::class_<UIElement, std::shared_ptr<UIElement>, PyUIElement>(m, "UIElement")
    .def(py::init<UIManager*>())
    .def_property_readonly("id", &UIElement::getID)
    .def_property("enabled", &UIElement::isEnabled, &UIElement::setEnabled)
    .def_property("position", &UIElement::getPosition, &UIElement::setPosition)
    .def_property("pivot", &UIElement::getPivot, &UIElement::setPivot)
    .def_property_readonly("uiManager", &UIElement::getUIManager)
    .def_property_readonly("window", &UIElement::getWindow);
}
