#include "ImpostorSelector.h"

#include <glm/glm.hpp>
#include <glm/gtx/hash.hpp>

#include "HeightmapCamera.h"
#include "EventManager.h"
#include "Impostor.h"
#include "ImpostorManager.h"
#include "InGameText.h"
#include "MovingImpostor.h"
#include "UIManager.h"
#include "utils.h"
#include "Window.h"

#include <algorithm>
#include <unordered_map>

ImpostorSelector::ImpostorSelector(Window* window, std::shared_ptr<ImpostorManager> impostorManager, std::shared_ptr<UIManager> uiManager) :
  Component(window),
  _impostorManager(impostorManager),
  _rectSelectDisplay(glm::vec4(1), false)
{
  _inGameText = std::static_pointer_cast<InGameText>(uiManager->createElement(py::type::of<InGameText>()));
}

void ImpostorSelector::updateVisuals(int /*msElapsed*/, const Camera* camera) {
  computeImpostor2DCorners(camera);

  if (_displaySelectionRectangle)
    updateRectSelectDisplay(camera);

  cleanUpSelection();
}

void ImpostorSelector::render(const Camera* camera) const {
  // For each color, store the list of rectangles that will fill the gauge
  std::unordered_map<glm::vec4, std::vector<glm::ivec4>> gaugesOfColor;
  std::vector<glm::ivec4> outlinesRects;
  std::vector<glm::ivec4> selectableRectangles;

  _inGameText->clearText();
  float DPIZoom = getWindow()->getDPIZoom();
  int scaledGaugeWidth = (int)(_gaugeSize.x * DPIZoom + 0.5f);
  int scaledGaugeHeight = (int)(_gaugeSize.y * DPIZoom + 0.5f);

  for (std::weak_ptr<Impostor> weakImpostor : _selection) {
    // Just checking for still being valid as the selection has already been cleaned up in updateVisuals
    // Can't be done here as it's a non-const function
    if (std::shared_ptr<Impostor> impostor = weakImpostor.lock()) {
      glm::ivec2 impostorTopCenter = impostor->getScreenTopCenter();

      if (impostor->getShouldDisplayGauge()) {
        glm::ivec4 fillingRectangle(
          impostorTopCenter.x - scaledGaugeWidth / 2.f,
          impostorTopCenter.y - scaledGaugeWidth / 4.f,
          scaledGaugeWidth * impostor->getDisplayablePercentageValue() / 100.f,
          scaledGaugeHeight
        );

        gaugesOfColor[impostor->getDisplayableValueColor()].push_back(fillingRectangle);

        outlinesRects.push_back(glm::ivec4(
          impostorTopCenter.x - scaledGaugeWidth / 2.f,
          impostorTopCenter.y - scaledGaugeWidth / 4.f,
          scaledGaugeWidth,
          scaledGaugeHeight
        ));

        impostorTopCenter.y += scaledGaugeHeight;
      }

      if (!impostor->getDisplayableText().empty())
        _inGameText->pushText(TextElement{impostor->getDisplayableText(), impostorTopCenter, glm::vec2(0.5f, 1.f)});

      if (_displayImpostorSelectionHitboxes)
        selectableRectangles.push_back(impostor->getScreenRect());
    }
  }

  if (_displayImpostorSelectionHitboxes) {
    ColoredRectangles selectableRectanglesRenderer(glm::vec4(0, 0, 1, 1), selectableRectangles, camera->getViewportSize(), false);
    selectableRectanglesRenderer.render();
  }

  for (auto& gaugeRectangles : gaugesOfColor) {
    ColoredRectangles gaugeDisplay(gaugeRectangles.first, gaugeRectangles.second, camera->getViewportSize());
    gaugeDisplay.render();
  }
  
  ColoredRectangles outlines(glm::vec4(0, 0, 0, 1), outlinesRects, camera->getViewportSize(), false);
  outlines.render();

  if (_displaySelectionRectangle)
    _rectSelectDisplay.render();
}

