import { NextResponse } from 'next/server';
import { runLeadRescue } from '@/lib/agent';

export const runtime = 'nodejs';
export const maxDuration = 60;

export async function POST() {
  try {
    const result = await runLeadRescue();
    return NextResponse.json(result);
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    return NextResponse.json(
      {
        error: message,
        hint: 'Configure AWS Bedrock credentials for the hackathon path, or enable Vercel AI Gateway/OIDC for the fallback live demo.'
      },
      { status: 500 }
    );
  }
}
