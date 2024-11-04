#include "Heightmap.h"

#include <glm/gtx/vector_angle.hpp>

#include "Camera.h"
#include "Terrain.h"
#include "Texture.h"
#include "Window.h"

#include <algorithm>
#include <array>
#include <cassert>

Heightmap::Heightmap(Window* window, const glm::ivec2& nbCells, std::vector<float> heights, std::vector<int> textureIDs) :
  Terrain(window),
  _nbVertices(nbCells + 1),
  _colors(heights.size(), Color(std::string("#40872d"))),
  _isNavigable(textureIDs.size(), true)
{
  setHeights(std::move(heights));
  setTextureIDs(std::move(textureIDs));

  updateVisuals(0, window->getCamera().get());
}

Heightmap::Heightmap(Window* window, const glm::ivec2& nbCells, std::vector<float> heights):
  Heightmap(window, nbCells, heights, std::vector<int>(nbCells.x* nbCells.y, -1))
{}

Heightmap::Heightmap(Window* window, const glm::ivec2& nbCells):
  Heightmap(window, nbCells, std::vector<float>((nbCells.x + 1) * (nbCells.y + 1), 0.f))
{}

void Heightmap::resize(const glm::ivec4& newRect) {
  // nbVertices = nbCells + 1 because we need one more dimension of vertices compared to cells
  glm::ivec2 newNbCells = glm::ivec2(newRect.z, newRect.w);
  glm::ivec2 nbCells = getNbCells();

  // Defaults for cut parts that are out of bounds
  std::vector<float> heights = std::vector<float>((newNbCells.x + 1) * (newNbCells.y + 1), 0.f);
  std::vector<Color> colors = std::vector<Color>((newNbCells.x + 1) * (newNbCells.y + 1), Color(std::string("#40872d")));
  std::vector<int> textureIDs = std::vector<int>(newNbCells.x * newNbCells.y, -1);
  std::vector<bool> isNavigable = std::vector<bool>(newNbCells.x * newNbCells.y, true);

  // Make sure the current values are kept
  for (int i = newRect.x; i < std::min(newRect.x + newNbCells.x + 1, _nbVertices.x); i++) {
    for (int j = newRect.y; j < std::min(newRect.y + newNbCells.y + 1, _nbVertices.y); j++) {
      int newCoordX = i - newRect.x;
      int newCoordY = j - newRect.y;

      heights[newCoordX * (newNbCells.y + 1) + newCoordY] = _heights[i * _nbVertices.y + j];
      colors[newCoordX * (newNbCells.y + 1) + newCoordY] = _colors[i * _nbVertices.y + j];

      if (newCoordX < newNbCells.x && newCoordY < newNbCells.y && i < nbCells.x && j < nbCells.y) {
        textureIDs[newCoordX * newNbCells.y + newCoordY] = _textureIDs[i * nbCells.y + j];
        isNavigable[newCoordX * newNbCells.y + newCoordY] = _isNavigable[i * nbCells.y + j];
      }
    }
  }

  _heights = std::move(heights);
  _colors = std::move(colors);
  _textureIDs = std::move(textureIDs);
  _isNavigable = std::move(isNavigable);

  _nbVertices = newNbCells + 1;

  _geometryDirty = true;
  _textureIDsDirty = true;
  updateVisuals(0, getWindow()->getCamera().get());
}

void Heightmap::updateVisuals(int /*msElapsed*/, const Camera*) {
  if (_textureIDsDirty)
    generateTextureMapping();

  if (_geometryDirty)
    generateGeometry();
}

void Heightmap::setNavigation(std::vector<bool> isNavigable) {
  if (isNavigable.size() != _textureIDs.size())
    throw std::out_of_range(std::string("Wrong size of argument, expected size ") + std::to_string(_textureIDs.size()));

  _isNavigable = std::move(isNavigable);
}

bool Heightmap::getIsNavigable(const glm::vec2& pos) const {
  if (isOutsideBounds(pos))
    return false;

  return _isNavigable[(int)pos.x * getNbCells().y + (int)pos.y];
}

