'use client';

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { ComparisonCard } from '@/components/features/compare/ComparisonCard';
import { ComparisonTable } from '@/components/features/compare/ComparisonTable';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ottoAPI } from '@/utils/api';
import { OttoScore } from '@/utils/types';
import { ArrowLeft, Plus, X, GitCompare } from 'lucide-react';
import Link from 'next/link';

export default function ComparePage() {
  const [compareStocks, setCompareStocks] = useState<OttoScore[]>([]);
  const [searchTicker, setSearchTicker] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAddStock = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchTicker.trim() || compareStocks.length >= 3) return;

    // Check if stock already added
    if (compareStocks.some(stock => stock.ticker === searchTicker.toUpperCase())) {
      alert('Stock already added to comparison');
      return;
    }

    try {
      setLoading(true);
      const stock = await ottoAPI.getScore(searchTicker);
      setCompareStocks([...compareStocks, stock]);
      setSearchTicker('');
    } catch (error) {
      alert(`Could not find data for ${searchTicker.toUpperCase()}`);
    } finally {
      setLoading(false);
    }
  };

  const removeStock = (ticker: string) => {
    setCompareStocks(compareStocks.filter(stock => stock.ticker !== ticker));
  };

  const addQuickCompare = async () => {
    const tickers = ['AAPL', 'MSFT', 'JNJ'];
    try {
      setLoading(true);
      const stocks = await ottoAPI.compareStocks(tickers);
      setCompareStocks(stocks);
    } catch (error) {
      console.error('Failed to load comparison stocks:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/">
            <Button variant="ghost" className="flex items-center space-x-2 mb-4">
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Dashboard</span>
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">OttoCompare™ Tool</h1>
          <p className="text-gray-600 mt-2">
            Compare up to 3 stocks side-by-side to make informed investment decisions
          </p>
        </div>

        {/* Add Stocks */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle>Add Stocks to Compare</CardTitle>
              {compareStocks.length === 0 && (
                <Button onClick={addQuickCompare} variant="outline" disabled={loading}>
                  <GitCompare className="h-4 w-4 mr-2" />
                  Quick Compare (AAPL, MSFT, JNJ)
                </Button>
              )}
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddStock} className="flex space-x-2 mb-4">
              <Input
                placeholder="Enter ticker symbol (e.g., AAPL)"
                value={searchTicker}
                onChange={(e) => setSearchTicker(e.target.value)}
                disabled={compareStocks.length >= 3 || loading}
                className="flex-1"
              />
              <Button 
                type="submit" 
                disabled={compareStocks.length >= 3 || loading || !searchTicker.trim()}
              >
                <Plus className="h-4 w-4 mr-2" />
                {loading ? 'Adding...' : 'Add Stock'}
              </Button>
            </form>

            {/* Current Stocks */}
            {compareStocks.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {compareStocks.map((stock) => (
                  <div key={stock.ticker} className="flex items-center space-x-2 bg-blue-100 px-3 py-1 rounded-full">
                    <span className="font-medium text-blue-900">{stock.ticker}</span>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => removeStock(stock.ticker)}
                      className="h-5 w-5 p-0 text-blue-600 hover:text-blue-800"
                    >
                      <X className="h-3 w-3" />
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Comparison Results */}
        {compareStocks.length === 0 ? (
          <Card>
            <CardContent className="py-12">
              <div className="text-center">
                <GitCompare className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-600 mb-2">
                  No Stocks Selected
                </h3>
                <p className="text-gray-500">
                  Add stocks using the search above or try the quick compare option
                </p>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-8">
            {/* Stock Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {compareStocks.map((stock) => (
                <ComparisonCard key={stock.ticker} stock={stock} />
              ))}
            </div>

            {/* Comparison Table */}
            {compareStocks.length >= 2 && (
              <ComparisonTable stocks={compareStocks} />
            )}
          </div>
        )}
      </main>
    </div>
  );
}