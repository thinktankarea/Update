import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScoreBadge } from './ScoreBadge';
import { FactorTable } from './FactorTable';
import { DividendSnapshot } from './DividendSnapshot';
import { OttoScore } from '@/utils/types';
import { Building2, TrendingUp } from 'lucide-react';

interface ScoreCardProps {
  stock: OttoScore;
}

export function ScoreCard({ stock }: ScoreCardProps) {
  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-2xl text-gray-900">{stock.ticker}</CardTitle>
              <p className="text-lg text-gray-600">{stock.companyName}</p>
              <div className="flex items-center space-x-4 mt-2">
                <Badge variant="outline" className="flex items-center space-x-1">
                  <Building2 className="h-3 w-3" />
                  <span>{stock.sector}</span>
                </Badge>
                <Badge variant="outline">
                  Beta: {stock.beta.toFixed(2)}
                </Badge>
              </div>
            </div>
            <ScoreBadge score={stock.score} grade={stock.grade} size="lg" />
          </div>
        </CardHeader>
        <CardContent>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-blue-900 mb-2">Otto's Take</h4>
            <p className="text-blue-800">{stock.ottosTask}</p>
          </div>
        </CardContent>
      </Card>

      {/* Dividend Snapshot */}
      <DividendSnapshot dividend={stock.dividend} />

      {/* Factor Analysis */}
      <Card>
        <CardContent className="pt-6">
          <FactorTable factors={stock.factors} />
        </CardContent>
      </Card>

      {/* Score Modifiers */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg text-gray-900">Score Modifiers</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            {Object.entries(stock.modifiers).map(([key, value]) => (
              <div key={key} className="text-center">
                <p className="text-sm text-gray-500 capitalize">{key}</p>
                <p className={`font-bold text-lg ${value >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {value >= 0 ? '+' : ''}{value}
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}