void ImpostorSelector::updateRectSelectDisplay(const Camera* camera) {
  glm::ivec4 absoluteRect;
  if (_selectionRectangle.z > 0) {
    absoluteRect.x = _selectionRectangle.x;
    absoluteRect.z = _selectionRectangle.z;
  }
  else {
    absoluteRect.x = _selectionRectangle.x + _selectionRectangle.z;
    absoluteRect.z = -_selectionRectangle.z;
  }

  if (_selectionRectangle.w > 0) {
    absoluteRect.y = _selectionRectangle.y;
    absoluteRect.w = _selectionRectangle.w;
  }
  else {
    absoluteRect.y = _selectionRectangle.y + _selectionRectangle.w;
    absoluteRect.w = -_selectionRectangle.w;
  }

  _rectSelectDisplay.setRectangles(absoluteRect, camera->getViewportSize());
}

std::shared_ptr<Impostor> ImpostorSelector::getSelectableImpostor(glm::ivec2 screenTarget) const {
  std::vector<std::shared_ptr<Impostor>> selectableImpostors = _impostorManager->getElementsByFilter(
    [this, screenTarget](const std::shared_ptr<Impostor> impostor) { 
      return impostor->canBeSelected() && ut::getRectanglesIntersect(impostor->getScreenRect(), glm::ivec4(screenTarget, 0, 0)); }
  );

  if (selectableImpostors.size() == 0)
    return nullptr;

  std::sort(selectableImpostors.begin(), selectableImpostors.end(),
    [](const std::shared_ptr<Impostor> a, const std::shared_ptr<Impostor> b) {
      return a->getScreenDepth() < b->getScreenDepth();
    });

  return selectableImpostors[0];
}

void ImpostorSelector::select(const glm::ivec4& encompassingRectangle, bool add, const std::function<bool(const std::shared_ptr<Impostor>)>& filter) {
  if (!add)
    _selection.clear();

  std::vector<std::shared_ptr<Impostor>> selectableImpostors = _impostorManager->getElementsByFilter(
    [filter](const std::shared_ptr<Impostor> impostor) { return impostor->canBeSelected() && filter(impostor); }
  );

  std::vector<std::shared_ptr<Impostor>> selection = getSelection();

  for (std::shared_ptr<Impostor> impostor : selectableImpostors) {
    if (std::find(selection.begin(), selection.end(), impostor) == selection.end()) {
      if (ut::getRectanglesIntersect(encompassingRectangle, impostor->getScreenRect())) {
        _selection.push_back(impostor);
      }
    }
  }
}

void ImpostorSelector::deleteOneInSelection() {
  cleanUpSelection();
  if (_selection.size() > 0)
    _selection[0].lock()->deleteElement();
}

void ImpostorSelector::goBackToSelection(HeightmapCamera* camera) {
  std::vector<std::shared_ptr<Impostor>> selection = getSelection();
  
  if (!selection.empty()) {
    glm::vec2 barycenter(0);
    float nbSelected = 0;

    for (std::shared_ptr<Impostor> element : selection) {
      barycenter += element->getPosition();
      nbSelected++;
    }

    camera->setAim2DPosition(barycenter / nbSelected);
  }
}

void ImpostorSelector::moveSelection(const glm::vec2& target) {
  for (std::shared_ptr<Impostor> element: getSelection()) {
    if (MovingImpostor* movingElement = dynamic_cast<MovingImpostor*>(element.get())) {
      movingElement->setTarget(target);
    }
  }
}

std::vector<std::shared_ptr<Impostor>> ImpostorSelector::getSelection() {
  cleanUpSelection();

  std::vector<std::shared_ptr<Impostor>> strongSelection;

  for (std::weak_ptr<Impostor> weakElement : _selection) {
    strongSelection.push_back(weakElement.lock());
  }

  return strongSelection;
}

