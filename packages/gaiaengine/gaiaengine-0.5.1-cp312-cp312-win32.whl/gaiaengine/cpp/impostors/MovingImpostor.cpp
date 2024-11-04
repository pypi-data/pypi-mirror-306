#include "MovingImpostor.h"

#include "ImpostorAsset.h"
#include "ImpostorManager.h"
#include "Terrain.h"

#include <cmath>
#include <ctime>

MovingImpostor::MovingImpostor(ImpostorManager* impostorManager, std::shared_ptr<const MovingImpostorAsset> impostorAsset, glm::vec2 position) :
  Impostor(impostorManager, impostorAsset, position),
  _orientation(rand() / (float)RAND_MAX * 360.f),
  _animationAsset(impostorAsset)
{
  _canBeSelected = true;
  startAnimation(0);
}

void MovingImpostor::startAnimation(int animation) {
  startAnimation(animation, 1.f, Callback());
}

void MovingImpostor::startAnimation(int animation, float playbackSpeed) {
  startAnimation(animation, playbackSpeed, Callback());
}

void MovingImpostor::startAnimation(int animation, const Callback& animFinishedCallback) {
  startAnimation(animation, 1.f, animFinishedCallback);
}

void MovingImpostor::startAnimation(int animation, float playbackSpeed, const Callback& animFinishedCallback) {
  if (!_animationAsset->textureExists(animation))
    throw std::out_of_range("Trying to start an animation whose asset hasn't been loaded");

  setCurrentTexture(animation);
  setCurrentSprite(getClosestAnimOrientation(getOrientation()) * _animationAsset->getNbSteps(getCurrentTexture()));

  _currentAnimFrame = 0;
  _msAnimationElapsed = 0;
  _animPaused = false;

  _animPlaybackSpeed = playbackSpeed;
  _onAnimFinished = std::move(animFinishedCallback);
}

void MovingImpostor::updateDisplay(int /*msElapsed*/, float theta) {
  setOrientation(_orientation + _camOrientation - theta); // Orientation moves opposite to the camera
  _camOrientation = theta;

  if (_direction.x != 0.f || _direction.y != 0.f) {
    float ori = glm::degrees(glm::orientedAngle(glm::vec2(1.0f, 0.0f), _direction));
    setOrientation(ori - _camOrientation);
  }
}

void MovingImpostor::update(int msElapsed, const Terrain* terrain) {
  _height = terrain->getHeight(_position);

  float cappedSpeed = _speed;

  if (_target) {
    if (!_target->isValid()) {
      stopMoving();
      _stopOnReachTarget = false;
      _target.reset();
    }
    else if (_stopOnReachTarget && hasReachedTarget()) {
      stopMoving();
      _stopOnReachTarget = false;
    }
    else {
      setDirectionInternal(_target->getPosition() - _position);
      if (hasReachedTarget())
        // Making sure we don't continue moving too fast towards the target if it's not going away
        cappedSpeed = std::min(std::sqrt(std::max(0.f, glm::dot(_target->getScaledDirection(), _direction))), _speed);
    }
  }

  // Don't update the position if the direction is invalid
  if (_direction != glm::vec2(0.f)) {
    glm::vec2 newPos = _position + _direction * cappedSpeed * (msElapsed / 1000.f);

    bool hasTeleported = false;
    glm::vec2 teleportTriggerPosition = glm::vec2(-1);

    if (getImpostorManager()->getImpostorsCanWrapAroundWorld()) {
      teleportTriggerPosition = newPos;
      hasTeleported = terrain->teleportPositionOnOtherSideIfOutside(newPos);
    }

    if (terrain->getIsNavigable(newPos))
      _position = newPos;
    else
      stopMoving();

	if (hasTeleported) {
		_height = terrain->getHeight(_position);
		_onTeleported.broadcast(py::make_tuple(teleportTriggerPosition));
	}

    setPositionArray();
  }

  updateAnimation(msElapsed);
}

bool MovingImpostor::hasReachedTarget() const {
  if (!_target)
    return false;

  return glm::length2(_target->getPosition() - _position) < _targetAcceptanceRadius * _targetAcceptanceRadius;
}

void MovingImpostor::setTarget(const glm::vec2& target) {
  _target = std::make_shared<StaticTarget>(target);
  _stopOnReachTarget = true;
  setDirectionInternal(_target->getPosition() - _position);
  if (_speed == 0.f)
    _onTargetOrDirectionSet.broadcast();
}

void MovingImpostor::setTarget(std::shared_ptr<Impostor> target) {
  _target = target;
  // By default, a MovingImpostor will follow an Impostor target instead of stopping when reached
  _stopOnReachTarget = false; 
  if (_target)
    setDirectionInternal(_target->getPosition() - _position);
  if (_speed == 0.f)
    _onTargetOrDirectionSet.broadcast();
}

glm::vec2 MovingImpostor::getTargetPosition() const {
  if (!_target)
    throw std::runtime_error("No valid target");

  return _target->getPosition();
}

void MovingImpostor::setDirection(const glm::vec2& direction) {
  setDirectionInternal(direction);
  _stopOnReachTarget = false;
  _target.reset();
  if (_speed == 0.f)
    _onTargetOrDirectionSet.broadcast();
}