void Heightmap::setIsNavigable(const glm::ivec2& cellCoordinates, bool navigable) {
  if (!isValidCellCoordinates(cellCoordinates)) {
    _isNavigable[cellCoordinates.x * getNbCells().y + cellCoordinates.y] = navigable;
  }
}

float Heightmap::getHeight(const glm::vec2& pos) const {
  if (isOutsideBounds(pos))
    return 0.f;

  int X = (int)pos.x;
  int Y = (int)pos.y;
  float x = pos.x - X;
  float y = pos.y - Y;

  // Bilinear interpolation
  // h0 -- hx0 - h1
  // |      |    |
  // |      h    |
  // |      |    |
  // h2 -- hx1 - h3

  float h0 = _heights[      X * _nbVertices.y + Y];
  float h1 = _heights[(X + 1) * _nbVertices.y + Y];
  float h2 = _heights[      X * _nbVertices.y + Y + 1];
  float h3 = _heights[(X + 1) * _nbVertices.y + Y + 1];

  float hx0 = h0 * (1 - x) + h1 * x;
  float hx1 = h2 * (1 - x) + h3 * x;

  return hx0 * (1 - y) + hx1 * y;
}

void Heightmap::setHeight(const glm::ivec2& vertCoordinates, float height) {
  if (!isValidVertexCoordinates(vertCoordinates)) {
    _heights[vertCoordinates.x * _nbVertices.y + vertCoordinates.y] = height;
    _geometryDirty = true;
  }
}

int Heightmap::getTextureID(const glm::vec2& pos) const {
  if (isOutsideBounds(pos))
    return 0;

  return _textureIDs[(int)pos.x * getNbCells().y + (int)pos.y];
}

void Heightmap::setTextureID(const glm::ivec2& cellCoordinates, int textureID) {
  if (!isValidCellCoordinates(cellCoordinates)) {
    _textureIDs[cellCoordinates.x * getNbCells().y + cellCoordinates.y] = textureID;
    _textureIDsDirty = true;
  }
}

Color Heightmap::getColor(const glm::vec2& pos) const {
  if (isOutsideBounds(pos))
    return Color((Uint8)0,0,0,0);

  return _colors[(int)pos.x * _nbVertices.y + (int)pos.y];
}

void Heightmap::setColor(const glm::ivec2& vertCoordinates, const Color& color) {
  if (!isValidVertexCoordinates(vertCoordinates)) {
    _colors[vertCoordinates.x * _nbVertices.y + vertCoordinates.y] = color;
    _geometryDirty = true;
  }
}

