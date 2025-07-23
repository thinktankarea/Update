import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScoreBadge } from '../score/ScoreBadge';
import { OttoScore } from '@/utils/types';

interface ComparisonTableProps {
  stocks: OttoScore[];
}

export function ComparisonTable({ stocks }: ComparisonTableProps) {
  const comparisonRows = [
    { label: 'OttoScore', key: 'score', format: (value: number) => value.toString() },
    { label: 'Dividend Yield', key: 'dividend.yield', format: (value: number) => `${value.toFixed(1)}%` },
    { label: 'Frequency', key: 'dividend.frequency', format: (value: string) => value },
    { label: 'Payout Ratio', key: 'dividend.payoutRatio', format: (value: number) => `${value}%` },
    { label: 'Growth Rate', key: 'dividend.growthRate', format: (value: number) => `${value.toFixed(1)}%` },
    { label: 'Beta', key: 'beta', format: (value: number) => value.toFixed(2) },
    { label: 'Sector', key: 'sector', format: (value: string) => value },
    { label: 'Growth Factor', key: 'factors.growth', format: (value: number) => `${value}/100` },
    { label: 'Safety Factor', key: 'factors.safety', format: (value: number) => `${value}/100` },
    { label: 'Consistency Factor', key: 'factors.consistency', format: (value: number) => `${value}/100` },
  ];

  const getValue = (obj: any, path: string) => {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Side-by-Side Comparison</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b">
                <th className="text-left p-3 font-medium text-gray-900">Metric</th>
                {stocks.map((stock) => (
                  <th key={stock.ticker} className="text-center p-3 min-w-[150px]">
                    <div className="space-y-2">
                      <div className="font-semibold text-gray-900">{stock.ticker}</div>
                      <ScoreBadge score={stock.score} grade={stock.grade} size="sm" />
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {comparisonRows.map((row, index) => (
                <tr key={row.key} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                  <td className="p-3 font-medium text-gray-700">{row.label}</td>
                  {stocks.map((stock) => {
                    const value = getValue(stock, row.key);
                    return (
                      <td key={stock.ticker} className="p-3 text-center">
                        {row.key === 'score' ? (
                          <Badge variant={value >= 80 ? 'default' : value >= 60 ? 'secondary' : 'destructive'}>
                            {row.format(value)}
                          </Badge>
                        ) : (
                          <span className="text-gray-900">{row.format(value)}</span>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}