void MovingImpostor::setDirectionInternal(const glm::vec2& direction) {
  // Only setting the direction if it's not going to be NaN.
  if (direction != glm::vec2(0.f))
    _direction = glm::normalize(direction);
  else
    _direction = direction;
}

void MovingImpostor::setOrientation(float nOrientation) {
  _orientation = nOrientation;

  if (_orientation < 0.f)
    _orientation += 360.f + 360 * (int)(-_orientation / 360);
  else
    _orientation -= 360.f * (int)(_orientation / 360);
}

void MovingImpostor::updateAnimation(int msElapsed) {
  if (_animPlaybackSpeed == 0.0 || _animPaused)
    return;

  int steps = _animationAsset->getNbSteps(getCurrentTexture());
  int frameDuration = (int) (_animationAsset->getFrameDurationMs(getCurrentTexture()) / _animPlaybackSpeed);
  int msPause = _animationAsset->getReplayDelay(getCurrentTexture());
  _msAnimationElapsed += msElapsed;

  // We make sure that the elapsed time does not extend one loop
  int msTotalAnimDuration = steps * frameDuration + msPause;
  _msAnimationElapsed = _msAnimationElapsed % msTotalAnimDuration;

  int nextSprite = _currentAnimFrame + _msAnimationElapsed / frameDuration;

  // Simple case, no restart to handle
  if (nextSprite < steps) {
    _msAnimationElapsed -= (nextSprite - _currentAnimFrame) * frameDuration;
    _currentAnimFrame = nextSprite;
  }

  else {
    _msAnimationElapsed -= (steps - 1 - _currentAnimFrame) * frameDuration;

    // The sprite is in the pause
    if (_msAnimationElapsed < msPause)
      _currentAnimFrame = steps - 1;

    // The sprite has started a new loop
    else {
      _onAnimFinished();

      // Only if no animation was launched by the callback
      if (_msAnimationElapsed != 0) {
        _msAnimationElapsed -= msPause;
        nextSprite = _msAnimationElapsed / frameDuration;
        _msAnimationElapsed -= nextSprite * frameDuration;
        _currentAnimFrame = nextSprite;
      }
    }
  }

  _currentAnimationOrientation = getClosestAnimOrientation(getOrientation());
  setCurrentSprite(_currentAnimationOrientation * _animationAsset->getNbSteps(getCurrentTexture()) + _currentAnimFrame);
}

int MovingImpostor::getClosestAnimOrientation(float orientation) const {
  float orientationStep = 360.f / (float)_animationAsset->getNbOrientations();

  return (_animationAsset->getNbOrientations() - (int)(round(orientation / orientationStep) + 0.5f))
    % _animationAsset->getNbOrientations();
}

#include <pybind11/stl.h>

void MovingImpostor::pythonBindings(py::module& m) {
  py::class_<MovingImpostor, std::shared_ptr<MovingImpostor>, Impostor>(m, "MovingImpostor")
    .def(py::init<ImpostorManager*, std::shared_ptr<const MovingImpostorAsset>, glm::vec2>())
    .def("getTargetPosition", &MovingImpostor::getTargetPosition)
    .def("setTarget", py::overload_cast<const glm::vec2&>(&MovingImpostor::setTarget))
    .def("setTarget", py::overload_cast<std::shared_ptr<Impostor>>(&MovingImpostor::setTarget))
    .def("hasReachedTarget", &MovingImpostor::hasReachedTarget)
    .def("stopMoving", &MovingImpostor::stopMoving)
    .def_property("direction", &MovingImpostor::getDirection, &MovingImpostor::setDirection)
    .def_readwrite("stopOnReachTarget", &MovingImpostor::_stopOnReachTarget)
    .def_readwrite("targetAcceptanceRadius", &MovingImpostor::_targetAcceptanceRadius)
    .def_property("_orientation", &MovingImpostor::getOrientation, &MovingImpostor::setOrientation)
    .def_property("speed", &MovingImpostor::getSpeed, &MovingImpostor::setSpeed)
    .def_readonly("currentAnimationOrientation", &MovingImpostor::_currentAnimationOrientation)
    .def_readwrite("currentAnimFrame", &MovingImpostor::_currentAnimFrame)
    .def_readwrite("animPaused", &MovingImpostor::_animPaused)
    .def("isAnimationLoaded", &MovingImpostor::isAnimationLoaded)
    .def("startAnimation", py::overload_cast<int>(&MovingImpostor::startAnimation))
    .def("startAnimation", py::overload_cast<int, float>(&MovingImpostor::startAnimation))
    .def("startAnimation", py::overload_cast<int, const Callback&>(&MovingImpostor::startAnimation))
    .def("startAnimation", py::overload_cast<int, float, const Callback&>(&MovingImpostor::startAnimation))
    .def_readonly("onTargetOrDirectionSet", &MovingImpostor::_onTargetOrDirectionSet)
    .def_readonly("onStoppedMoving", &MovingImpostor::_onStoppedMoving)
    .def_readonly("onTeleported", &MovingImpostor::_onTeleported);

}
