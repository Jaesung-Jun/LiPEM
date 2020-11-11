#version 330
//https://www.khronos.org/opengl/wiki/Skeletal_Animation
// Vertex Shader
attribute vec4 Vertex;
attribute vec3 Normal;
attribute vec2 Index;
attribute vec2 Weight;
uniform mat4 ModelviewMatrix;
uniform mat4 ProjectionModelviewMatrix;
uniform mat4 Bone[10]; // Array of bones that you compute (animate) on the CPU and you upload to the shader
// --------------------
varying vec3 EyeNormal;
// --------------------
void main()
{
    vec4 newVertex;
    vec4 newNormal;
    int index;
    // --------------------
    index=int(Index.x); // Cast to int
    newVertex = (Bone[index] * Vertex) * Weight.x;
    newNormal = (Bone[index] * vec4(Normal, 0.0)) * Weight.x;
    index=int(Index.y); //Cast to int
    newVertex = (Bone[index] * Vertex) * Weight.y + newVertex;
    newNormal = (Bone[index] * vec4(Normal, 0.0)) * Weight.y + newNormal;
    EyeNormal = vec3(ModelviewMatrix * newNormal);
    gl_Position = ProjectionModelviewMatrix * vec4(newVertex.xyz, 1.0);
    TexCoord0 = TexCoord;
}