void Heightmap::generateGeometry() {
  _geometryDirty = false;

  std::vector<float> vertices, normals, colors;

  glm::ivec2 nbCells = _nbVertices - 1;

  vertices.resize(nbCells.x * nbCells.y * 3 * 6, 0.f);
  normals.resize(nbCells.x * nbCells.y * 3 * 6, 0.f);
  colors.resize(nbCells.x * nbCells.y * 4 * 6, 0.f);

  auto setVertexData = [&](int currentIndex, int x, int y, glm::vec3 normal, Color color) {
    vertices[3 * currentIndex] = (float)x;
    vertices[3 * currentIndex + 1] = (float)y;
    vertices[3 * currentIndex + 2] = _heights[x * _nbVertices.y + y];

    if (_smoothNormals)
      normal = getNormal(glm::ivec2(x, y), false);

    normals[3 * currentIndex] = normal.x;
    normals[3 * currentIndex + 1] = normal.y;
    normals[3 * currentIndex + 2] = normal.z;

    if (_smoothColors)
      color = _colors[x * _nbVertices.y + y];

    colors[4 * currentIndex] = color.getFloatR();
    colors[4 * currentIndex + 1] = color.getFloatG();
    colors[4 * currentIndex + 2] = color.getFloatB();
    colors[4 * currentIndex + 3] = color.getFloatA();
  };

  for (int i = 0; i < nbCells.x; i++) {
    for (int j = 0; j < nbCells.y; j++) {
      
      glm::vec3 normal = getNormal(glm::ivec2(i, j), true);

      Color color = _colors[i * _nbVertices.y + j];

      setVertexData(6 * (i * nbCells.y + j),     i,     j,     normal, color);
      setVertexData(6 * (i * nbCells.y + j) + 1, i + 1, j,     normal, color);
      setVertexData(6 * (i * nbCells.y + j) + 2, i,     j + 1, normal, color);
      setVertexData(6 * (i * nbCells.y + j) + 3, i,     j + 1, normal, color);
      setVertexData(6 * (i * nbCells.y + j) + 4, i + 1, j,     normal, color);
      setVertexData(6 * (i * nbCells.y + j) + 5, i + 1, j + 1, normal, color);
    }
  }

  SCOPE_BIND(_vbo)

  size_t bufferSizeVertices = vertices.size() * sizeof vertices[0];
  size_t bufferSizeNormals = normals.size() * sizeof normals[0];
  size_t bufferSizeColors = colors.size() * sizeof colors[0];

  glBufferData(GL_ARRAY_BUFFER, bufferSizeVertices + bufferSizeNormals + bufferSizeColors, NULL, GL_DYNAMIC_DRAW);
  glBufferSubData(GL_ARRAY_BUFFER, 0, bufferSizeVertices, &vertices[0]);
  glBufferSubData(GL_ARRAY_BUFFER, bufferSizeVertices, bufferSizeNormals, &normals[0]);
  glBufferSubData(GL_ARRAY_BUFFER, bufferSizeVertices + bufferSizeNormals, bufferSizeColors, &colors[0]);

  SCOPE_BIND(_vao)

  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(0));
  glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(vertices.size() * sizeof vertices[0]));
  glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(vertices.size() * sizeof vertices[0] + normals.size() * sizeof normals[0]));

  glEnableVertexAttribArray(0);
  glEnableVertexAttribArray(1);
  glEnableVertexAttribArray(2);
}

glm::vec3 Heightmap::getNormal(const glm::ivec2& coordinates, bool fullFace) const {
  int x = coordinates.x;
  int y = coordinates.y;
  float C, T, L, R, B;
  //     T
  //  L  C  R
  //     B

  // Interpolated normal of point based on surrounding ones
  if (!fullFace) {
    C = _heights[x * _nbVertices.y + y];
    T = y - 1 >= 0 ? _heights[x * _nbVertices.y + y - 1] : C;
    L = x - 1 >= 0 ? _heights[(x - 1) * _nbVertices.y + y] : C;
    R = x + 1 < _nbVertices.x ? _heights[(x + 1) * _nbVertices.y + y] : C;
    B = y + 1 < _nbVertices.y ? _heights[x * _nbVertices.y + y + 1] : C;
  }

  // Interpolated normal based on the two diagonals of a face
  else {
    T = _heights[x * _nbVertices.y + y];
    L = _heights[x * _nbVertices.y + y + 1]; 
    R = _heights[(x + 1) * _nbVertices.y + y];
    B = _heights[(x + 1) * _nbVertices.y + y + 1];
  }

  return glm::cross(glm::normalize(glm::vec3(1.f, 0.f, R - L)), glm::normalize(glm::vec3(0.f, 1.f, T - B)));
}

void Heightmap::generateTextureMapping() {
  _textureIDsDirty = false;
  _ibos.clear();
  _indicesPerTexture.clear();

  for (int i = 0; i < _nbVertices.x - 1; i++) {
    for (int j = 0; j < _nbVertices.y - 1; j++) {
      std::vector<int>& currentIndicesArray = _indicesPerTexture[_textureIDs[i * (_nbVertices.y - 1) + j]];
      for (int k = 0; k < 6; k++) {
        currentIndicesArray.push_back(6 * (i * (_nbVertices.y - 1) + j) + k);
      }
    }
  }

  // IBO for each texture

  for (auto& indicesForTexture : _indicesPerTexture) {
    size_t bufferSizeIndices = indicesForTexture.second.size() * sizeof indicesForTexture.second[0];

    SCOPE_BIND(_ibos[indicesForTexture.first])

    glBufferData(GL_ELEMENT_ARRAY_BUFFER, bufferSizeIndices, NULL, GL_STATIC_DRAW);
    glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, 0, bufferSizeIndices, &(indicesForTexture.second[0]));
  }
}

