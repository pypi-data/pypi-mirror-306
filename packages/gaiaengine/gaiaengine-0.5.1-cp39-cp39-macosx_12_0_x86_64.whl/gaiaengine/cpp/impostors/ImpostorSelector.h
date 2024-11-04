#pragma once

#include "Component.h"
#include "ColoredRectangles.h"

#include <functional>
#include <memory>
#include <vector>

class Camera;
class HeightmapCamera;
class Impostor;
class ImpostorManager;
class InGameText;
class UIManager;

class ImpostorSelector : public Component {
public:
  ImpostorSelector(Window* window, std::shared_ptr<ImpostorManager> impostorManager, std::shared_ptr<UIManager> uiManager);

  void updateVisuals(int msElapsed, const Camera* camera) override;
  void render(const Camera* camera) const override;

  std::shared_ptr<Impostor> getSelectableImpostor(glm::ivec2 screenTarget) const;
  void select(const glm::ivec4& encompassingRectangle, bool add, const std::function<bool(const std::shared_ptr<Impostor>)>& filter);
  inline void select(const glm::ivec4& encompassingRectangle, bool add) {
    select(encompassingRectangle, add, [](const std::shared_ptr<Impostor>) { return true; });
  }

  inline void clearSelection() { _selection.clear(); }
  inline bool isSelectionEmpty() { cleanUpSelection(); return _selection.empty(); }
  inline void addToSelection(std::shared_ptr<Impostor> impostor) { _selection.push_back(impostor); }
  inline void removeFromSelection(std::shared_ptr<Impostor> impostor) {
    std::erase_if(_selection, [impostor](std::weak_ptr<Impostor> it) { return it.lock() == impostor; });
  }
  void deleteOneInSelection();
  void goBackToSelection(HeightmapCamera* camera);
  void moveSelection(const glm::vec2& target);

  std::vector<std::shared_ptr<Impostor>> getSelection();

  static void pythonBindings(py::module& m);

private:
  // Remove stale elements from the selection
  void cleanUpSelection();

  void computeImpostor2DCorners(const Camera* camera);
  void updateRectSelectDisplay(const Camera* camera);

  std::shared_ptr<ImpostorManager> _impostorManager;

  glm::ivec4 _selectionRectangle = glm::ivec4(-1);
  ColoredRectangles _rectSelectDisplay;
  glm::ivec2 _gaugeSize = glm::ivec2(20, 4);
  std::shared_ptr<InGameText> _inGameText;

  bool _displayImpostorSelectionHitboxes = false;
  bool _displaySelectionRectangle = false;

  std::vector<std::weak_ptr<Impostor>> _selection;
};
