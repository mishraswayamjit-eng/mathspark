/**
 * shareImage.ts — client-side PNG generation from a rendered DOM element.
 *
 * Dynamically imports html-to-image so it never lands in the SSR bundle.
 * Caller must pass an HTMLElement that is already in the DOM.
 */

export async function generateShareImage(element: HTMLElement): Promise<Blob> {
  const { toPng } = await import('html-to-image');

  const dataUrl = await toPng(element, {
    pixelRatio:  2,      // 2× → 1080×1080 from a 540×540 element
    cacheBust:   true,
    skipAutoScale: false,
  });

  // Convert data-URL → Blob
  const res = await fetch(dataUrl);
  return res.blob();
}
