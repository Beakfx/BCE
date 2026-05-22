//*****************************************************************************/
// 
// Filename: BCE_SAM.glsl
//
// Beak f(x), 2026
//
// Matchbox shader: BCE SAM carrier / passthrough

#version 126

uniform sampler2D input1;
uniform sampler2D input2;

uniform float adsk_result_w;
uniform float adsk_result_h;

uniform bool preview_mode;

void main() {
    vec2 uv = gl_FragCoord.xy / vec2(adsk_result_w, adsk_result_h);

    vec4 front = texture2D(input1, uv);

    vec2 matte_uv = uv;
    if (preview_mode) {
        matte_uv = clamp(uv, vec2(0.0), vec2(1.0));
    }

    vec4 matte = texture2D(input2, matte_uv);

    gl_FragColor = vec4(front.rgb, matte.r);
}
