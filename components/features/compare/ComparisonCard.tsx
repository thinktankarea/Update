import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScoreBadge } from '../score/ScoreBadge';
import { DividendSnapshot } from '../score/DividendSnapshot';
import { OttoScore } from '@/utils/types';
import { Building2 } from 'lucide-react';

interface ComparisonCardProps {
  stock: OttoScore;
}

export function ComparisonCard({ stock }: ComparisonCardProps) {
  return (
    <Card className="h-full">
      <CardHeader>
        <div className="space-y-3">
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-xl">{stock.ticker}</CardTitle>
              <p className="text-sm text-gray-600">{stock.companyName}</p>
            </div>
            <ScoreBadge score={stock.score} grade={stock.grade} size="md" />
          </div>
          <div className="flex items-center space-x-2">
            <Building2 className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-600">{stock.sector}</span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <DividendSnapshot dividend={stock.dividend} />
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <h4 className="font-semibold text-blue-900 text-sm mb-2">Otto's Take</h4>
          <p className="text-blue-800 text-sm">{stock.ottosTask}</p>
        </div>
      </CardContent>
    </Card>
  );
}