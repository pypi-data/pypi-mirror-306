#include "Impostor.h"

#include "ImpostorAsset.h"
#include "ImpostorManager.h"
#include "TextureArray.h"
#include "Window.h"

#include <cmath>

Impostor::Impostor(ImpostorManager* impostorManager, std::shared_ptr<const ImpostorAsset> impostorAsset, glm::vec2 position) :
  ManagedElement(impostorManager),
  _impostorAsset(impostorAsset),
  _sizeFactor(impostorManager->getBaseImpostorSizeFactor())
{
  setPosition(position);

  setCurrentTexture(0);
  setCurrentSprite(rand() % _impostorAsset->getSpriteInfo()[0].size());
}

void Impostor::setPosition(const glm::vec2& val) {
  _position = val;
  setHeight(getImpostorManager()->getHeight(_position));
}

ImpostorManager* Impostor::getImpostorManager() const {
  return static_cast<ImpostorManager*>(getManager());
}

Window* Impostor::getWindow() const {
  return getImpostorManager()->getWindow();
}

std::vector<std::shared_ptr<Impostor>> Impostor::getVisibleImpostors() const {
  return getImpostorManager()->getVisibleImpostors(_position, _type, _lineOfSight);
}

const TextureArray* Impostor::getTextureArray() const {
  return _impostorAsset->getTextureArray();
}

glm::ivec4 Impostor::getScreenRect() const {
  glm::ivec2 screenSize = getWindow()->getWindowSize();
  glm::ivec4 res;
  res.x = (int) ( (_projectedVertices[3] + 1.f) / 2.f * screenSize.x);
  res.y = (int) (-(_projectedVertices[1] + 1.f) / 2.f * screenSize.y + screenSize.y);
  res.z = (int) ( (_projectedVertices[0] - _projectedVertices[3]) / 2.f * screenSize.x);
  res.w = (int) ( (_projectedVertices[1] - _projectedVertices[7]) / 2.f * screenSize.y);

  return res;
}

glm::ivec2 Impostor::getScreenTopCenter() const {
  glm::ivec4 corners = getScreenRect();
  const SpriteInfo& currentSprite = _impostorAsset->getCurrentSpriteInfo(getCurrentTexture(), getCurrentSprite());
  
  return glm::ivec2(corners.x + std::round(currentSprite.anchor_x * std::abs(corners.z) / (float)std::abs(currentSprite.w)),
                    corners.y + std::round((currentSprite.anchor_y - _impostorAsset->getMaxAnchorHeight()) * std::abs(corners.w) / (float)std::abs(currentSprite.h)));
}

void Impostor::setType(int val) {
  _type = val;
  _lineOfSight = getImpostorManager()->getBaseLineOfSight(_type);
}

void Impostor::setPositionArray() {
  for (int i = 0; i < 4; i++) {
    _posArray[3*i]     = _position.x;
    _posArray[3*i + 1] = _position.y;
    _posArray[3*i + 2] = _height;
  }
}

void Impostor::setCurrentSprite(int sprite) {
  _currentSprite = sprite;

  glm::vec4 rect = _impostorAsset->getTexRectangle(getCurrentTexture(), sprite);

  _coord2D[0] = rect.x + rect.z;
  _coord2D[1] = rect.y;
  _coord2D[2] = rect.x;
  _coord2D[3] = rect.y;
  _coord2D[4] = rect.x;
  _coord2D[5] = rect.y + rect.w;
  _coord2D[6] = rect.x + rect.z;
  _coord2D[7] = rect.y + rect.w;

  const SpriteInfo& currentSprite = _impostorAsset->getCurrentSpriteInfo(getCurrentTexture(), getCurrentSprite());
  glm::vec2 size = glm::vec2(std::abs(currentSprite.w), std::abs(currentSprite.h)) * _sizeFactor;

  // The anchor is based on the top left corner of the texture, while we're drawing from the bottom left
  glm::vec2 offset = glm::vec2(-currentSprite.anchor_x, currentSprite.anchor_y - std::abs(currentSprite.h)) * _sizeFactor;

  _vertices[0] = 0; _vertices[1] =  offset.x + size.x; _vertices[2] =  offset.y + size.y;
  _vertices[3] = 0; _vertices[4] =  offset.x;          _vertices[5] =  offset.y + size.y;
  _vertices[6] = 0; _vertices[7] =  offset.x;          _vertices[8] =  offset.y;
  _vertices[9] = 0; _vertices[10] = offset.x + size.x; _vertices[11] = offset.y;
}

void Impostor::setCurrentTexture(int texture) {
  for (int i = 0; i < 4; i++) {
    _layer[i] = (float)texture;
  }
}

int Impostor::getNumSprites() const {
  return (int)_impostorAsset->getSpriteInfo()[getCurrentTexture()].size();
}

int Impostor::getNumTextures() const {
  return getTextureArray()->getCount();
}

#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

PYBIND11_MAKE_OPAQUE(std::vector<Impostor*>)

void Impostor::pythonBindings(py::module& m) {
  py::class_<Impostor, std::shared_ptr<Impostor>>(m, "Impostor")
    .def(py::init<ImpostorManager*, std::shared_ptr<const ImpostorAsset>, glm::vec2>())
    .def_property_readonly("impostorManager", &Impostor::getImpostorManager)
    .def_property_readonly("window", &Impostor::getWindow)
    .def_property_readonly("asset", &Impostor::getImpostorAsset)
    .def_property_readonly("screenRect", &Impostor::getScreenRect)
    .def_property("currentSprite", &Impostor::getCurrentSprite, &Impostor::setCurrentSprite)
    .def_property("currentTexture", &Impostor::getCurrentTexture, &Impostor::setCurrentTexture)
    .def_property_readonly("numSprites", &Impostor::getNumSprites)
    .def_property_readonly("numTextures", &Impostor::getNumTextures)
    .def_property("position", &Impostor::getPosition, &Impostor::setPosition)
    .def_property("sizeFactor", &Impostor::getSizeFactor, &Impostor::setSizeFactor)
    .def_property("type", &Impostor::getType, &Impostor::setType)
    .def_property("lineOfSight", &Impostor::getLineOfSight, &Impostor::setLineOfSight)
    .def("getVisibleImpostors", &Impostor::getVisibleImpostors)

    // Properties that are used by the selector component (might need a refactor?)
    .def_readwrite("canBeSelected", &Impostor::_canBeSelected)
    .def_readwrite("displayablePercentageValue", &Impostor::_displayablePercentageValue)
    .def_readwrite("displayableValueColor", &Impostor::_displayableValueColor)
    .def_readwrite("shouldDisplayGauge", &Impostor::_shouldDisplayGauge)
    .def_readwrite("displayableText", &Impostor::_displayableText)
    .def("delete", &ManagedElement<Impostor>::deleteElement)
    .def("isDeleted", &ManagedElement<Impostor>::isElementDeleted);

  py::bind_vector<std::vector<Impostor*>>(m, "ImpostorVector");
}