import { ImageResponse } from 'next/og';

// App Router auto-wires this as /apple-icon.png (for iOS Add to Home Screen)
export const size = { width: 180, height: 180 };
export const contentType = 'image/png';

export default function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: 180,
          height: 180,
          borderRadius: 38,
          background: 'linear-gradient(135deg, #58CC02 0%, #46a302 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 105,
        }}
      >
        🧮
      </div>
    ),
    { width: 180, height: 180 },
  );
}
