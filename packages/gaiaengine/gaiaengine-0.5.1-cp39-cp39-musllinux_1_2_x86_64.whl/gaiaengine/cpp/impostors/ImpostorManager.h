#pragma once

#include <glm/glm.hpp>
#include <glm/gtx/hash.hpp>

#include "Component.h"
#include "ImpostorRenderer.h"
#include "Manager.h"
#include "Shader.h"

#include <list>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

class Camera;
class Impostor;
class MovingImpostor;
class Terrain;
class TextureArray;

typedef std::unordered_map < glm::ivec2, std::list < std::shared_ptr< Impostor> > > Grid;

typedef struct ImpostorSpatialOrder {
  // Saved as base characteristics of impostor types
  std::vector<int> visibleTypes;

  // Re-built every frame to make queries of surrounding impostors faster
  float maxLineOfSight = 0.f;
  float baseLineOfSight = 0.f;
  Grid grid;
} ImpostorSpatialOrder;

class ImpostorManager: public Component, public Manager<Impostor> {
public:
  ImpostorManager(Window* window, std::shared_ptr<Terrain> terrain);
  
  void update(int msElapsed) override;
  void updateVisuals(int msElapsed, const Camera* camera) override;
  void render(const Camera* camera) const override;

  glm::mat4 getModelMatrix(const Camera* camera) const;

  std::shared_ptr<Impostor> createElement(const py::object& myClass, const py::args& args = py::args()) override;

  float getHeight(const glm::vec2& pos) const;

  inline float getBaseImpostorSizeFactor() const { return _baseImpostorSizeFactor; }

  inline float getImpostorNearPlane() const { return _impostorNearPlane; }
  void setImpostorNearPlane(float val);

  inline bool getImpostorsCanWrapAroundWorld() const { return _impostorsCanWrapAroundWorld; }

  std::vector<std::shared_ptr<Impostor>> getVisibleImpostors(const glm::vec2& pos, int type, float lineOfSight) const;

  const std::vector<int>& getVisibleTypes(int typeWatching) const;
  float getBaseLineOfSight(int typeWatching) const;
  void setVisibleTypes(int typeWatching, const std::vector<int>& visibleTypes, float baseLineOfSight);

  static void pythonBindings(py::module& m);
private:
  std::unordered_map<int, ImpostorSpatialOrder> _impostorTypeToSpatialOrder;
  std::unordered_map<int, std::vector<int>> _typeVisibleFromTheseTypes;

  void updateSpatialOrders();
  void addImpostorToSpatialOrders(std::shared_ptr<Impostor> impostor);

  std::shared_ptr<Terrain> _terrain;
  Shader _impostorShader;
  float _baseImpostorSizeFactor = 1.f;
  float _impostorNearPlane = -1.f;
  bool _impostorsCanWrapAroundWorld = false;

  ImpostorRenderer _impostorRenderer;
};

