//
//  gifenc.h
//  GifExploder
//
//  Created by Miles Luders on 10/5/18.
//

#ifndef gifenc_h
#define gifenc_h

#include <stdint.h>

typedef struct ge_GIF {
    uint16_t w, h;
    int depth;
    int fd;
    int offset;
    int nframes;
    uint8_t *frame, *back;
    uint32_t partial;
    uint8_t buffer[0xFF];
} ge_GIF;

ge_GIF *ge_new_gif(
                   const char *fname, uint16_t width, uint16_t height,
                   uint8_t *palette, int depth, int loop
                   );
void ge_add_frame(ge_GIF *gif, uint16_t delay);
void ge_close_gif(ge_GIF* gif);

#endif /* gifenc_h */
