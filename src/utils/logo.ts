/**
 * Height, in pixels, at which a logo covers `area` square pixels. Logos of any
 * shape read at the same visual weight when they cover the same area, so a
 * wide wordmark sits lower and a square mark taller.
 */
export function logoHeight(image: ImageMetadata, area: number): number {
  return Math.round(Math.sqrt(area / (image.width / image.height)));
}
