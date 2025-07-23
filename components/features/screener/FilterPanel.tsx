'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { ScreenerFilters } from '@/utils/types';

interface FilterPanelProps {
  onFiltersChange: (filters: ScreenerFilters) => void;
}

export function FilterPanel({ onFiltersChange }: FilterPanelProps) {
  const [filters, setFilters] = useState<ScreenerFilters>({
    minYield: 0,
    maxYield: 10,
    sectors: [],
    frequency: [],
    maxBeta: 2,
    minScore: 0,
    maxScore: 100
  });

  const sectors = ['Technology', 'Healthcare', 'REITs', 'Utilities', 'Financial', 'ETFs'];
  const frequencies = ['Monthly', 'Quarterly', 'Semi-Annual', 'Annual'];

  const handleSectorChange = (sector: string, checked: boolean) => {
    const newSectors = checked 
      ? [...(filters.sectors || []), sector]
      : (filters.sectors || []).filter(s => s !== sector);
    
    const newFilters = { ...filters, sectors: newSectors };
    setFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const handleFrequencyChange = (frequency: string, checked: boolean) => {
    const newFrequencies = checked 
      ? [...(filters.frequency || []), frequency]
      : (filters.frequency || []).filter(f => f !== frequency);
    
    const newFilters = { ...filters, frequency: newFrequencies };
    setFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const handleYieldChange = (values: number[], type: 'min' | 'max') => {
    const newFilters = { 
      ...filters, 
      [type === 'min' ? 'minYield' : 'maxYield']: values[0] 
    };
    setFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const resetFilters = () => {
    const resetFilters: ScreenerFilters = {
      minYield: 0,
      maxYield: 10,
      sectors: [],
      frequency: [],
      maxBeta: 2,
      minScore: 0,
      maxScore: 100
    };
    setFilters(resetFilters);
    onFiltersChange(resetFilters);
  };

  return (
    <Card className="h-fit">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>Filters</CardTitle>
          <Button variant="outline" size="sm" onClick={resetFilters}>
            Reset
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Yield Range */}
        <div className="space-y-4">
          <Label className="text-sm font-medium">Dividend Yield Range</Label>
          <div className="space-y-3">
            <div>
              <Label className="text-xs text-gray-500">Minimum: {filters.minYield}%</Label>
              <Slider
                value={[filters.minYield || 0]}
                onValueChange={(values) => handleYieldChange(values, 'min')}
                max={10}
                min={0}
                step={0.1}
                className="mt-2"
              />
            </div>
            <div>
              <Label className="text-xs text-gray-500">Maximum: {filters.maxYield}%</Label>
              <Slider
                value={[filters.maxYield || 10]}
                onValueChange={(values) => handleYieldChange(values, 'max')}
                max={10}
                min={0}
                step={0.1}
                className="mt-2"
              />
            </div>
          </div>
        </div>

        {/* Sectors */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Sectors</Label>
          <div className="space-y-2">
            {sectors.map((sector) => (
              <div key={sector} className="flex items-center space-x-2">
                <Checkbox
                  id={`sector-${sector}`}
                  checked={(filters.sectors || []).includes(sector)}
                  onCheckedChange={(checked) => 
                    handleSectorChange(sector, checked as boolean)
                  }
                />
                <Label 
                  htmlFor={`sector-${sector}`} 
                  className="text-sm font-normal"
                >
                  {sector}
                </Label>
              </div>
            ))}
          </div>
        </div>

        {/* Dividend Frequency */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Dividend Frequency</Label>
          <div className="space-y-2">
            {frequencies.map((frequency) => (
              <div key={frequency} className="flex items-center space-x-2">
                <Checkbox
                  id={`freq-${frequency}`}
                  checked={(filters.frequency || []).includes(frequency)}
                  onCheckedChange={(checked) => 
                    handleFrequencyChange(frequency, checked as boolean)
                  }
                />
                <Label 
                  htmlFor={`freq-${frequency}`} 
                  className="text-sm font-normal"
                >
                  {frequency}
                </Label>
              </div>
            ))}
          </div>
        </div>

        {/* Beta */}
        <div className="space-y-3">
          <Label className="text-sm font-medium">Maximum Beta: {filters.maxBeta}</Label>
          <Slider
            value={[filters.maxBeta || 2]}
            onValueChange={(values) => {
              const newFilters = { ...filters, maxBeta: values[0] };
              setFilters(newFilters);
              onFiltersChange(newFilters);
            }}
            max={3}
            min={0.1}
            step={0.1}
          />
        </div>

        {/* OttoScore Range */}
        <div className="space-y-4">
          <Label className="text-sm font-medium">OttoScore Range</Label>
          <div className="space-y-3">
            <div>
              <Label className="text-xs text-gray-500">Minimum: {filters.minScore}</Label>
              <Slider
                value={[filters.minScore || 0]}
                onValueChange={(values) => {
                  const newFilters = { ...filters, minScore: values[0] };
                  setFilters(newFilters);
                  onFiltersChange(newFilters);
                }}
                max={100}
                min={0}
                step={1}
                className="mt-2"
              />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}