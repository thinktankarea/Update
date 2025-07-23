'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { CalendarStock } from '@/utils/types';
import { Calendar, DollarSign, TrendingUp } from 'lucide-react';

interface CalendarViewProps {
  selectedStocks: CalendarStock[];
  onRemoveStock: (ticker: string) => void;
}

export function CalendarView({ selectedStocks, onRemoveStock }: CalendarViewProps) {
  const months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];

  const getMonthPayments = (month: number) => {
    return selectedStocks.filter(stock => 
      stock.paymentMonths.includes(month + 1)
    );
  };

  const getTotalMonthlyIncome = (month: number, investment: number = 10000) => {
    const monthPayments = getMonthPayments(month);
    const perStockInvestment = investment / selectedStocks.length;
    
    return monthPayments.reduce((total, stock) => {
      const annualIncome = (perStockInvestment * stock.yield) / 100;
      const quarterlyIncome = annualIncome / 4; // Assuming quarterly payments
      return total + quarterlyIncome;
    }, 0);
  };

  const totalAnnualIncome = selectedStocks.reduce((total, stock) => {
    return total + (10000 / selectedStocks.length) * (stock.yield / 100);
  }, 0);

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <DollarSign className="h-8 w-8 text-green-600" />
              <div>
                <p className="text-sm text-gray-600">Annual Income</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${totalAnnualIncome.toFixed(0)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-8 w-8 text-blue-600" />
              <div>
                <p className="text-sm text-gray-600">Avg Yield</p>
                <p className="text-2xl font-bold text-gray-900">
                  {selectedStocks.length > 0 
                    ? (selectedStocks.reduce((sum, s) => sum + s.yield, 0) / selectedStocks.length).toFixed(1)
                    : '0.0'
                  }%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Calendar className="h-8 w-8 text-purple-600" />
              <div>
                <p className="text-sm text-gray-600">Stocks Selected</p>
                <p className="text-2xl font-bold text-gray-900">{selectedStocks.length}/3</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Calendar Grid */}
      <Card>
        <CardHeader>
          <CardTitle>Monthly Payment Schedule</CardTitle>
          <p className="text-sm text-gray-600">
            Based on $10,000 equally distributed across selected stocks
          </p>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {months.map((month, index) => {
              const monthPayments = getMonthPayments(index);
              const monthlyIncome = getTotalMonthlyIncome(index);
              
              return (
                <div key={month} className="border rounded-lg p-4 space-y-3">
                  <div className="text-center">
                    <h3 className="font-semibold text-gray-900">{month}</h3>
                    <p className="text-sm text-green-600 font-medium">
                      ${monthlyIncome.toFixed(0)}
                    </p>
                  </div>
                  
                  <div className="space-y-1">
                    {monthPayments.length > 0 ? (
                      monthPayments.map((stock) => (
                        <Badge key={stock.ticker} variant="secondary" className="text-xs">
                          {stock.ticker}
                        </Badge>
                      ))
                    ) : (
                      <p className="text-xs text-gray-400 text-center">No payments</p>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Selected Stocks */}
      <Card>
        <CardHeader>
          <CardTitle>Selected Stocks</CardTitle>
        </CardHeader>
        <CardContent>
          {selectedStocks.length === 0 ? (
            <p className="text-gray-500 text-center py-8">
              No stocks selected. Add stocks to build your 3x12 plan.
            </p>
          ) : (
            <div className="space-y-3">
              {selectedStocks.map((stock) => (
                <div key={stock.ticker} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div>
                      <p className="font-semibold">{stock.ticker}</p>
                      <p className="text-sm text-gray-600">{stock.companyName}</p>
                    </div>
                    <Badge>Score: {stock.score}</Badge>
                    <Badge variant="outline">{stock.yield.toFixed(1)}% yield</Badge>
                  </div>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    onClick={() => onRemoveStock(stock.ticker)}
                  >
                    Remove
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}