void ImpostorSelector::cleanUpSelection() {
  std::erase_if(_selection, [](std::weak_ptr<Impostor>& impostor) { 
    return impostor.expired() || !impostor.lock()->canBeSelected();
  });
}

void ImpostorSelector::computeImpostor2DCorners(const Camera* camera) {
  glm::mat4 rotateImpostors = _impostorManager->getModelMatrix(camera);

  for (auto impostor : _impostorManager->getElements()) {
    glm::vec3 pos;
    pos.x = impostor->getPosition().x;
    pos.y = impostor->getPosition().y;
    pos.z = impostor->getHeight();

    std::array<float, 12> vertices;

    if (impostor->canBeSelected() && glm::length(pos - camera->getCurrentPosition()) > _impostorManager->getImpostorNearPlane()) {
      // Calculate new corners
      glm::vec3 corners3[4];
      const std::array<float, 12>& vert = impostor->getVertices();

      corners3[0] = glm::vec3(vert[0], vert[1], vert[2]);
      corners3[1] = glm::vec3(vert[3], vert[4], vert[5]);
      corners3[2] = glm::vec3(vert[6], vert[7], vert[8]);
      corners3[3] = glm::vec3(vert[9], vert[10], vert[11]);

      glm::vec3 translatePosition(impostor->getPosition().x,
        impostor->getPosition().y,
        impostor->getHeight());

      glm::mat4 model = glm::translate(glm::mat4(1.f), translatePosition) * rotateImpostors;

      // Compute their projections
      for (int i = 0; i < 4; i++) {
        glm::vec4 tmp(corners3[i], 1.f);
        tmp = model * tmp;
        tmp = camera->getViewProjectionMatrix() * tmp;
        corners3[i] = glm::vec3(tmp) / tmp.w;
      }

      for (int i = 0; i < 4; i++) {
        vertices[3 * i] = corners3[i].x;
        vertices[3 * i + 1] = corners3[i].y;
        vertices[3 * i + 2] = corners3[i].z;
      }
    }

    else {
      for (int i = 0; i < 12; i++) {
        vertices[i] = 0;
      }
    }

    impostor->setProjectedVertices(vertices);
  }
}

#include <pybind11/functional.h>
#include <pybind11/stl.h>

void ImpostorSelector::pythonBindings(py::module& m) {
  py::class_<ImpostorSelector, std::shared_ptr<ImpostorSelector>, Component>(m, "ImpostorSelector")
    .def(py::init<Window*, std::shared_ptr<ImpostorManager>, std::shared_ptr<UIManager>>())
    .def("getSelectableImpostor", &ImpostorSelector::getSelectableImpostor)
    .def("select", py::overload_cast<const glm::ivec4&, bool>(&ImpostorSelector::select))
    .def("select", py::overload_cast<const glm::ivec4&, bool, const std::function<bool(const std::shared_ptr<Impostor>)> &>(& ImpostorSelector::select))
    .def("clearSelection", &ImpostorSelector::clearSelection)
    .def("isSelectionEmpty", &ImpostorSelector::isSelectionEmpty)
    .def("addToSelection", &ImpostorSelector::addToSelection)
    .def("removeFromSelection", &ImpostorSelector::removeFromSelection)
    .def("deleteOneInSelection", &ImpostorSelector::deleteOneInSelection)
    .def("goBackToSelection", &ImpostorSelector::goBackToSelection)
    .def("moveSelection", &ImpostorSelector::moveSelection)
    .def_property_readonly("selection", &ImpostorSelector::getSelection)
    .def_readwrite("selectionRectangle", &ImpostorSelector::_selectionRectangle)
    .def_readwrite("gaugeSize", &ImpostorSelector::_gaugeSize)
    .def_readwrite("displaySelectionRectangle", &ImpostorSelector::_displaySelectionRectangle)
    .def_readwrite("displayImpostorSelectionHitboxes", &ImpostorSelector::_displayImpostorSelectionHitboxes);
}