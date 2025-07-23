'use client';

import { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { CalendarView } from '@/components/features/calendar/CalendarView';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CalendarStock } from '@/utils/types';
import { calendarStocks } from '@/utils/mockData';
import { ArrowLeft, Plus, Search } from 'lucide-react';
import Link from 'next/link';

export default function CalendarPage() {
  const [selectedStocks, setSelectedStocks] = useState<CalendarStock[]>([]);
  const [searchTicker, setSearchTicker] = useState('');
  const [searchResults, setSearchResults] = useState<CalendarStock[]>([]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchTicker.trim()) {
      const results = calendarStocks.filter(stock => 
        stock.ticker.toLowerCase().includes(searchTicker.toLowerCase()) ||
        stock.companyName.toLowerCase().includes(searchTicker.toLowerCase())
      );
      setSearchResults(results);
    } else {
      setSearchResults([]);
    }
  };

  const addStock = (stock: CalendarStock) => {
    if (selectedStocks.length < 3 && !selectedStocks.find(s => s.ticker === stock.ticker)) {
      setSelectedStocks([...selectedStocks, stock]);
      setSearchResults([]);
      setSearchTicker('');
    }
  };

  const removeStock = (ticker: string) => {
    setSelectedStocks(selectedStocks.filter(s => s.ticker !== ticker));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link href="/">
            <Button variant="ghost" className="flex items-center space-x-2 mb-4">
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Dashboard</span>
            </Button>
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Otto3x12™ Calendar Builder</h1>
          <p className="text-gray-600 mt-2">
            Build a monthly dividend income plan using three quarterly-paying stocks
          </p>
        </div>

        {/* Stock Search */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Add Stocks to Your Plan</CardTitle>
            <p className="text-sm text-gray-600">
              Search and add up to 3 quarterly dividend-paying stocks
            </p>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSearch} className="flex space-x-2 mb-4">
              <Input
                placeholder="Search by ticker or company name"
                value={searchTicker}
                onChange={(e) => setSearchTicker(e.target.value)}
                className="flex-1"
              />
              <Button type="submit">
                <Search className="h-4 w-4 mr-2" />
                Search
              </Button>
            </form>

            {/* Search Results */}
            {searchResults.length > 0 && (
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">Search Results:</h4>
                {searchResults.map((stock) => (
                  <div key={stock.ticker} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="font-semibold">{stock.ticker}</p>
                      <p className="text-sm text-gray-600">{stock.companyName}</p>
                      <p className="text-sm text-green-600">{stock.yield.toFixed(1)}% yield</p>
                    </div>
                    <Button
                      size="sm"
                      onClick={() => addStock(stock)}
                      disabled={selectedStocks.length >= 3 || selectedStocks.some(s => s.ticker === stock.ticker)}
                    >
                      <Plus className="h-4 w-4 mr-1" />
                      Add
                    </Button>
                  </div>
                ))}
              </div>
            )}

            {/* Quick Add Suggestions */}
            {searchResults.length === 0 && (
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900">Suggested Stocks:</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {calendarStocks.slice(0, 3).map((stock) => (
                    <div key={stock.ticker} className="p-3 border rounded-lg">
                      <div className="flex justify-between items-center">
                        <div>
                          <p className="font-semibold">{stock.ticker}</p>
                          <p className="text-xs text-gray-600">{stock.companyName}</p>
                          <p className="text-sm text-green-600">{stock.yield.toFixed(1)}% yield</p>
                        </div>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => addStock(stock)}
                          disabled={selectedStocks.length >= 3 || selectedStocks.some(s => s.ticker === stock.ticker)}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Calendar View */}
        <CalendarView 
          selectedStocks={selectedStocks} 
          onRemoveStock={removeStock}
        />
      </main>
    </div>
  );
}