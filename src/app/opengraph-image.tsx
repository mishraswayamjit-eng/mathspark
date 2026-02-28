import { ImageResponse } from 'next/og';

export const runtime = 'edge';
export const alt = 'MathSpark — Fun Math Practice for Grade 4 IPM';
export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';

export default function OgImage() {
  return new ImageResponse(
    (
      <div
        style={{
          background: 'linear-gradient(135deg, #131F24 0%, #1a3040 50%, #58CC02 100%)',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'sans-serif',
          padding: '60px',
        }}
      >
        <div style={{ fontSize: 96, marginBottom: 24 }}>🧮</div>
        <div
          style={{
            fontSize: 72,
            fontWeight: 900,
            color: '#ffffff',
            textAlign: 'center',
            lineHeight: 1.1,
            marginBottom: 20,
            textShadow: '0 4px 20px rgba(0,0,0,0.4)',
          }}
        >
          MathSpark
        </div>
        <div
          style={{
            fontSize: 32,
            fontWeight: 700,
            color: 'rgba(255,255,255,0.80)',
            textAlign: 'center',
            letterSpacing: 1,
          }}
        >
          Grade 4 Math · IPM Exam Prep · India
        </div>
        <div
          style={{
            marginTop: 40,
            backgroundColor: 'rgba(88,204,2,0.20)',
            border: '2px solid rgba(88,204,2,0.60)',
            borderRadius: 16,
            padding: '12px 32px',
            fontSize: 22,
            fontWeight: 700,
            color: '#A8FF5A',
          }}
        >
          2,345 questions · Hints · Step-by-step solutions
        </div>
      </div>
    ),
    { ...size },
  );
}
