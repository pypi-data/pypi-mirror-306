#pragma once

#include "BasicGLObjects.h"
#include "Component.h"
#include "TextureArray.h"

#include <array>
#include <string>
#include <vector>

class Skybox: public Component {
public:
  Skybox(Window* window);
  Skybox(Window* window, const std::string& texturePath);

  void render(const Camera* camera) const override;

  static void pythonBindings(py::module& m);
private:
  std::vector<std::string> getTexturePaths(const std::string& folderPath) const;

  std::array<GLuint,36> _indices{};
  std::array<float, 72> _vertices{};
  std::array<float, 48> _coord{};
  std::array<float, 24> _layer{};

  VertexArrayObject _vao;
  VertexBufferObject _vbo;
  IndexBufferObject _ibo;

  TextureArray _textureArray;
};
