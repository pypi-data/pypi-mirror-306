#pragma once

#include <glm/gtx/vector_angle.hpp>

#include "Callback.h"
#include "Delegate.h"
#include "Impostor.h"
#include "MovingImpostorAsset.h"

#include <string>
#include <vector>

#include <pybind11/pybind11.h>

namespace py = pybind11;

class ImpostorManager;
class Terrain;


class MovingImpostor : public Impostor {
public:
  MovingImpostor(ImpostorManager* impostorManager, std::shared_ptr<const MovingImpostorAsset> impostorAsset, glm::vec2 position);

  void startAnimation(int animation);
  void startAnimation(int animation, float playbackSpeed);
  // The callback is expected to be a python function without arguments
  void startAnimation(int animation, const Callback& animFinishedCallback);
  void startAnimation(int animation, float playbackSpeed, const Callback& animFinishedCallback);

  void updateDisplay(int msElapsed, float theta) override; // Update sprite
  void update(int msElapsed, const Terrain* terrainManager) override; // Update pos and inner statuses

  // TargetInterface
  glm::vec2 getScaledDirection() const override { return _speed * _direction; }

  float getSpeed() const { return _speed; }
  inline void setSpeed(float newSpeed) { _speed = newSpeed; }

  bool hasReachedTarget() const;
  void stopMoving() { _speed = 0.f; _onStoppedMoving.broadcast(); }

  // React to the environment
  virtual void setTarget(const glm::vec2& target);
  void setTarget(std::shared_ptr<Impostor> target);
  glm::vec2 getTargetPosition() const;

  inline glm::vec2 getDirection() const { return _direction; }
  // Setting the direction makes you forget about the target
  virtual void setDirection(const glm::vec2& direction);

  inline float getOrientation() const { return _orientation; }
  void setOrientation(float nOrientation);

  inline bool isAnimationLoaded(int animation) { return _animationAsset->textureExists(animation); }

  static void pythonBindings(py::module& m);

private:
  void setDirectionInternal(const glm::vec2& direction);
  void updateAnimation(int msElapsed);
  int getClosestAnimOrientation(float orientation) const;

  float _speed = 0.f;
  std::shared_ptr<TargetInterface> _target;
  float _targetAcceptanceRadius = 0.5f;
  bool _stopOnReachTarget = false;
  // Normalized vector towards the target
  // It is private to guarantee a correct normalization
  glm::vec2 _direction = glm::vec2(0.f);

  Callback _onAnimFinished;

  float _camOrientation = 0.f;
  float _orientation = 0.f; // Angle between the front of the sprite and the camera

  // Animation variables
  std::shared_ptr<const MovingImpostorAsset> _animationAsset = nullptr;
  int _currentAnimationOrientation = -1;
  int _currentAnimFrame = -1;
  int _msAnimationElapsed = 0;
  bool _animPaused = false;
  float _animPlaybackSpeed = 1.f;

  Delegate _onTargetOrDirectionSet;
  Delegate _onStoppedMoving;
  Delegate _onTeleported;
};
