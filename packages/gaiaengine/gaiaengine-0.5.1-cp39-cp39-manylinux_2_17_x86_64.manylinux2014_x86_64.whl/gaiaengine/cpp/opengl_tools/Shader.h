#pragma once

#include <opengl.h>
#include <SDL_log.h>

#include "GLObject.h"
#include "utils.h"

#include <cassert>
#include <string>

class Shader : public GLObject<Shader> {
public:
  // To manage the vertex and the fragment shaders
  template<GLenum ShaderType>
  class SingleShader : public GLObject<SingleShader<ShaderType>> {
  public:
    SingleShader(const std::string& sourceFile) : GLObject<SingleShader>() {
      std::string absolutePath = GAIA_SOURCE_PATH + std::string("/shaders/") + sourceFile;
      std::string sourceCode = ut::textFileToString(absolutePath);

      const GLchar* str = sourceCode.c_str();
      const char* sources[2] = { getGLSLVersion().c_str(), str };

      glShaderSource(GLObject<SingleShader>::getObjectID(), 2, sources, 0);
      glCompileShader(GLObject<SingleShader>::getObjectID());

      GLint compilationError(0);
      glGetShaderiv(GLObject<SingleShader>::getObjectID(), GL_COMPILE_STATUS, &compilationError);
      
      if (compilationError != GL_TRUE) {
        GLint errorLength(0);
        glGetShaderiv(GLObject<SingleShader>::getObjectID(), GL_INFO_LOG_LENGTH, &errorLength);

        char* error = new char[errorLength + 1];

        glGetShaderInfoLog(GLObject<SingleShader>::getObjectID(), errorLength, &errorLength, error);
        error[errorLength] = '\0';

        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "%s: Error in shader compilation: %s", sourceFile.c_str(), error);

        delete[] error;
        glDeleteShader(GLObject<SingleShader>::getObjectID());

        assert(false);
      }
    }

  private:
    static void genObject(GLuint& objectID) { objectID = glCreateShader(ShaderType); };
    static void bindObject(GLuint /*objectID*/) { /* Shaders are used through programs, not by themselves */ };
    static void deleteObject(GLuint objectID) { glDeleteShader(objectID); };

    friend class GLObject<SingleShader>;
  };

  Shader(const std::string& vertexSourceFile, const std::string& fragmentSourceFile);

  inline GLint getUniformLocation(const GLchar* name) const { return glGetUniformLocation(getObjectID(), name); }

  inline static const std::string& getGLSLVersion() { return glslVersion; }

private:
  static void genObject(GLuint& objectID) { objectID = glCreateProgram(); };
  static void bindObject(GLuint objectID) { glUseProgram(objectID); };
  static void deleteObject(GLuint objectID) { glDeleteProgram(objectID); };

  friend class GLObject;

  static std::string glslVersion;

  SingleShader<GL_VERTEX_SHADER> _vertex;
  SingleShader<GL_FRAGMENT_SHADER> _fragment;
};
