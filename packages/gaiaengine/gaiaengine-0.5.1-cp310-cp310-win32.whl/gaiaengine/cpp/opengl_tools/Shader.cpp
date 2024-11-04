#include "Shader.h"

std::string Shader::glslVersion = "#version 330\n";

Shader::Shader(const std::string& vertexSourceFile, const std::string& fragmentSourceFile):
  GLObject(),
  _vertex(vertexSourceFile),
  _fragment(fragmentSourceFile)
{
  glAttachShader(getObjectID(), _vertex.getObjectID());
  glAttachShader(getObjectID(), _fragment.getObjectID());

  glLinkProgram(getObjectID());

  GLint errorLink(0);
  glGetProgramiv(getObjectID(), GL_LINK_STATUS, &errorLink);
  if (errorLink != GL_TRUE) {
    GLint sizeError(0);
    glGetProgramiv(getObjectID(), GL_INFO_LOG_LENGTH, &sizeError);

    char* error = new char[sizeError + 1];

    glGetShaderInfoLog(getObjectID(), sizeError, &sizeError, error);
    error[sizeError] = '\0';

    SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "(%s,%s): Error in shader linking: %s",
      vertexSourceFile.c_str(), fragmentSourceFile.c_str(), error);

    delete[] error;
    glDeleteProgram(getObjectID());
  }
}
