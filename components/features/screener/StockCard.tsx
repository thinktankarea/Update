import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScoreBadge } from '../score/ScoreBadge';
import { OttoScore } from '@/utils/types';
import { TrendingUp, Building2, Calendar } from 'lucide-react';

interface StockCardProps {
  stock: OttoScore;
}

export function StockCard({ stock }: StockCardProps) {
  return (
    <Link href={`/score/${stock.ticker}`}>
      <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer">
        <CardHeader className="pb-3">
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-lg">{stock.ticker}</CardTitle>
              <p className="text-sm text-gray-600 line-clamp-1">{stock.companyName}</p>
            </div>
            <ScoreBadge score={stock.score} grade={stock.grade} size="sm" />
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-1 text-green-600">
              <TrendingUp className="h-4 w-4" />
              <span className="font-semibold">{stock.dividend.yield.toFixed(1)}%</span>
            </div>
            <Badge variant="outline" className="text-xs">
              {stock.dividend.frequency}
            </Badge>
          </div>
          
          <div className="flex items-center space-x-2">
            <Building2 className="h-3 w-3 text-gray-400" />
            <span className="text-xs text-gray-600">{stock.sector}</span>
          </div>
          
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div>
              <span className="text-gray-500">Beta:</span>
              <span className="ml-1 font-medium">{stock.beta.toFixed(2)}</span>
            </div>
            <div>
              <span className="text-gray-500">Payout:</span>
              <span className="ml-1 font-medium">{stock.dividend.payoutRatio}%</span>
            </div>
          </div>
          
          <p className="text-xs text-gray-600 line-clamp-2">
            {stock.ottosTask}
          </p>
        </CardContent>
      </Card>
    </Link>
  );
}