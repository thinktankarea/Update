import { Progress } from '@/components/ui/progress';

interface FactorTableProps {
  factors: {
    growth: number;
    safety: number;
    payout: number;
    consistency: number;
    valuation: number;
  };
}

export function FactorTable({ factors }: FactorTableProps) {
  const factorData = [
    { name: 'Growth', value: factors.growth, description: 'Dividend growth potential' },
    { name: 'Safety', value: factors.safety, description: 'Financial stability' },
    { name: 'Payout', value: factors.payout, description: 'Payout sustainability' },
    { name: 'Consistency', value: factors.consistency, description: 'Payment reliability' },
    { name: 'Valuation', value: factors.valuation, description: 'Current valuation appeal' }
  ];

  const getProgressColor = (value: number) => {
    if (value >= 80) return 'bg-emerald-500';
    if (value >= 60) return 'bg-blue-500';
    if (value >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Factor Breakdown</h3>
      <div className="space-y-3">
        {factorData.map((factor) => (
          <div key={factor.name} className="space-y-2">
            <div className="flex justify-between items-center">
              <div>
                <span className="font-medium text-gray-900">{factor.name}</span>
                <p className="text-sm text-gray-500">{factor.description}</p>
              </div>
              <span className="font-bold text-gray-900">{factor.value}/100</span>
            </div>
            <div className="relative">
              <Progress value={factor.value} className="h-2" />
              <div 
                className={`absolute top-0 left-0 h-2 rounded-full ${getProgressColor(factor.value)}`}
                style={{ width: `${factor.value}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}