#include "ImpostorManager.h"

#include <glm/gtx/vector_angle.hpp>

#include "ImpostorAsset.h"
#include "Camera.h"
#include "MovingImpostor.h"
#include "Terrain.h"
#include "Window.h"

#include <algorithm>
#include <sstream>

ImpostorManager::ImpostorManager(Window* window, std::shared_ptr<Terrain> terrain) :
  Component(window),
  _terrain(terrain),
  _impostorShader("impostor.vert", "impostor.frag")
{
  setImpostorNearPlane(2.f);
}

void ImpostorManager::setImpostorNearPlane(float val) {
  _impostorNearPlane = val;
  SCOPE_BIND(_impostorShader)
  glUniform1f(_impostorShader.getUniformLocation("elementNearPlane"), getImpostorNearPlane());
}

void ImpostorManager::update(int msElapsed) {
  for (auto& impostor: getElements()) {
    impostor->update(msElapsed, _terrain.get());
  }

  updateSpatialOrders();
}

void ImpostorManager::updateVisuals(int msElapsed, const Camera* camera) {
  float cameraAngleWithXAxis = glm::degrees(glm::orientedAngle(
    glm::vec2(1.f, 0.f),
    glm::normalize(- glm::vec2(camera->getCurrentDirection().x, camera->getCurrentDirection().y))
  ));

  for (auto& impostor: getElements()) {
    impostor->updateDisplay(msElapsed, cameraAngleWithXAxis);
  }

  _impostorRenderer.loadImpostors(getElements());
}

void ImpostorManager::render(const Camera* camera) const {
  glm::mat4 MVP = camera->getViewProjectionMatrix();

  glm::mat4 rotateImpostors = getModelMatrix(camera);

  SCOPE_BIND(_impostorShader)
  glUniformMatrix4fv(_impostorShader.getUniformLocation("VP"),
    1, GL_FALSE, &MVP[0][0]);
  glUniformMatrix4fv(_impostorShader.getUniformLocation("MODEL"),
    1, GL_FALSE, &rotateImpostors[0][0]);
  glUniform3fv(_impostorShader.getUniformLocation("camPos"),
    1, &camera->getCurrentPosition()[0]);

  // Two passes to avoid artifacts due to alpha blending

  glUniform1i(_impostorShader.getUniformLocation("onlyOpaqueParts"), true);
  _impostorRenderer.renderImpostors();

  glUniform1i(_impostorShader.getUniformLocation("onlyOpaqueParts"), false);

  glEnable(GL_BLEND);
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

  _impostorRenderer.renderImpostors();

  glDisable(GL_BLEND);
}

glm::mat4 ImpostorManager::getModelMatrix(const Camera* camera) const {
  glm::vec3 toCamera = -camera->getCurrentDirection();

  glm::mat4 rotateImpostors = glm::rotate(glm::mat4(1.f),
    glm::orientedAngle(glm::vec2(1.f, 0.f), glm::normalize(glm::vec2(toCamera.x, toCamera.y))),
    glm::vec3(0, 0, 1));

  // - pi/2 to make the face rather than the edge face the camera
  // We divide by 2 afterwards to have the rotation from the center of the impostor rather than the bottom
  rotateImpostors = glm::rotate(rotateImpostors,
    (glm::angle(glm::vec3(0.f, 0.f, 1.f), toCamera) - (float)M_PI / 2.f) / 2.f,
    glm::vec3(0, 1, 0));

  return rotateImpostors;
}

std::shared_ptr<Impostor> ImpostorManager::createElement(const py::object& myClass, const py::args& args /*= py::args()*/) {
  ImpostorAsset* impostorAsset = args[0].cast<ImpostorAsset*>();

  if (impostorAsset == nullptr)
    throw std::invalid_argument("Invalid ImpostorAsset object");

  if (!impostorAsset->isLoaded())
    impostorAsset->load();

  std::shared_ptr<Impostor> newImpostor = Manager<Impostor>::createElement(myClass, args);

  // If the new impostor has a bigger line of sight than the one that has been used to compute the spatial orders,
  // we need to recompute all of them
  if (getVisibleTypes(newImpostor->getType()).size() > 0) {
    if (newImpostor->getLineOfSight() > _impostorTypeToSpatialOrder[newImpostor->getType()].maxLineOfSight) {
      updateSpatialOrders();
      return newImpostor;
    }
  }

  // Otherwise just add it to the existing spatial orders
  addImpostorToSpatialOrders(newImpostor);
  return newImpostor;
}

float ImpostorManager::getHeight(const glm::vec2& pos) const {
  return _terrain->getHeight(pos);
}

