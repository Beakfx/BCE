//*****************************************************************************/
// 
// Filename: zigmod_template.glsl
//
// Beak f(x), 2016
//
//updated 2026, Beak ƒ(x)



// Matchbox shader: passthrough.glsl

#version 126

uniform sampler2D input1;
uniform sampler2D input2;

uniform float adsk_result_w;
uniform float adsk_result_h;

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(adsk_result_w, adsk_result_h);

    vec4 front = texture2D(input1, uv);
    vec4 matte = texture2D(input2, uv);

    gl_FragColor = vec4(front.rgb, matte.r);
}
