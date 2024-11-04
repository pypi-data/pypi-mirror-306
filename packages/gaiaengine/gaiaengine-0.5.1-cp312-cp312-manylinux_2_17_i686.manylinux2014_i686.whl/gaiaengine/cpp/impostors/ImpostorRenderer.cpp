#include "ImpostorRenderer.h"

#include "MovingImpostor.h"
#include "TextureArray.h"

#include <cmath>

void ImpostorRenderer::fillBufferData(GLenum renderType) {
  if (_data.size() == 0)
    return;

  SCOPE_BIND(_vbo)

  glBufferData(GL_ARRAY_BUFFER, _data.size() * sizeof(float), &_data[0], renderType);

  SCOPE_BIND(_ibo)

  std::vector<GLuint> indices(6*_capacity);

  for (int i = 0; i < _capacity; i++) {
    indices[6*i]     = 0 + 4*i;
    indices[6*i + 1] = 1 + 4*i;
    indices[6*i + 2] = 2 + 4*i;
    indices[6*i + 3] = 0 + 4*i;
    indices[6*i + 4] = 2 + 4*i;
    indices[6*i + 5] = 3 + 4*i;
  }

  glBufferData(GL_ELEMENT_ARRAY_BUFFER, _capacity * 6 * sizeof(indices[0]), &indices[0], GL_STATIC_DRAW);

  SCOPE_BIND(_vao)

  int sizeVertices = _capacity * 12 * sizeof(float);
  int sizeCoord2D = _capacity * 8 * sizeof(float);

  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(0));
  glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(sizeVertices));
  glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(2*sizeVertices));
  glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(2*sizeVertices + sizeCoord2D));

  glEnableVertexAttribArray(0);
  glEnableVertexAttribArray(1);
  glEnableVertexAttribArray(2);
  glEnableVertexAttribArray(3);
}

void ImpostorRenderer::processSpree(const std::vector<std::shared_ptr<Impostor>>& impostorsToDisplay,
  int currentSpreeLength, int firstIndexSpree) {

  if (currentSpreeLength != 0) { // otherwise first call, there is no spree yet

    _textures.push_back(impostorsToDisplay[firstIndexSpree]->getTextureArray());
    _nbImpostorsInSpree.push_back(currentSpreeLength);

    for (int i = firstIndexSpree; i < firstIndexSpree + currentSpreeLength; i++) {
      const std::array<float, 12>& vertices = impostorsToDisplay[i]->getVertices();
      const std::array<float, 12>& posArray = impostorsToDisplay[i]->getPositionArray();
      const std::array<float,  8>& coord2D = impostorsToDisplay[i]->getCoord2D();
      const std::array<float,  4>& layer = impostorsToDisplay[i]->getLayer();

      std::copy(vertices.begin(), vertices.end(), _data.begin() + i*12);
      std::copy(posArray.begin(), posArray.end(), _data.begin() + _capacity*12 + i*12);
      std::copy(coord2D.begin(),  coord2D.end(),  _data.begin() + _capacity*24 + i*8);
      std::copy(layer.begin(),    layer.end(),    _data.begin() + _capacity*32 + i*4);
    }
  }
}

void ImpostorRenderer::loadImpostors(const std::vector<std::shared_ptr<Impostor>>& visibleImpostors, bool onlyOnce) {
  _textures.clear();
  _nbImpostorsInSpree.clear();

  _capacity = (int) visibleImpostors.size();
  _data.resize(_capacity * 36);

  int currentSpreeLength = 0;
  int firstIndexSpree = 0;

  const TextureArray* currentTexture = nullptr;

  for (int i = 0; i < visibleImpostors.size(); i++) {
    if (currentTexture != visibleImpostors[i]->getTextureArray()) {
      processSpree(visibleImpostors, currentSpreeLength, firstIndexSpree);
      currentTexture = visibleImpostors[i]->getTextureArray();
      firstIndexSpree += currentSpreeLength;
      currentSpreeLength = 0;
    }

    currentSpreeLength++;
  }

  processSpree(visibleImpostors, currentSpreeLength, firstIndexSpree);

  if (onlyOnce)
    fillBufferData(GL_STATIC_DRAW);
  else
    fillBufferData(GL_DYNAMIC_DRAW);
}

int ImpostorRenderer::renderImpostors() const {
  int cursor = 0;

  SCOPE_BIND(_vao)
  SCOPE_BIND(_ibo)

  // Allowing impostors not to be clipped inside the ground by offsetting the depth buffer slightly
  glEnable(GL_POLYGON_OFFSET_FILL);
  glPolygonOffset(-150.0, 150.0);

  for (int i = 0; i < _nbImpostorsInSpree.size(); i++) {
    SCOPE_BIND_PTR(_textures[i])

    glDrawElements(GL_TRIANGLES, 6 * _nbImpostorsInSpree[i], GL_UNSIGNED_INT, BUFFER_OFFSET(cursor * sizeof(GLuint)));

    cursor += 6 * _nbImpostorsInSpree[i];
  }

  glDisable(GL_POLYGON_OFFSET_FILL);

  return cursor / 6;
}
