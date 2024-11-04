#include "FrameBufferObject.h"

#include <SDL_log.h>

#include "Texture.h"

FrameBufferObject::FrameBufferObject(const glm::ivec2& size, GLenum colorBufferInternalFormat, GLenum colorBufferFormat, GLenum colorBufferType):
  GLObject(),
  _size(size),
  _colorBuffer(std::make_shared<Texture>()),
  _depthBuffer(std::make_shared<Texture>())
{
  SCOPE_BIND_PTR(_colorBuffer)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
  glTexImage2D(GL_TEXTURE_2D, 0, colorBufferInternalFormat, size.x, size.y, 0, colorBufferFormat, colorBufferType, 0);

  SCOPE_BIND_PTR(_depthBuffer)
  glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT24, size.x, size.y,
    0, GL_DEPTH_COMPONENT, GL_UNSIGNED_INT, NULL);

  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);

  _depthBuffer->unbind();

  bind();
  _colorBuffer->attachToBoundFBO(GL_COLOR_ATTACHMENT0);
  _depthBuffer->attachToBoundFBO(GL_DEPTH_ATTACHMENT);

  if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) {
    SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Error in FrameBufferObject::init, unable to create FBO");
    switch (glCheckFramebufferStatus(GL_FRAMEBUFFER)) {
    case GL_FRAMEBUFFER_UNDEFINED:                     SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "GL_FRAMEBUFFER_UNDEFINED"); break;
    case GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT:         SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT"); break;
    case GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT: SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT"); break;
    case GL_FRAMEBUFFER_UNSUPPORTED:                   SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "GL_FRAMEBUFFER_UNSUPPORTED"); break;
    case GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE:        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE"); break;
    case GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER:        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER"); break;
    case GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER:        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER"); break;
    case GL_FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS:      SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "GL_FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS"); break;
    }
  }

  unbind();
}
