import { cn } from '@/lib/utils';

interface ScoreBadgeProps {
  score: number;
  grade: string;
  size?: 'sm' | 'md' | 'lg';
}

export function ScoreBadge({ score, grade, size = 'md' }: ScoreBadgeProps) {
  const getScoreColor = (score: number) => {
    if (score >= 90) return 'bg-emerald-500';
    if (score >= 80) return 'bg-blue-500';
    if (score >= 70) return 'bg-yellow-500';
    if (score >= 60) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getTextColor = (score: number) => {
    if (score >= 90) return 'text-emerald-700';
    if (score >= 80) return 'text-blue-700';
    if (score >= 70) return 'text-yellow-700';
    if (score >= 60) return 'text-orange-700';
    return 'text-red-700';
  };

  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1',
    lg: 'text-lg px-4 py-2'
  };

  return (
    <div className="flex items-center space-x-2">
      <div className={cn(
        'rounded-full text-white font-bold flex items-center justify-center',
        getScoreColor(score),
        size === 'sm' ? 'w-8 h-8 text-xs' : size === 'md' ? 'w-10 h-10 text-sm' : 'w-12 h-12 text-lg'
      )}>
        {score}
      </div>
      <span className={cn(
        'font-semibold',
        getTextColor(score),
        sizeClasses[size]
      )}>
        Grade {grade}
      </span>
    </div>
  );
}