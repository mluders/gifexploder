//
//  gif.cpp
//  IO
//
//  Created by Miles Luders on 10/5/18.
//

#include "gif.hpp"

#include <iostream>
#include <math.h>
#include <fcntl.h>

HF_GIF::HF_GIF(std::string fname, int w, int h) : width(w), height(h) {
    lastR = 0;
    lastG = 0;
    lastB = 0;
    lastIndex = 0;
    currentPixel = 0;
    
    gif = ge_new_gif(
         fname.c_str(),
         width, height,
         palette,
         6, // depth,
         0
     );
}

float HF_GIF::distEuclidean(int r0, int g0, int b0, int r1, int g1, int b1) {
    int rd = r1 - r0;
    int gd = g1 - g0;
    int bd = b1 - b0;
    return rd*rd + gd*gd + bd*bd;
}

int HF_GIF::nearestIndex(int r, int g, int b) {
    float min = 999999999;
    int idx = 0;
    for (int i=0; i<(numColors*3); i+=3) {
        float dist = distEuclidean(r, g, b, palette[i+0], palette[i+1], palette[i+2]);
        if (min > dist) {
            min = dist;
            idx = i / 3;
        }
    }
    return idx;
}

void HF_GIF::set_pixel(int r, int g, int b) {
    if (r == lastR && g == lastG && b == lastB) {
        gif->frame[currentPixel] = lastIndex;
    } else {
        lastR = r;
        lastG = g;
        lastB = b;
        lastIndex = nearestIndex(r, g, b);
        gif->frame[currentPixel] = lastIndex;
    }
    currentPixel++;
}

void HF_GIF::add_frame() {
    ge_add_frame(gif, 3);
    currentPixel = 0;
}

void HF_GIF::close_gif() {
    ge_close_gif(gif);
}
