#pragma once

#include "BasicGLObjects.h"

#include <memory>
#include <vector>

class Impostor;
class TextureArray;

class ImpostorRenderer {
public:
  ImpostorRenderer() = default;

  void loadImpostors(const std::vector<std::shared_ptr<Impostor>>& visibleImpostors, bool onlyOnce = false);
  int renderImpostors() const;

private:
  void fillBufferData(GLenum renderType);
  void processSpree(const std::vector<std::shared_ptr<Impostor>>& visibleImpostors, int currentSpreeLength, int firstIndexSpree);

  int _capacity = 0;
  bool _fixedCapacity = false;

  std::vector<float> _data;

  VertexArrayObject _vao;
  VertexBufferObject _vbo;
  IndexBufferObject _ibo;
  std::vector<const TextureArray*> _textures;
  std::vector<int> _nbImpostorsInSpree;
};
