#pragma once

#include <glm/glm.hpp>

#include "BasicGLObjects.h"
#include "Terrain.h"

#include <unordered_map>
#include <vector>

// Vertex coordinates and cell coordinates
// 0,0 --- 0,1 --- 0,2
//  |  0,0  |  0,1  |
// 1,0 --- 1,1 --- 1,2
//  |  1,0  |  1,1  |
// 2,0 --- 2,1 --- 2,2

class Heightmap : public Terrain {
public:
  Heightmap(Window* window, const glm::ivec2& nbCells);
  Heightmap(Window* window, const glm::ivec2& nbCells, std::vector<float> heights);
  Heightmap(Window* window, const glm::ivec2& nbCells, std::vector<float> heights, std::vector<int> textureIDs);

  void updateVisuals(int /*msElapsed*/, const Camera*) override;
  void render(const Camera* camera) const override;

  glm::vec2 getMaxCoordinates() const override { return glm::vec2(_nbVertices.x - 1, _nbVertices.y - 1); }

  inline bool isValidCellCoordinates(const glm::ivec2& coord) const {
    return coord.x < 0 || coord.y < 0 || coord.x >= getNbCells().x || coord.y >= getNbCells().y;
  }

  inline bool isValidVertexCoordinates(const glm::ivec2& coord) const {
    return coord.x < 0 || coord.y < 0 || coord.x >= getNbVertices().x || coord.y >= getNbVertices().y;
  }

  inline glm::ivec2 getNbCells() const { return glm::ivec2(_nbVertices.x - 1, _nbVertices.y - 1); }
  inline glm::ivec2 getNbVertices() const { return _nbVertices; }

  inline void resize(const glm::ivec2& nbCells) { resize(glm::ivec4(0, 0, nbCells)); }
  void resize(const glm::ivec4& newRect);

  inline const std::vector<bool>& getNavigation() const { return _isNavigable; }
  void setNavigation(std::vector<bool> isNavigable);
  bool getIsNavigable(const glm::vec2& pos) const override;
  void setIsNavigable(const glm::ivec2& cellCoordinates, bool isNavigable) override;

  inline virtual const std::vector<float>& getHeights() const { return _heights; }
  inline virtual void setHeights(std::vector<float> heights) { _heights = std::move(heights); _geometryDirty = true; }
  float getHeight(const glm::vec2& pos) const override;
  void setHeight(const glm::ivec2& vertCoordinates, float height) override;

  inline const std::vector<int>& getTextureIDs() const { return _textureIDs; }
  inline void setTextureIDs(std::vector<int> textureIDs) { _textureIDs = std::move(textureIDs); _textureIDsDirty = true; }
  int getTextureID(const glm::vec2& pos) const override;
  void setTextureID(const glm::ivec2& cellCoordinates, int textureID) override;

  inline const std::vector<Color>& getColors() const { return _colors; }
  inline void setColors(std::vector<Color> colors) { _colors = std::move(colors); _geometryDirty = true; }
  Color getColor(const glm::vec2& pos) const override;
  void setColor(const glm::ivec2& vertCoordinates, const Color& color) override;

  std::shared_ptr<Texture> getTexture(const glm::vec2& pos) const override { return Terrain::getTexture(getTextureID(pos)); }

  glm::vec3 getNormal(const glm::ivec2& coordinates, bool fullFace) const;
  
  inline glm::vec3 getOriginOffset() const { return _originOffset; }
  inline void setOriginOffset(glm::vec3 val) { _originOffset = val; }

  inline bool getSmoothNormals() const { return _smoothNormals; }
  void setSmoothNormals(bool val);

  inline bool getSmoothColors() const { return _smoothColors; }
  void setSmoothColors(bool val);

  static void pythonBindings(py::module& m);

private:
  void generateGeometry();
  void generateTextureMapping();

  glm::ivec2 _nbVertices = glm::ivec2(-1);
  std::vector<float> _heights;
  std::vector<Color> _colors;
  std::vector<int> _textureIDs;
  std::vector<bool> _isNavigable;
  glm::vec3 _originOffset = glm::vec3(0.f);

  bool _noNormalInShader = false;
  bool _smoothNormals = true;
  bool _smoothColors = false;

  bool _geometryDirty = false;
  bool _textureIDsDirty = false;

  // Buffers
  VertexArrayObject _vao;
  VertexBufferObject _vbo;
  std::unordered_map<int, IndexBufferObject> _ibos;

  // Data
  std::unordered_map<int, std::vector<int>> _indicesPerTexture;
};