precision highp float;
varying vec2 vUV;

uniform sampler2D textureSampler;

void main(void) {
	gl_FragColor = vec4(0.2,0.5, 0.5, 0.5);
	// texture2D(textureSampler, vUV);
}	