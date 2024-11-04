#include "Skybox.h"

#include "Camera.h"
#include "Shader.h"
#include "utils.h"
#include "Window.h"

#include <sstream>

static float t = 1000.f;

std::vector<std::string> Skybox::getTexturePaths(const std::string& folderPath) const {
  std::vector<std::string> texturePaths;

  // Load images with incremental names until it fails
  while (true) {
    std::ostringstream texturePath;
    texturePath << folderPath << texturePaths.size() << ".png";

    // Reached the end of the array
    if (!SDL_RWFromFile(texturePath.str().c_str(), "r"))
      break;

    texturePaths.push_back(texturePath.str());
  }

  return texturePaths;
}

Skybox::Skybox(Window* window):
  Skybox(window, GAIA_SOURCE_PATH + std::string("/res/assets/skybox"))
{}

Skybox::Skybox(Window* window, const std::string& texturePath) :
  Component(window),
  _indices {
     0,  1,  2,  2,  1,  3, // XN
     4,  5,  6,  6,  5,  7, // XP
     8,  9, 10, 10,  9, 11, // YN
    12, 13, 14, 14, 13, 15, // YP
    16, 17, 18, 18, 17, 19, // ZN
    20, 21, 22, 22, 21, 23  // ZP
  },
  _vertices {
     -t,-t,-t,  -t, t,-t,  -t,-t, t,  -t, t, t, // XN
      t, t,-t,   t,-t,-t,   t, t, t,   t,-t, t, // XP
      t,-t,-t,  -t,-t,-t,   t,-t, t,  -t,-t, t, // YN
     -t, t,-t,   t, t,-t,  -t, t, t,   t, t, t, // YP
      t,-t,-t,  -t,-t,-t,   t, t,-t,  -t, t,-t, // ZN
     -t, t, t,   t, t, t,  -t,-t, t,   t,-t, t  // ZP
  },
  _coord {
    0, 1,  1, 1,  0, 0,  1, 0,
    0, 1,  1, 1,  0, 0,  1, 0,
    0, 1,  1, 1,  0, 0,  1, 0,
    0, 1,  1, 1,  0, 0,  1, 0,
    0, 1,  1, 1,  0, 0,  1, 0,
    0, 1,  1, 1,  0, 0,  1, 0
  },
  _layer {
    0, 0, 0, 0,
    1, 1, 1, 1,
    2, 2, 2, 2,
    3, 3, 3, 3,
    4, 4, 4, 4,
    5, 5, 5, 5
  },
  _textureArray(getTexturePaths(texturePath))
{
  SCOPE_BIND(_vbo)

  glBufferData(	GL_ARRAY_BUFFER, sizeof(_vertices) + sizeof(_coord) + sizeof(_layer), NULL, GL_STATIC_DRAW);

  glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(_vertices), &_vertices[0]);
  glBufferSubData(GL_ARRAY_BUFFER, sizeof(_vertices) , sizeof(_coord), &_coord[0]);
  glBufferSubData(GL_ARRAY_BUFFER, sizeof(_vertices) + sizeof(_coord), sizeof(_layer), &_layer[0]);

  SCOPE_BIND(_ibo)

  glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(_indices), NULL, GL_STATIC_DRAW);
  glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, 0, sizeof(_indices), &_indices[0]);

  SCOPE_BIND(_vao)

  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(0));
  glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(sizeof(_vertices)));
  glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(sizeof(_vertices) + sizeof(_coord)));

  glEnableVertexAttribArray(0);
  glEnableVertexAttribArray(1);
  glEnableVertexAttribArray(2);
}

void Skybox::render(const Camera* camera) const {
  glm::mat4 view = glm::lookAt(
    glm::vec3(0, 0, 0),
    camera->getCurrentDirection(),
    camera->getCurrentUpVector()
  );

  glm::mat4 MVP = camera->getProjectionMatrix() * view;


  static const Shader shader = Shader("skybox.vert", "skybox.frag");
  SCOPE_BIND(shader)
  glUniformMatrix4fv(shader.getUniformLocation("MVP"),
    1, GL_FALSE, &MVP[0][0]);

  glDisable(GL_DEPTH_TEST);

  SCOPE_BIND(_vao)
  SCOPE_BIND(_textureArray)
  SCOPE_BIND(_ibo)

  glDrawElements(GL_TRIANGLES, (GLsizei) _indices.size(), GL_UNSIGNED_INT, BUFFER_OFFSET(0));

  glEnable(GL_DEPTH_TEST);
}

void Skybox::pythonBindings(py::module& m) {
  py::class_<Skybox, std::shared_ptr<Skybox>, Component>(m, "Skybox")
    .def(py::init<Window*>())
    .def(py::init<Window*, const std::string&>());
}