void Heightmap::render(const Camera* camera) const {
  glm::mat4 MVP = camera->getViewProjectionMatrix();

  SCOPE_BIND(_terrainShader)
  glUniformMatrix4fv(_terrainShader.getUniformLocation("MVP"), 1, GL_FALSE, &MVP[0][0]);
  glUniform3f(_terrainShader.getUniformLocation("originOffset"), _originOffset.x, _originOffset.y, _originOffset.z);
  glUniform1i(_terrainShader.getUniformLocation("useColor"), false);
  glUniform1i(_terrainShader.getUniformLocation("noNormal"), _noNormalInShader);

  if (_wireframe)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

  SCOPE_BIND(_vao)

  for (auto& ibo : _ibos) {
    if (ibo.first == -1)
      glUniform1i(_terrainShader.getUniformLocation("useColor"), true);
    else
      bindTexture(ibo.first);

    SCOPE_BIND(ibo.second)

    glDrawElements(GL_TRIANGLES, (GLsizei)_indicesPerTexture.at(ibo.first).size(), GL_UNSIGNED_INT, BUFFER_OFFSET(0));

    if (ibo.first == -1)
      glUniform1i(_terrainShader.getUniformLocation("useColor"), false);
  }

  Texture::unbind();

  if (_wireframe)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
}

void Heightmap::setSmoothNormals(bool val) {
  if (_smoothNormals != val) {
    _smoothNormals = val;
    _geometryDirty = true;
  }
}

void Heightmap::setSmoothColors(bool val) {
  if (_smoothColors != val) {
    _smoothColors = val;
    _geometryDirty = true;
  }
}

#include <pybind11/stl.h>

void Heightmap::pythonBindings(py::module& m) {
  py::class_<Heightmap, std::shared_ptr<Heightmap>, Terrain>(m, "Heightmap")
    .def(py::init<Window*, const glm::ivec2&>())
    .def(py::init<Window*, const glm::ivec2&, std::vector<float>>())
    .def(py::init<Window*, const glm::ivec2&, std::vector<float>, std::vector<int>>())
    .def("getNavigation", &Heightmap::getNavigation)
    .def("setNavigation", &Heightmap::setNavigation)
    .def("getIsNavigable", &Heightmap::getIsNavigable)
    .def("setIsNavigable", &Heightmap::setIsNavigable)
    .def("getHeights", &Heightmap::getHeights)
    .def("setHeights", &Heightmap::setHeights)
    .def("getHeight", &Heightmap::getHeight)
    .def("setHeight", &Heightmap::setHeight)
    .def("getTextureIDs", &Heightmap::getTextureIDs)
    .def("setTextureIDs", &Heightmap::setTextureIDs)
    .def("getTextureID", &Heightmap::getTextureID)
    .def("setTextureID", &Heightmap::setTextureID)
    .def("getColors", &Heightmap::getColors)
    .def("setColors", &Heightmap::setColors)
    .def("getColor", &Heightmap::getColor)
    .def("setColor", &Heightmap::setColor)
    .def("getTexture", &Heightmap::getTexture)
    .def("resize", py::overload_cast<const glm::ivec2&>(&Heightmap::resize))
    .def("resize", py::overload_cast<const glm::ivec4&>(&Heightmap::resize))
    .def("getNormal", &Heightmap::getNormal)
    .def("getNbCells", &Heightmap::getNbCells)
    .def("getNbVertices", &Heightmap::getNbVertices)
    .def_property("originOffset", &Heightmap::getOriginOffset, &Heightmap::setOriginOffset)
    .def_readwrite("noNormalInShader", &Heightmap::_noNormalInShader)
    .def_property("smoothNormals", &Heightmap::getSmoothNormals, &Heightmap::setSmoothNormals)
    .def_property("smoothColors", &Heightmap::getSmoothColors, &Heightmap::setSmoothColors);
}
