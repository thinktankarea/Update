import { Header } from '@/components/layout/Header';
import { ScoreCard } from '@/components/features/score/ScoreCard';
import { Card, CardContent } from '@/components/ui/card';
import { ottoAPI } from '@/utils/api';
import { OttoScore } from '@/utils/types';
import { mockStocks } from '@/utils/mockData';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';

export async function generateStaticParams() {
  return mockStocks.map((stock) => ({
    ticker: stock.ticker.toUpperCase(),
  }));
}

interface Props {
  params: { ticker: string };
}

export default async function ScorePage({ params }: Props) {
  const ticker = params.ticker.toUpperCase();
  let stock: OttoScore | null = null;

  try {
    stock = await ottoAPI.getScore(ticker);
  } catch (err) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="max-w-4xl mx-auto px-4 py-8">
          <Link href="/">
            <Button variant="ghost" className="flex items-center space-x-2 mb-4">
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Dashboard</span>
            </Button>
          </Link>
          <Card>
            <CardContent className="py-12">
              <div className="text-center">
                <p className="text-red-600 mb-4">Could not load data for {ticker}</p>
                <p className="text-gray-600 text-sm">
                  Try searching for a different ticker or check back later.
                </p>
              </div>
            </CardContent>
          </Card>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-8">
        <Link href="/">
          <Button variant="ghost" className="flex items-center space-x-2 mb-4">
            <ArrowLeft className="h-4 w-4" />
            <span>Back to Dashboard</span>
          </Button>
        </Link>
        <ScoreCard stock={stock} />
      </main>
    </div>
  );
}
