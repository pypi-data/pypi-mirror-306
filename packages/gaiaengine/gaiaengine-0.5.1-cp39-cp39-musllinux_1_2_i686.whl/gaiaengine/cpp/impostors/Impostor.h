#pragma once

#include <glm/glm.hpp>

#include "Manager.h"
#include "TargetInterface.h"

#include <array>
#include <memory>
#include <string>
#include <vector>

#include <pybind11/pybind11.h>

namespace py = pybind11;

class ImpostorAsset;
class ImpostorManager;
class Terrain;
class TextureArray;
class Window;

class Impostor : public ManagedElement<Impostor>, public TargetInterface {
public:
  Impostor(ImpostorManager* impostorManager, std::shared_ptr<const ImpostorAsset> impostorAsset, glm::vec2 position);

  virtual void update(int /*msElapsed*/, const Terrain*) {}
  virtual void updateDisplay(int /*msElapsed*/, float /*theta*/) {}

  inline std::vector<std::shared_ptr<Impostor>> getVisibleImpostors() const;

  // TargetInterface
  glm::vec2 getPosition() const override { return _position; }
  bool isValid() const override { return !isElementDeleted(); }

  // Getters and setters

  void setPosition(const glm::vec2& val);

  ImpostorManager* getImpostorManager() const;
  Window* getWindow() const;

  const TextureArray* getTextureArray() const;
  inline std::shared_ptr<const ImpostorAsset> getImpostorAsset() const { return _impostorAsset; }

  inline void setHeight(float height) { _height = height; setPositionArray(); }
  inline float getHeight() const { return _height; }

  inline const std::array<float, 12>& getVertices()      const {return _vertices;}
  inline const std::array<float, 12>& getPositionArray() const {return _posArray;}
  inline const std::array<float,  8>& getCoord2D()       const {return _coord2D;}
  inline const std::array<float,  4>& getLayer()         const {return _layer;}

  inline void setProjectedVertices(std::array<float, 12> nVertices) { _projectedVertices = nVertices; }
  // x y are the screen coordinates of the top left corner of the sprite ((0,0) being on the top left corner of the window
  // z w are the extent of the sprite
  glm::ivec4 getScreenRect() const;
  
  // Returns how far away from the camera the impostor is
  inline float getScreenDepth() const { return _projectedVertices[2]; }
  
  // Gets the screen position that will match the highest sprite height throughout all animations, aligned horizontally with the anchor
  glm::ivec2 getScreenTopCenter() const;

  inline int getType() const { return _type; }
  // Resets the line of sight to the base one of the new type
  void setType(int val);

  inline float getLineOfSight() const { return _lineOfSight; }
  void setLineOfSight(float val) { _lineOfSight = val; }

  inline bool canBeSelected() const { return _canBeSelected; }

  inline float getDisplayablePercentageValue() const { return _displayablePercentageValue; }
  inline glm::vec4 getDisplayableValueColor() const { return _displayableValueColor; }
  inline bool getShouldDisplayGauge() const { return _shouldDisplayGauge; }
  inline std::string getDisplayableText() const { return _displayableText; }

  inline int getCurrentSprite() const { return _currentSprite; }
  void setCurrentSprite(int val);

  inline int getCurrentTexture() const { return static_cast<int>(_layer[0]); }
  void setCurrentTexture(int val);

  int getNumSprites() const;
  int getNumTextures() const;

  static void pythonBindings(py::module& m);

  inline float getSizeFactor() const { return _sizeFactor; }
  inline void setSizeFactor(float val) { _sizeFactor = val; setCurrentSprite(getCurrentSprite()); }

protected:
  void setPositionArray();

  std::shared_ptr<const ImpostorAsset> _impostorAsset;
  float _sizeFactor = 1.f;

  // The type allows to set which impostor can be visible to which other, 
  // as well as having different navigation channels.
  // -1 is the default, where no type is defined (non-detectable, can navigate on anything)
  int _type = -1;
  float _lineOfSight = 0.f;

  glm::vec2 _position = glm::vec2(0);
  float _height = 0.f;

  bool _canBeSelected = false;
  float _displayablePercentageValue = 0.f;
  glm::vec4 _displayableValueColor = glm::vec4(0);
  bool _shouldDisplayGauge = true;
  std::string _displayableText;

  std::array<float, 12> _vertices{};
  std::array<float, 12> _posArray{};
  std::array<float,  8> _coord2D{};
  std::array<float,  4> _layer{};
  std::array<float, 12> _projectedVertices{};

private:
  int _currentSprite = -1;
};
