import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, Calendar, Percent, DollarSign } from 'lucide-react';

interface DividendSnapshotProps {
  dividend: {
    yield: number;
    frequency: string;
    payoutRatio: number;
    growthRate: number;
  };
}

export function DividendSnapshot({ dividend }: DividendSnapshotProps) {
  const metrics = [
    {
      icon: Percent,
      label: 'Yield',
      value: `${dividend.yield.toFixed(1)}%`,
      color: 'text-blue-600'
    },
    {
      icon: Calendar,
      label: 'Frequency',
      value: dividend.frequency,
      color: 'text-purple-600'
    },
    {
      icon: DollarSign,
      label: 'Payout Ratio',
      value: `${dividend.payoutRatio}%`,
      color: 'text-green-600'
    },
    {
      icon: TrendingUp,
      label: 'Growth Rate',
      value: `${dividend.growthRate.toFixed(1)}%`,
      color: 'text-orange-600'
    }
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg text-gray-900">Dividend Snapshot</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          {metrics.map((metric) => (
            <div key={metric.label} className="flex items-center space-x-3">
              <div className={`p-2 rounded-lg bg-gray-50 ${metric.color}`}>
                <metric.icon className="h-4 w-4" />
              </div>
              <div>
                <p className="text-sm text-gray-500">{metric.label}</p>
                <p className="font-semibold text-gray-900">{metric.value}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}