std::vector<std::shared_ptr<Impostor>> ImpostorManager::getVisibleImpostors(const glm::vec2& pos, int type, float lineOfSight) const {
  const ImpostorSpatialOrder* spatialOrder = nullptr;
  try {
    spatialOrder = &_impostorTypeToSpatialOrder.at(type);
  }
  catch (const std::out_of_range&) {
    throw std::out_of_range(std::string("No visible types set for type ") + std::to_string(type));
  }

  glm::vec2 cellSize = glm::vec2(spatialOrder->maxLineOfSight);
  glm::ivec2 nbCells = glm::ivec2(_terrain->getMaxCoordinates() / cellSize) + glm::ivec2(1); // +1 for border cells

  std::vector<std::shared_ptr<Impostor>> visibleImpostors;

  glm::ivec2 currentCell = pos / cellSize;
  float lineOfSightSquared = lineOfSight * lineOfSight;

  for (int i = std::max(0, currentCell.x - 1); i <= std::min(nbCells.x - 1, currentCell.x + 1); i++) {
    for (int j = std::max(0, currentCell.y - 1); j <= std::min(nbCells.y - 1, currentCell.y + 1); j++) {
      glm::ivec2 cellCoords(i, j);

      const auto& impostorsInCell = spatialOrder->grid.find(cellCoords);
      if (impostorsInCell != spatialOrder->grid.end()) {
        auto isImpostorVisible = [pos, lineOfSightSquared](std::shared_ptr<Impostor> impostor) {
          return glm::distance2(pos, impostor->getPosition()) <= lineOfSightSquared;
        };
        
        std::copy_if(impostorsInCell->second.begin(), impostorsInCell->second.end(), std::back_inserter(visibleImpostors), isImpostorVisible);
      }
    }
  }

  return visibleImpostors;
}

const std::vector<int>& ImpostorManager::getVisibleTypes(int typeWatching) const {
  static const std::vector<int> defaultEmptyVector;
  const auto& spatialOrderPair = _impostorTypeToSpatialOrder.find(typeWatching);
 
  if (spatialOrderPair == _impostorTypeToSpatialOrder.end())
    return defaultEmptyVector;

  return spatialOrderPair->second.visibleTypes;
}

float ImpostorManager::getBaseLineOfSight(int typeWatching) const {
  const auto& spatialOrderPair = _impostorTypeToSpatialOrder.find(typeWatching);

  if (spatialOrderPair == _impostorTypeToSpatialOrder.end())
    return 0.f;

  return spatialOrderPair->second.baseLineOfSight;
}

void ImpostorManager::setVisibleTypes(int typeWatching, const std::vector<int>& visibleTypes, float baseLineOfSight) {
  _impostorTypeToSpatialOrder[typeWatching].visibleTypes = visibleTypes;
  _impostorTypeToSpatialOrder[typeWatching].baseLineOfSight = baseLineOfSight;

  if (baseLineOfSight > _impostorTypeToSpatialOrder[typeWatching].maxLineOfSight)
    _impostorTypeToSpatialOrder[typeWatching].maxLineOfSight = baseLineOfSight;

  updateSpatialOrders();
}

void ImpostorManager::updateSpatialOrders() {
  // Updating line of sight values
  for (auto& spatialOrderPair : _impostorTypeToSpatialOrder) {
    spatialOrderPair.second.maxLineOfSight = 0.f;
  }

  for (auto& impostor : getElements()) {
    if (getVisibleTypes(impostor->getType()).size() > 0)
      if (impostor->getLineOfSight() > _impostorTypeToSpatialOrder[impostor->getType()].maxLineOfSight)
        _impostorTypeToSpatialOrder.at(impostor->getType()).maxLineOfSight = impostor->getLineOfSight();
  }

  // Updating which type is visible from which
  _typeVisibleFromTheseTypes.clear();

  for (auto& spatialOrderPair : _impostorTypeToSpatialOrder) {
    spatialOrderPair.second.grid.clear();
    if (spatialOrderPair.second.maxLineOfSight > 0.f) {
      for (int visibleType : spatialOrderPair.second.visibleTypes) {
        _typeVisibleFromTheseTypes[visibleType].push_back(spatialOrderPair.first);
      }
    }
  }

  // Actually sorting the impostors
  for (auto& impostor : getElements()) {
    addImpostorToSpatialOrders(impostor);
  }
}

void ImpostorManager::addImpostorToSpatialOrders(std::shared_ptr<Impostor> impostor) {
  const auto& visibleFromTheseTypes = _typeVisibleFromTheseTypes.find(impostor->getType());
  if (visibleFromTheseTypes != _typeVisibleFromTheseTypes.end()) {
    for (int typeWatching : visibleFromTheseTypes->second) {
      glm::ivec2 cell = glm::ivec2(impostor->getPosition() / glm::vec2(_impostorTypeToSpatialOrder.at(typeWatching).maxLineOfSight));
      _impostorTypeToSpatialOrder.at(typeWatching).grid[cell].push_back(impostor);
    }
  }
}

#include <pybind11/functional.h>
#include <pybind11/stl.h>

void ImpostorManager::pythonBindings(py::module& m) {
  py::class_<ImpostorManager, std::shared_ptr<ImpostorManager>, Component>(m, "ImpostorManager")
    .def(py::init<Window*, std::shared_ptr<Terrain>>())
    .def("create", &ImpostorManager::createElement)
    .def("getImpostors", &ImpostorManager::getElements)
    .def("getImpostorsByFilter", &ImpostorManager::getElementsByFilter)
    .def("getVisibleImpostors", &ImpostorManager::getVisibleImpostors)
    .def("getVisibleTypes", &ImpostorManager::getVisibleTypes)
    .def("setVisibleTypes", &ImpostorManager::setVisibleTypes)
    .def_readwrite("terrain", &ImpostorManager::_terrain)
    .def_readwrite("baseImpostorSizeFactor", &ImpostorManager::_baseImpostorSizeFactor)
    .def_readwrite("impostorsCanWrapAroundWorld", &ImpostorManager::_impostorsCanWrapAroundWorld);
}
