#include "MovingImpostorAsset.h"

MovingImpostorAsset::MovingImpostorAsset(const std::vector<std::string>& assetPaths):
  MovingImpostorAsset(assetPaths, {})
{}

MovingImpostorAsset::MovingImpostorAsset(const std::vector<std::string>& assetPaths, const std::vector<float>& animDurations):
  MovingImpostorAsset(assetPaths, animDurations, {})
{}

MovingImpostorAsset::MovingImpostorAsset(const std::vector<std::string>& assetPaths, const std::vector<float>& animDurations, const std::vector<float>& replayDelays):
  ImpostorAsset(assetPaths)
{
  // If the anim durations are not specified yet, they'll get their default on loading,
  // since it will depend on the number of frames
  if (animDurations.size() != 0)
    _animDurations = animDurations;

  _replayDelays.resize(assetPaths.size());

  for (int i = 0; i < replayDelays.size(); i++) {
    _replayDelays[i] = (int) (replayDelays[i] * 1000);
  }
}

void MovingImpostorAsset::load() {
  ImpostorAsset::load();

  for (int i = 0; i < _spriteInfo.size(); i++) {
    int nbSteps = (int) _spriteInfo[i].size() / 5;

    // TODO make orientation handling more generic
    // Hack: if there is only one sprite, it means that it's a static picture and we don't want to generate the additional orientations
    if (_spriteInfo[i].size() == 1)
      continue;

    // 8 orientations, we need to manually fill the 3 missing
    _spriteInfo[i].resize(nbSteps * 8);

    // The missing 3 orientations are horizontally flipped copies of the others
    for (int j = 0; j < nbSteps; j++) {
      _spriteInfo[i][5 * nbSteps + j] = _spriteInfo[i][3 * nbSteps + j].getFlippedCopy();
      _spriteInfo[i][6 * nbSteps + j] = _spriteInfo[i][2 * nbSteps + j].getFlippedCopy();
      _spriteInfo[i][7 * nbSteps + j] = _spriteInfo[i][1 * nbSteps + j].getFlippedCopy();
    }
  }

  if (_animDurations.size() == 0) {
    _animDurations.resize(_assetPaths.size());
    for (int i = 0; i < _animDurations.size(); i++) {
      _animDurations[i] = getNbSteps(i) / 25.f; // Default of 25 FPS for an unspecified animation
    }
  }
}

#include <pybind11/stl.h>

void MovingImpostorAsset::pythonBindings(py::module& m) {
  py::class_<MovingImpostorAsset, std::shared_ptr<MovingImpostorAsset>, ImpostorAsset>(m, "MovingImpostorAsset")
    .def(py::init<const std::vector<std::string>&>())
    .def(py::init<const std::vector<std::string>&, const std::vector<float>&>())
    .def(py::init<const std::vector<std::string>&, const std::vector<float>&, const std::vector<float>&>())
    .def("getNbSteps", &MovingImpostorAsset::getNbSteps)
    .def("getFrameDurationMs", &MovingImpostorAsset::getFrameDurationMs)
    .def("getReplayDelay", &MovingImpostorAsset::getReplayDelay)
    .def("getAnimDuration", &MovingImpostorAsset::getAnimDuration)
    .def_readwrite("animDurations", &MovingImpostorAsset::_animDurations)
    .def_readwrite("replayDelays", &MovingImpostorAsset::_replayDelays);
}