precision highp float;
varying vec2 vUV;

uniform vec4 diffuse;
uniform sampler2D textureSampler;

void main(void) {
	gl_FragColor = diffuse;
	// texture2D(textureSampler, vUV);
}	