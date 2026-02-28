import { ImageResponse } from 'next/og';

// App Router auto-wires this as /icon.png
export const size = { width: 192, height: 192 };
export const contentType = 'image/png';

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: 192,
          height: 192,
          borderRadius: 40,
          background: 'linear-gradient(135deg, #58CC02 0%, #46a302 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 110,
        }}
      >
        🧮
      </div>
    ),
    { width: 192, height: 192 },
  );
}
