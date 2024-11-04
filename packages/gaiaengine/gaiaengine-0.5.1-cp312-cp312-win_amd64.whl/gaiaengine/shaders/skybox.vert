// Version is defined by shader compiler, 330 for desktop and 300 es for mobile

layout (location = 0) in vec3 in_Vertex;
layout (location = 1) in vec2 in_TexCoords;
layout (location = 2) in float in_Layer;

out vec2 texCoords;
out float layer;

uniform mat4 MVP;

void main() {
	gl_Position =  MVP * vec4(in_Vertex,1);

	texCoords = in_TexCoords;
	layer = in_Layer;
}
